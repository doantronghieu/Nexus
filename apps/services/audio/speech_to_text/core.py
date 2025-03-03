"""
Abstract base class for Speech-to-Text services.
Provides core functionality and interfaces for speech recognition implementations.
"""

from typing import Dict, Any, Optional, List, Union
from abc import abstractmethod
from pydantic import BaseModel, Field
import numpy as np

from services.bases.ai import AIService, AIModelConfig

class STTConfig(AIModelConfig):
    """Configuration model for speech-to-text services"""
    
    sample_rate: int = Field(16000, description="Audio sample rate in Hz")
    channels: int = Field(1, description="Number of audio channels")
    language: str = Field("en", description="Primary language code")
    max_duration: float = Field(30.0, description="Maximum audio duration in seconds")

class CoreSpeechToText(AIService):
    """
    Abstract base class for speech-to-text services.
    Extends AIService to provide domain-specific functionality for speech recognition.
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[STTConfig] = None
    ) -> None:
        """
        Initialize speech-to-text service
        
        Args:
            name: Service name
            config: Service configuration
            model_config: Model-specific configuration
        """
        super().__init__(name, config, model_config)

    def get_default_model_config(self) -> STTConfig:
        """Get default STT model configuration"""
        return STTConfig()

    @abstractmethod
    def validate_audio(self, audio: Union[bytes, np.ndarray]) -> bool:
        """
        Validate audio data format and parameters
        
        Args:
            audio: Raw audio data as bytes or numpy array
            
        Returns:
            bool: True if audio is valid, False otherwise
            
        Raises:
            ValueError: If audio format is invalid
        """
        pass

    @abstractmethod
    def transcribe(
        self,
        audio: Union[bytes, np.ndarray],
        language: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Transcribe audio to text
        
        Args:
            audio: Audio data as bytes or numpy array
            language: Language code (overrides default)
            **kwargs: Additional model-specific parameters
            
        Returns:
            str: Transcribed text
            
        Raises:
            ValueError: If audio is invalid
            RuntimeError: If transcription fails
        """
        pass

    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes
        
        Returns:
            List[str]: Supported language codes
        """
        pass

    def preprocess_input(self, audio: Union[bytes, np.ndarray]) -> np.ndarray:
        """
        Preprocess audio input. Override in child classes for specific preprocessing.
        
        Args:
            audio: Raw audio data
            
        Returns:
            np.ndarray: Preprocessed audio data
            
        Raises:
            ValueError: If audio format is invalid
        """
        if not self.validate_audio(audio):
            raise ValueError("Invalid audio format or parameters")
        return np.array(audio)

    def get_service_info(self) -> Dict[str, Any]:
        """Get service information including supported languages"""
        info = super().get_service_info()
        info.update({
            "supported_languages": self.get_supported_languages(),
            "audio_config": {
                "sample_rate": self.model_config.sample_rate,
                "channels": self.model_config.channels,
                "max_duration": self.model_config.max_duration
            }
        })
        return info