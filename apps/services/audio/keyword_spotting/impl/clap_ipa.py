
"""
CLAP-IPA based keyword spotting implementation.
Uses CLAP model with IPA tokenization for multilingual keyword detection.
"""

from typing import Dict, Any, Optional, List, AsyncIterator, Union, Tuple
from collections import deque
import time
import asyncio
from datetime import datetime

import numpy as np
import torch
from transformers import DebertaV2Tokenizer, AutoProcessor
from pydantic import Field
import pyaudio
from loguru import logger

import packages
from services.audio.keyword_spotting.core import (
    CoreKeywordSpotter,
    KeywordSpotterConfig,
    DetectionResult,
    AudioProcessingError,
    ModelStateError
)
from .clap.encoders import SpeechEncoder, PhoneEncoder
class VoiceActivityDetector:
    """Voice activity detector for streaming audio"""
    
    def __init__(
        self, 
        energy_threshold: float = 0.01,
        silence_threshold: float = 0.5
    ) -> None:
        """
        Initialize VAD.
        
        Args:
            energy_threshold: Energy threshold for speech detection
            silence_threshold: Seconds of silence to consider speech ended
        """
        self.energy_threshold = energy_threshold
        self.silence_threshold = silence_threshold
        self.speaking_started = None
        self.is_speaking = False
        self.last_active_time = None

    def detect(self, audio_data: np.ndarray) -> Tuple[bool, Optional[float]]:
        """
        Detect voice activity in audio data.
        
        Args:
            audio_data: Audio samples
            
        Returns:
            Tuple of (is_speaking, speech_start_time)
        """
        current_time = time.time()
        
        # Calculate energy of latest audio chunk
        chunk_size = min(1600, len(audio_data))  # 100ms at 16kHz
        energy = np.mean(np.square(audio_data[-chunk_size:]))
        is_active = energy > self.energy_threshold
        
        # State transition logic
        if not self.is_speaking and is_active:
            self.speaking_started = current_time
            self.is_speaking = True
            self.last_active_time = current_time
        elif self.is_speaking and is_active:
            self.last_active_time = current_time
        elif self.is_speaking and not is_active:
            if current_time - self.last_active_time > self.silence_threshold:
                self.is_speaking = False
                self.speaking_started = None
        
        return self.is_speaking, self.speaking_started

class ClapIPAConfig(KeywordSpotterConfig):
    """Configuration for CLAP-IPA keyword spotter"""
    
    # Model settings
    model_path: str = Field(
        "anyspeech/clap-ipa-tiny-speech",
        description="Path to CLAP model checkpoint"
    )
    device: str = Field("cpu", description="Device to run model on (cpu/cuda)")
    max_sequence_length: int = Field(40000, gt=0, description="Maximum audio sequence length")
    
    # Streaming settings
    stream_chunk_size: int = Field(1024, gt=0, description="Audio chunk size for streaming")
    stream_buffer_duration: float = Field(3.0, gt=0, description="Audio buffer duration in seconds")
    
    # VAD settings
    vad_energy_threshold: float = Field(0.01, gt=0, description="Voice activity detection energy threshold")
    vad_silence_threshold: float = Field(0.5, gt=0, description="Silence duration (seconds) to end speech")
    
    # Detection settings
    detection_cooldown: float = Field(2.0, ge=0, description="Minimum time between keyword detections")

