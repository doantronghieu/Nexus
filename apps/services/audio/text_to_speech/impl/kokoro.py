"""
Kokoro Text-to-Speech implementation.
Provides integration with the Kokoro ONNX model for multilingual speech synthesis.
"""

import os
import json
from enum import Enum
from typing import Dict, Any, Optional, List, Union, Literal
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from pydantic import Field, ConfigDict
from loguru import logger
import tempfile

import packages
from services.audio.text_to_speech.core import CoreTextToSpeech, TTSConfig, AudioConfig


PATH_ASSETS = f"{packages.APP_PATH}/services/audio/text_to_speech/impl/assets/kokoro"

class KokoroModelType(str, Enum):
    """Available Kokoro model types"""
    NORMAL = "kokoro-v1.0.onnx"

class KokoroVoice(str, Enum):
    """Available Kokoro voices"""
    AF = "af"
    AF_BELLA = "af_bella"
    AF_NICOLE = "af_nicole"
    AF_SARAH = "af_sarah"
    AF_SKY = "af_sky"
    AM_ADAM = "am_adam"
    AM_MICHAEL = "am_michael"
    BF_EMMA = "bf_emma"
    BF_ISABELLA = "bf_isabella"
    BM_GEORGE = "bm_george"
    BM_LEWIS = "bm_lewis"

class KokoroConfig(TTSConfig):
    """Configuration for Kokoro TTS"""
    
    model_config = ConfigDict(protected_namespaces=())
    
    # Base AI model fields
    name: str = Field("kokoro", description="Model name")
    version: str = Field("0.19.0", description="Model version")
    type: str = Field("audio", description="Type of model")
    
    # Model settings
    tts_model_type: KokoroModelType = Field(
        KokoroModelType.NORMAL,
        description="Type of Kokoro model to use"
    )
    tts_model_path: str = Field(
        f"{PATH_ASSETS}",
        description="Path to Kokoro model directory"
    )
    voices_path: str = Field(
        f"{PATH_ASSETS}/voices.bin",
        description="Path to voices configuration file"
    )
    
    # Voice settings
    voice: KokoroVoice = Field(
        KokoroVoice.AF_SARAH,
        description="Default voice to use"
    )
    language: str = Field("en-us", description="Default language")
    
    # Performance settings
    use_cpu: bool = Field(
        True,
        description="Force CPU execution provider"
    )
    
    # Output settings
    output_dir: str = Field(
        f"{PATH_ASSETS}/outputs",
        description="Directory for output files"
    )

