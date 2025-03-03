"""
Core Wake Word Detection Implementation using OpenWakeWord
Provides wake word detection functionality with configurable models and parameters.
"""

import os
import time
import numpy as np
from typing import Any, Dict, Optional, Union, List
from pydantic import Field, validator
import openwakeword
from openwakeword.model import Model
from loguru import logger

import packages
from services.bases.ai import AIService, AIModelConfig

class WakeWordModelConfig(AIModelConfig):
    """Configuration for wake word detection model"""
    
    # Audio processing settings
    sample_rate: int = Field(default=16000, description="Audio sample rate in Hz")
    chunk_size: int = Field(default=1280, description="Audio chunk size in samples")
    
    # Wake word detection settings
    detection_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for wake word detection"
    )
    cooldown_period: float = Field(
        default=2.0,
        ge=0.0,
        description="Minimum time between detections in seconds"
    )
    
    # Model settings
    models_path: str = Field(
        default=f"{packages.ROOT_PATH}/data/assets/repos/openWakeWord/models",
        description="Path to wake word models directory"
    )
    model_file: str = Field(
        default="Hi_I_Vee.onnx",
        description="Wake word model filename"
    )
    
    @validator('chunk_size')
    def validate_chunk_size(cls, v, values):
        """Validate that chunk size is appropriate for sample rate"""
        if 'sample_rate' in values:
            # Ensure chunk is between 50ms and 200ms
            min_samples = int(values['sample_rate'] * 0.05)  # 50ms
            max_samples = int(values['sample_rate'] * 0.2)   # 200ms
            if not (min_samples <= v <= max_samples):
                raise ValueError(
                    f"Chunk size must be between {min_samples} and {max_samples} "
                    f"samples for {values['sample_rate']}Hz sample rate"
                )
        return v

class DetectionResult:
    """Data class for wake word detection results
    
    Attributes:
        wake_word_detected (bool): Whether a wake word was detected
        score (float): Confidence score of the detection (0.0 to 1.0)
        wake_word (Optional[str]): Name of the detected wake word model, if any
    """
    
    def __init__(
        self,
        wake_word_detected: bool = False,
        score: float = 0.0,
        wake_word: Optional[str] = None
    ):
        self.wake_word_detected = wake_word_detected
        self.score = score
        self.wake_word = wake_word
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format"""
        return {
            "wake_word_detected": self.wake_word_detected,
            "score": self.score,
            "wake_word": self.wake_word
        }

class CoreWakeWordDetector(AIService):
    """Core implementation of wake word detection using OpenWakeWord"""
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[Union[Dict[str, Any], WakeWordModelConfig]] = None
    ) -> None:
        """
        Initialize wake word detector.
        
        Args:
            name: Service name
            config: Service configuration
            model_config: Wake word model configuration
        """
        # Convert dict to WakeWordModelConfig if needed
        if isinstance(model_config, dict):
            model_config = WakeWordModelConfig(**model_config)
            
        super().__init__(name, config, model_config)
        self.audio_buffer = np.array([], dtype=np.int16)
        self.last_detection_time = 0
        
    def __del__(self):
        """Cleanup resources"""
        self.cleanup()
        
    def cleanup(self) -> None:
        """Clean up model resources"""
        if hasattr(self, 'model') and self.model is not None:
            # Clear prediction buffers
            if hasattr(self.model, 'prediction_buffer'):
                self.model.prediction_buffer.clear()
            self.model = None
            logger.debug("🧹 Cleaned up wake word detector resources")
        
    def get_default_model_config(self) -> WakeWordModelConfig:
        """Get default wake word model configuration"""
        return WakeWordModelConfig()
        
    def load_model(self) -> None:
        """Load wake word detection model"""
        try:
            # Cleanup any existing model
            self.cleanup()
            
            # Ensure models are downloaded
            logger.info("📥 Downloading wake word models...")
            openwakeword.utils.download_models()
            
            # Construct model path
            model_path = os.path.join(
                self.model_config.models_path,
                self.model_config.model_file
            )
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"❌ Model file not found: {model_path}")
            
            logger.info(f"🔄 Loading wake word model: {model_path}")
            self.model = Model(
                wakeword_models=[model_path],
                inference_framework="onnx"
            )
            
            logger.info("✅ Wake word model loaded successfully")
            logger.debug(f"📋 Available models: {list(self.model.prediction_buffer.keys())}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load wake word model: {e}")
            raise
        
    def preprocess_input(self, input_data: bytes) -> np.ndarray:
        """
        Preprocess audio input for the model.
        
        Args:
            input_data: Raw audio bytes
            
        Returns:
            np.ndarray: Preprocessed audio data
        """
        try:
            return np.frombuffer(input_data, dtype=np.int16)
        except Exception as e:
            logger.error(f"❌ Error preprocessing audio input: {e}")
            raise
        
    def predict(self, input_data: np.ndarray) -> List[DetectionResult]:
        """
        Process audio data for wake word detection.
        
        Args:
            input_data: Preprocessed audio data
            
        Returns:
            List[DetectionResult]: Detection results for each processed chunk
        """
        try:
            # Append to buffer
            self.audio_buffer = np.append(self.audio_buffer, input_data)
            logger.debug(f"🎵 Audio buffer: {len(self.audio_buffer)} samples")
            
            results = []
            current_time = time.time()
            
            # Process chunks
            while len(self.audio_buffer) >= self.model_config.chunk_size:
                # Extract chunk
                chunk = self.audio_buffer[:self.model_config.chunk_size]
                self.audio_buffer = self.audio_buffer[self.model_config.chunk_size:]
                
                logger.debug(f"🔍 Processing chunk: {len(chunk)} samples")
                
                # Get predictions
                prediction = self.model.predict(chunk)
                
                # Initialize result
                result = DetectionResult()
                
                # Check each model's predictions
                for mdl, scores in self.model.prediction_buffer.items():
                    if not scores:
                        continue
                        
                    current_score = float(scores[-1])
                    logger.debug(f"📊 Model {mdl}: {current_score:.3f}")
                    result.score = max(result.score, current_score)
                    
                    # Check for detection
                    if (current_score > self.model_config.detection_threshold and 
                        current_time - self.last_detection_time > self.model_config.cooldown_period):
                        result.wake_word_detected = True
                        result.wake_word = mdl
                        result.score = current_score
                        self.last_detection_time = current_time
                        logger.info(f"🎯 Wake word '{mdl}' detected! Score: {current_score:.3f}")
                        break
                
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in wake word detection: {e}")
            raise
        
    def postprocess_output(self, model_output: List[DetectionResult]) -> DetectionResult:
        """
        Postprocess model predictions.
        
        Args:
            model_output: List of detection results
            
        Returns:
            DetectionResult: Final detection result
        """
        # Return the latest result if available, otherwise return empty result
        return model_output[-1] if model_output else DetectionResult()