class ClapIPA(CoreKeywordSpotter):
    """
    CLAP-IPA based keyword spotter implementation.
    
    Uses CLAP speech and phone encoders with IPA tokenization for
    multilingual keyword spotting. Supports both batch and streaming detection.
    
    Features:
    - IPA-based phonetic matching
    - Voice activity detection for streaming
    - Multiple pronunciation support
    - Real-time processing capability
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[ClapIPAConfig] = None
    ) -> None:
        """Initialize the CLAP-IPA keyword spotter"""
        super().__init__(name, config, model_config)
        
        # Initialize models and processors to None
        self.device = torch.device(self.model_config.device)
        self._speech_encoder = None
        self._phone_encoder = None
        self._tokenizer = None
        self._processor = None
        
        # Keyword management
        self.keyword_data: Dict[str, Dict] = {}  # Stores IPA and embeddings
        self.last_detections: Dict[str, float] = {}  # Tracks detection times
        
        # Streaming components
        self._vad = VoiceActivityDetector(
            energy_threshold=self.model_config.vad_energy_threshold,
            silence_threshold=self.model_config.vad_silence_threshold
        )
        self._audio_buffer = deque(
            maxlen=int(self.model_config.sample_rate * self.model_config.stream_buffer_duration)
        )
        self._pyaudio = None
        self._stream = None

    def get_default_model_config(self) -> ClapIPAConfig:
        """Get default model configuration"""
        return ClapIPAConfig()

    def _setup_resources(self) -> None:
        """Setup models and processors"""
        try:
            logger.info(f"Loading models from {self.model_config.model_path}")
            
            # Load speech encoder
            self._speech_encoder = SpeechEncoder.from_pretrained(self.model_config.model_path)
            self._speech_encoder.to(self.device)
            self._speech_encoder.eval()
            
            # Load phone encoder
            self._phone_encoder = PhoneEncoder.from_pretrained('anyspeech/clap-ipa-tiny-phone')
            self._phone_encoder.to(self.device)
            self._phone_encoder.eval()
            
            # Load tokenizer and processor
            self._tokenizer = DebertaV2Tokenizer.from_pretrained(
                'charsiu/IPATokenizer',
                use_fast=True
            )
            self._processor = AutoProcessor.from_pretrained(
                'openai/whisper-tiny',
                truncation=True,
                use_fast=True
            )
            
            logger.info("Models and processors loaded successfully")
            
        except Exception as e:
            raise ModelStateError(f"Failed to initialize models: {str(e)}")

    def _cleanup_resources(self) -> None:
        """Cleanup resources"""
        # Stop streaming if active
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
            
        if self._pyaudio is not None:
            self._pyaudio.terminate()
            self._pyaudio = None
        
        # Clear buffers and caches
        self._audio_buffer.clear()
        self.keyword_data.clear()
        self.last_detections.clear()
        
        # Clear models
        self._speech_encoder = None
        self._phone_encoder = None
        self._tokenizer = None
        self._processor = None
        
        logger.info("Resources cleaned up successfully")

    def _validate_config(self) -> None:
        """Validate service configuration"""
        super()._validate_config()
        
        try:
            # Validate device
            if self.model_config.device not in ['cpu', 'cuda']:
                if self.model_config.device.startswith('cuda:'):
                    if not torch.cuda.is_available():
                        raise ValueError("CUDA not available")
                else:
                    raise ValueError(f"Unsupported device: {self.model_config.device}")
                    
            # Validate streaming parameters
            if self.model_config.stream_chunk_size > self.model_config.stream_buffer_duration * self.model_config.sample_rate:
                raise ValueError("Chunk size cannot be larger than buffer duration")
                
        except Exception as e:
            raise ModelStateError(f"Configuration validation failed: {str(e)}")

    async def extract_features(
        self,
        audio: np.ndarray,
        sample_rate: Optional[int] = None
    ) -> np.ndarray:
        """Extract speech features using CLAP encoder"""
        try:
            # Normalize audio
            audio, sample_rate = await self.normalize_audio(audio, sample_rate)
            
            # Prepare input
            inputs = self._processor(
                audio,
                sampling_rate=sample_rate,
                return_tensors='pt',
                return_attention_mask=True,
                max_length=self.model_config.max_sequence_length
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Extract features
            with torch.inference_mode():
                features = self._speech_encoder(
                    **inputs,
                    return_dict=True
                ).last_hidden_state.squeeze(0)
                
                # Average pooling
                features = torch.mean(features, dim=0, keepdim=True)
                
            return features.cpu().numpy()
            
        except Exception as e:
            raise AudioProcessingError(f"Feature extraction failed: {str(e)}")

    async def get_detection_scores(
        self,
        features: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Calculate detection scores for all keywords"""
        if not self.keywords:
            return {}
            
        try:
            # Convert to tensor
            features = torch.from_numpy(features).to(self.device)
            
            # Calculate similarities
            scores = {}
            with torch.inference_mode():
                for keyword, data in self.keyword_data.items():
                    similarity = torch.sum(features * data['embedding'], dim=1)
                    scores[keyword] = similarity.cpu().numpy()
                    
            return scores
            
        except Exception as e:
            raise ModelStateError(f"Detection scoring failed: {str(e)}")

    def _prepare_phone_embedding(self, ipa_string: str) -> torch.Tensor:
        """Prepare phone embedding for a keyword"""
        try:
            # Tokenize IPA string
            tokens = self._tokenizer(
                ''.join(ipa_string),
                return_attention_mask=False,
                return_length=True,
                return_token_type_ids=False,
                add_special_tokens=False
            )['input_ids']
            tokens = torch.tensor(tokens, device=self.device)
            
            # Generate embedding
            with torch.inference_mode():
                features = self._phone_encoder(
                    tokens.unsqueeze(0)
                ).last_hidden_state.squeeze(0)
                return torch.mean(features, dim=0, keepdim=True)
                
        except Exception as e:
            raise ModelStateError(f"Phone embedding failed: {str(e)}")

    def add_keyword(
        self,
        keyword: str,
        ipa_string: Optional[Union[str, List[str]]] = None
    ) -> None:
        """
        Add a keyword to the detection vocabulary
        
        Args:
            keyword: Keyword to detect
            ipa_string: IPA pronunciation(s) of the keyword
        """
        if not self.is_initialized:
            raise ModelStateError("Service must be initialized before adding keywords")
            
        if keyword in self.keywords:
            raise ValueError(f"Keyword '{keyword}' already exists")
            
        if ipa_string is None:
            raise ValueError("IPA string is required")
            
        try:
            # Handle multiple pronunciations
            if isinstance(ipa_string, str):
                ipa_strings = [ipa_string]
            else:
                ipa_strings = ipa_string
                
            # Prepare embeddings for all pronunciations
            embeddings = []
            for ipa in ipa_strings:
                embedding = self._prepare_phone_embedding(ipa)
                embeddings.append(embedding)
                
            # Store keyword data
            self.keyword_data[keyword] = {
                'ipa': ipa_strings,
                'embedding': torch.stack(embeddings).mean(dim=0)  # Average embeddings
            }
            self.last_detections[keyword] = 0
            self.keywords.append(keyword)
            
            logger.info(f"Added keyword '{keyword}' with {len(ipa_strings)} pronunciation(s)")
            
        except Exception as e:
            raise ModelStateError(f"Failed to add keyword: {str(e)}")

    def remove_keyword(self, keyword: str) -> None:
        """Remove a keyword from the detection vocabulary"""
        super().remove_keyword(keyword)  # This will raise ValueError if keyword doesn't exist
        
        # Clean up keyword data
        del self.keyword_data[keyword]
        if keyword in self.last_detections:
            del self.last_detections[keyword]
            
        logger.info(f"Removed keyword '{keyword}'")

    async def detect_keywords(
        self,
        audio: np.ndarray,
        sample_rate: Optional[int] = None
    ) -> List[DetectionResult]:
        """Detect keywords in audio data"""
        if not self.keywords:
            return []
            
        try:
            # Extract features
            features = await self.extract_features(audio, sample_rate)
            
            # Get detection scores
            scores = await self.get_detection_scores(features)
            
            # Process detections
            current_time = time.time()
            results = []
            
            for keyword, score_array in scores.items():
                max_score = float(np.max(score_array))
                
                # Check threshold and cooldown
                if (max_score > self._detection_threshold and 
                    (current_time - self.last_detections[keyword]) > self.model_config.detection_cooldown):
                    
                    # Update last detection time
                    self.last_detections[keyword] = current_time
                    
                    # Create detection result
                    result = DetectionResult(
                        keyword=keyword,
                        confidence=max_score,
                        start_time=0.0,  # Not meaningful for batch detection
                        end_time=float(len(audio)) / sample_rate if sample_rate else 0.0,
                        timestamp=datetime.utcnow()
                    )
                    results.append(result)
                    
                    logger.debug(f"Detected keyword '{keyword}' with confidence {max_score:.3f}")
            
            return results
            
        except Exception as e:
            raise AudioProcessingError(f"Keyword detection failed: {str(e)}")

    async def _audio_callback(self, in_data, frame_count, time_info, status):
        """Process incoming audio data"""
        try:
            # Convert to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            
            # Add to buffer
            self._audio_buffer.extend(audio_data)
            
            return (in_data, pyaudio.paContinue)
            
        except Exception as e:
            logger.error(f"Error in audio callback: {str(e)}")
            return (in_data, pyaudio.paComplete)

    def _setup_audio_stream(self) -> None:
        """Setup PyAudio stream for real-time processing"""
        try:
            if self._pyaudio is None:
                self._pyaudio = pyaudio.PyAudio()
                
            # Configure and open stream
            self._stream = self._pyaudio.open(
                format=pyaudio.paFloat32,
                channels=self.model_config.num_channels,
                rate=self.model_config.sample_rate,
                input=True,
                frames_per_buffer=self.model_config.stream_chunk_size,
                stream_callback=self._audio_callback
            )
            
            self._stream.start_stream()
            logger.info("Audio stream started")
            
        except Exception as e:
            raise AudioProcessingError(f"Failed to setup audio stream: {str(e)}")

    def _stop_audio_stream(self) -> None:
        """Stop and cleanup audio stream"""
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
            
        if self._pyaudio is not None:
            self._pyaudio.terminate()
            self._pyaudio = None
            
        self._audio_buffer.clear()
        logger.info("Audio stream stopped")

    async def stream_detect_keywords(
        self,
        audio_stream: Any,
        sample_rate: Optional[int] = None
    ) -> AsyncIterator[DetectionResult]:
        """
        Detect keywords in streaming audio data
        
        Args:
            audio_stream: Audio stream object (unused, using PyAudio instead)
            sample_rate: Sample rate of audio stream
            
        Yields:
            DetectionResult objects as keywords are detected
        """
        if not self.keywords:
            return
            
        try:
            # Setup audio streaming
            self._setup_audio_stream()
            
            while self._stream and self._stream.is_active():
                # Get current buffer
                current_audio = np.array(list(self._audio_buffer))
                
                if len(current_audio) >= self.model_config.sample_rate * 0.5:  # At least 0.5 seconds
                    # Check voice activity
                    is_speaking, speech_start = self._vad.detect(current_audio)
                    
                    if is_speaking:
                        # Detect keywords
                        detections = await self.detect_keywords(current_audio, self.model_config.sample_rate)
                        
                        # Update detection times and yield results
                        current_time = time.time()
                        for detection in detections:
                            # Calculate actual timestamps
                            if speech_start is not None:
                                detection.start_time = speech_start
                                detection.end_time = current_time
                                
                            yield detection
                
                # Sleep briefly to prevent CPU overload
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Streaming detection error: {str(e)}")
            raise
            
        finally:
            self._stop_audio_stream()

    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the service state"""
        info = super().get_service_info()
        
        # Add CLAP-specific information
        info.update({
            "model_path": self.model_config.model_path,
            "device": self.model_config.device,
            "streaming_active": self._stream is not None and self._stream.is_active(),
            "keywords": {
                keyword: {
                    "pronunciations": data["ipa"],
                    "last_detection": self.last_detections.get(keyword, 0)
                }
                for keyword, data in self.keyword_data.items()
            }
        })
        
        return info

# Example usage
if __name__ == "__main__":
    # Configuration
    config = ClapIPAConfig(
        model_path="anyspeech/clap-ipa-tiny-speech",
        device="cpu",
        sample_rate=16000,
        num_channels=1,
        detection_threshold=0.5,
        stream_chunk_size=1024,
        stream_buffer_duration=3.0
    )
    
    # Create service
    service = ClapIPA(
        name="CLAP-IPA-KWS",
        model_config=config
    )
    
    async def main():
        try:
            # Initialize service
            service.initialize()
            
            # Add some keywords
            service.add_keyword("hello", "həˈloʊ")
            service.add_keyword("goodbye", ["ɡʊdˈbaɪ", "ɡʊdˈbaɪ"])
            service.add_keyword("computer", "kəmˈpjuːtər")
            
            print("\nStarting keyword detection...")
            print(f"Active keywords: {service.get_keywords()}")
            print("Press Ctrl+C to stop")
            
            # Start streaming detection
            async for detection in service.stream_detect_keywords(None):
                print(f"\nDetected: {detection.keyword}")
                print(f"Confidence: {detection.confidence:.3f}")
                print(f"Time: {detection.start_time:.2f}s - {detection.end_time:.2f}s")
                
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            service.shutdown()
    
    # Run the service
    import asyncio
    asyncio.run(main())