class KokoroTTS(CoreTextToSpeech):
    """
    Kokoro-based text-to-speech implementation.
    
    Implements speech synthesis using the Kokoro ONNX model with support for:
    - Multiple voices and accents
    - CPU/GPU inference
    - Model quantization options
    - Flexible audio output formats
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[KokoroConfig] = None,
        audio_config: Optional[AudioConfig] = None
    ) -> None:
        """Initialize Kokoro TTS service"""
        super().__init__(name, config, model_config, audio_config)
        
        # Initialize Kokoro-specific attributes
        self.kokoro = None
        self._voice_data = {}
        
        # Set ONNX provider if specified
        if self.model_config.use_cpu:
            os.environ["ONNX_PROVIDER"] = "CPUExecutionProvider"
        
        # Ensure output directory exists
        os.makedirs(self.model_config.output_dir, exist_ok=True)

    def get_default_model_config(self) -> KokoroConfig:
        """Get default model configuration"""
        return KokoroConfig()

    def _validate_config(self) -> None:
        pass

    def _setup_resources(self) -> None:
        """Setup Kokoro model and resources"""
        try:
            # Initialize Kokoro
            model_file = os.path.join(
                self.model_config.tts_model_path,
                self.model_config.tts_model_type
            )
            
            self.kokoro = Kokoro(
                model_file,
                self.model_config.voices_path
            )
            
            logger.info(f"Initialized Kokoro model from {model_file}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to setup Kokoro: {str(e)}")

    def _cleanup_resources(self) -> None:
        """Cleanup resources"""
        self.kokoro = None
        self._voice_data = {}

    async def generate_audio(
        self,
        text: str,
        audio_config: Optional[AudioConfig] = None,
        voice_override: Optional[str] = None
    ) -> bytes:
        """Generate audio from text using Kokoro"""
        try:
            # Debug logging for voice selection
            logger.info(f"Voice override requested: {voice_override}")
            logger.info(f"Default voice: {self.model_config.voice.value}")
            logger.info(f"Available voices: {list(self._voice_data.keys())}")
            
            # Validate text input
            if not text or not isinstance(text, str):
                raise ValueError("Text input must be a non-empty string")
            
            # Use provided config or default
            cfg = audio_config or self.audio_config or AudioConfig()
            
            # Handle voice override with debug logging
            if voice_override:
                # Convert voice ID to match expected format
                voice_id = voice_override.lower().strip()
                logger.info(f"Attempting to use voice: {voice_id}")
                
                # Validate voice exists
                if voice_id not in self._voice_data:
                    available = list(self._voice_data.keys())
                    logger.error(f"Voice '{voice_id}' not found. Available: {available}")
                    raise ValueError(f"Voice '{voice_id}' not found. Available: {available}")
                    
                logger.info(f"Voice '{voice_id}' validated and selected")
            else:
                voice_id = str(self.model_config.voice.value)
                logger.info(f"Using default voice: {voice_id}")
            
            # Generate audio using Kokoro
            try:
                logger.info(f"Creating audio with parameters:")
                logger.info(f"  - Voice: {voice_id}")
                logger.info(f"  - Speed: {float(cfg.speed)}")
                logger.info(f"  - Language: {str(self.model_config.language)}")
                
                samples, sample_rate = self.kokoro.create(
                    text=text.strip(),
                    voice=voice_id,
                    speed=float(cfg.speed),
                    lang=str(self.model_config.language)
                )
                
                logger.info(f"Audio generated successfully: {len(samples)} samples at {sample_rate}Hz")
                
            except Exception as e:
                logger.error(f"Kokoro create() failed: {str(e)}")
                raise RuntimeError(f"Audio generation failed: {str(e)}")
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(suffix=f".{cfg.format}", delete=False) as temp_file:
                if cfg.format == "wav":
                    sf.write(
                        temp_file.name,
                        samples,
                        sample_rate,
                        format=cfg.format.upper()
                    )
                else:
                    raise ValueError(f"Unsupported output format: {cfg.format}")
                
                # Read file contents
                with open(temp_file.name, 'rb') as f:
                    audio_data = f.read()
                
                # Cleanup
                os.unlink(temp_file.name)
                
            logger.info(f"Generated {len(audio_data)} bytes of audio data")
            return audio_data
            
        except Exception as e:
            logger.error(f"Audio generation failed: {str(e)}")
            raise
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(suffix=f".{cfg.format}", delete=False) as temp_file:
                if cfg.format == "wav":
                    sf.write(
                        temp_file.name,
                        samples,
                        sample_rate,
                        format=cfg.format.upper()
                    )
                else:
                    raise ValueError(f"Unsupported output format: {cfg.format}")
                
                # Read file contents
                with open(temp_file.name, 'rb') as f:
                    audio_data = f.read()
                
                # Cleanup temp file
                os.unlink(temp_file.name)
                
            return audio_data
            
        except Exception as e:
            logger.error(f"Audio generation failed: {str(e)}")
            raise

    @property
    def supported_models(self) -> List[str]:
        """Get list of supported model names/identifiers"""
        return [model.value for model in KokoroModelType]
    
    @property
    def available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices with their properties"""
        voices = []
        for voice in KokoroVoice:
            voice_id = voice.value
            if voice_id in self._voice_data:
                voices.append({
                    "id": voice_id,
                    "name": voice.name,
                    "data": self._voice_data[voice_id]
                })
        return voices

    @property
    def supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return ["en-us"]  # Add more as supported
    
    @property
    def supported_audio_formats(self) -> List[str]:
        """Get list of supported output audio formats"""
        return ["wav"]

    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the service state"""
        info = super().get_service_info()
        info.update({
            "model_type": self.model_config.tts_model_type,
            "current_voice": self.model_config.voice,
            "voice_count": len(self._voice_data),
            "output_formats": self.supported_audio_formats,
            "using_cpu": self.model_config.use_cpu
        })
        return info

if __name__ == "__main__":
    # Example usage
    config = KokoroConfig(
        tts_model_type=KokoroModelType.NORMAL,
        voice=KokoroVoice.AF_SARAH
    )
    
    service = KokoroTTS(
        name="KokoroTTS",
        model_config=config,
        audio_config=AudioConfig()
    )
    
    async def test():
        try:
            # Initialize service
            service.initialize()
            
            # Generate speech
            audio_data = await service.synthesize_text(
                text="Hello! This is a test of the Kokoro text-to-speech system.",
                audio_config=AudioConfig(speed=1.2)  # Optional config override
            )
            
            print(f"Generated {len(audio_data)} bytes of audio")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            service.shutdown()
    
    import asyncio
    asyncio.run(test())