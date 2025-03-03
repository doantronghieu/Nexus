import threading
import pyaudio
import numpy as np
from openwakeword.model import Model
from openwakeword.utils import download_models
import time
import queue
from typing import Optional, Callable, Any
from dataclasses import dataclass
import logging
from config import audio_config, model_config, app_config

class AudioStreamError(Exception):
    """Custom exception for audio stream errors."""
    pass

class ModelError(Exception):
    """Custom exception for model-related errors."""
    pass

@dataclass
class DetectionResult:
    """Data class for detection results."""
    wake_word: str
    confidence: float
    timestamp: float

class WakeWordDetector(threading.Thread):
    def __init__(
        self,
        callback_queue: queue.Queue,
        on_error: Optional[Callable[[Exception], Any]] = None
    ):
        super().__init__()
        self.logger = app_config.setup_logging('WakeWordDetector')
        self.callback_queue = callback_queue
        self.on_error = on_error or self._default_error_handler
        
        self._initialize_audio_stream()
        self.running = False
        self.owwModel = None
        
    def _initialize_audio_stream(self) -> None:
        """Initialize the audio stream with error handling."""
        try:
            self.audio = pyaudio.PyAudio()
            self.mic_stream = self.audio.open(
                format=self.audio.get_format_from_width(audio_config.FORMAT // 8),
                channels=audio_config.CHANNELS,
                rate=audio_config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=audio_config.CHUNK_SIZE,
            )
            self.logger.info("Audio stream initialized successfully")
        except Exception as e:
            raise AudioStreamError(f"Failed to initialize audio stream: {e}")
        
    def _load_model(self) -> None:
        """Load the wake word model with error handling."""
        try:
            self.owwModel = Model(
                wakeword_models=[model_config.WAKE_WORD],
                inference_framework=model_config.INFERENCE_FRAMEWORK
            )
            self.logger.info("Wake word model loaded successfully")
        except Exception as e:
            raise ModelError(f"Failed to load model: {e}")
    
    def _process_audio_chunk(self) -> None:
        """Process a single chunk of audio data."""
        try:
            audio = np.frombuffer(
                self.mic_stream.read(audio_config.CHUNK_SIZE), 
                dtype=np.int16
            )
            prediction = self.owwModel.predict(audio)
            self._handle_prediction(prediction)
        except Exception as e:
            self.logger.error(f"Error processing audio chunk: {e}")
            raise
            
    def _handle_prediction(self, prediction: dict) -> None:
        """Handle model predictions and trigger callbacks."""
        for mdl, scores in self.owwModel.prediction_buffer.items():
            if scores[-1] > model_config.CONFIDENCE_THRESHOLD:
                result = DetectionResult(
                    wake_word=mdl,
                    confidence=scores[-1],
                    timestamp=time.time()
                )
                self.logger.info(
                    f"Wake word detected: {result.wake_word} "
                    f"(confidence: {result.confidence:.2f})"
                )
                self.callback_queue.put(("wake_word_detected", result))
    
    def _default_error_handler(self, error: Exception) -> None:
        """Default error handler if none provided."""
        self.logger.error(f"Error in wake word detector: {error}")
        self.stop()
    
    def run(self) -> None:
        """Main detection loop."""
        self.logger.info("Starting wake word detection...")
        self.running = True
        
        try:
            self.logger.info("Downloading models...")
            download_models()
            self._load_model()
            
            while self.running:
                self._process_audio_chunk()
                time.sleep(0.01)  # Prevent CPU overuse
                
        except Exception as e:
            self.on_error(e)
        finally:
            self.stop()
            
    def stop(self) -> None:
        """Stop the detector and clean up resources."""
        self.logger.info("Stopping wake word detector...")
        self.running = False
        
        if hasattr(self, 'mic_stream'):
            try:
                self.mic_stream.stop_stream()
                self.mic_stream.close()
            except Exception as e:
                self.logger.error(f"Error closing mic stream: {e}")
                
        if hasattr(self, 'audio'):
            try:
                self.audio.terminate()
            except Exception as e:
                self.logger.error(f"Error terminating audio: {e}")
        
        self.logger.info("Wake word detector stopped")