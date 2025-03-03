"""
Core abstract base class for keyword spotting services.
Provides domain-specific abstractions and interfaces for implementing
various keyword spotting models.
"""

from abc import abstractmethod
from typing import Dict, Any, Optional, List, Union, Tuple, AsyncIterator
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

import numpy as np
from pydantic import BaseModel, Field, validator
from loguru import logger

import packages
from services.bases.ai import AIService, AIModelConfig

class AudioFormat(str, Enum):
    """Supported audio input formats"""
    WAV = "wav"
    RAW = "raw"
    FLAC = "flac"
    MP3 = "mp3"

class FeatureType(str, Enum):
    """Supported feature extraction types"""
    MFCC = "mfcc"
    MEL_SPECTROGRAM = "mel_spectrogram"
    SPECTROGRAM = "spectrogram"
    FILTERBANK = "filterbank"
    RAW_AUDIO = "raw_audio"

@dataclass
class DetectionResult:
    """Container for keyword detection results"""
    keyword: str
    confidence: float
    start_time: float
    end_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class KeywordSpotterConfig(AIModelConfig):
    """Configuration for keyword spotting models"""
    # Audio parameters
    sample_rate: int = Field(16000, ge=8000, le=48000, description="Audio sample rate in Hz")
    num_channels: int = Field(1, ge=1, le=2, description="Number of audio channels")
    audio_duration: float = Field(1.0, gt=0, description="Duration of audio chunks in seconds")
    
    # Feature extraction
    feature_type: FeatureType = Field(FeatureType.MFCC, description="Type of audio features to extract")
    window_size_ms: float = Field(25.0, gt=0, description="Window size in milliseconds")
    hop_length_ms: float = Field(10.0, gt=0, description="Hop length in milliseconds")
    num_features: int = Field(40, gt=0, description="Number of features to extract")
    
    # Detection parameters
    detection_threshold: float = Field(0.5, ge=0, le=1, description="Detection confidence threshold")
    smoothing_window: int = Field(1, ge=1, description="Window size for detection smoothing")
    min_duration: float = Field(0.25, ge=0, description="Minimum keyword duration in seconds")
    
    # Processing
    stream_buffer_size: int = Field(4096, gt=0, description="Buffer size for streaming audio")
    overlap_ratio: float = Field(0.5, ge=0, le=1, description="Overlap ratio between processing windows")

    @validator("hop_length_ms")
    def validate_hop_length(cls, v, values):
        """Validate that hop length is less than window size"""
        if "window_size_ms" in values and v > values["window_size_ms"]:
            raise ValueError("Hop length must be less than or equal to window size")
        return v

    class Config:
        arbitrary_types_allowed = True

class KeywordSpottingError(Exception):
    """Base exception class for keyword spotting errors"""
    pass

class AudioProcessingError(KeywordSpottingError):
    """Raised when audio processing fails"""
    pass

class ModelStateError(KeywordSpottingError):
    """Raised when model is in invalid state"""
    pass

class InvalidConfigError(KeywordSpottingError):
    """Raised when configuration is invalid"""
    pass

class CoreKeywordSpotter(AIService):
    """
    Abstract base class for keyword spotting services.
    
    Implements common functionality and defines interface for keyword spotting models:
    - Audio preprocessing and feature extraction
    - Keyword detection and confidence scoring
    - Vocabulary management
    - Real-time streaming support
    
    Args:
        name: Service name
        config: Service configuration
        model_config: Keyword spotter specific configuration
        
    Attributes:
        keywords (List[str]): List of current detection keywords
        _feature_extractor: Feature extraction implementation
        _detection_threshold (float): Current detection threshold
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[KeywordSpotterConfig] = None
    ) -> None:
        """Initialize the keyword spotter service"""
        super().__init__(name, config, model_config)
        self.keywords: List[str] = []
        self._feature_extractor = None
        self._detection_threshold = self.model_config.detection_threshold
        self._is_streaming = False

    def get_default_model_config(self) -> KeywordSpotterConfig:
        """Get default model configuration"""
        return KeywordSpotterConfig()

    @abstractmethod
    async def detect_keywords(
        self,
        audio: np.ndarray,
        sample_rate: Optional[int] = None
    ) -> List[DetectionResult]:
        """
        Detect keywords in audio data.
        
        Args:
            audio: Audio samples as numpy array
            sample_rate: Sample rate of audio (if different from config)
            
        Returns:
            List of DetectionResult objects for detected keywords
            
        Raises:
            AudioProcessingError: If audio processing fails
            ModelStateError: If model is not properly initialized
        """
        pass

    @abstractmethod
    async def stream_detect_keywords(
        self,
        audio_stream: Any,
        sample_rate: Optional[int] = None
    ) -> AsyncIterator[DetectionResult]:
        """
        Detect keywords in streaming audio data.
        
        Args:
            audio_stream: Audio stream object
            sample_rate: Sample rate of audio stream
            
        Yields:
            DetectionResult objects as keywords are detected
            
        Raises:
            AudioProcessingError: If audio processing fails
            ModelStateError: If model is not properly initialized
        """
        pass

    @abstractmethod
    async def extract_features(
        self,
        audio: np.ndarray,
        sample_rate: Optional[int] = None
    ) -> np.ndarray:
        """
        Extract features from audio data.
        
        Args:
            audio: Audio samples as numpy array
            sample_rate: Sample rate of audio
            
        Returns:
            Feature matrix as numpy array
            
        Raises:
            AudioProcessingError: If feature extraction fails
        """
        pass

    @abstractmethod
    async def get_detection_scores(
        self,
        features: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """
        Get raw detection scores for all keywords.
        
        Args:
            features: Audio features as numpy array
            
        Returns:
            Dictionary mapping keywords to score arrays
            
        Raises:
            ModelStateError: If model is not properly initialized
        """
        pass

    @abstractmethod
    def add_keyword(
        self,
        keyword: str,
        samples: Optional[List[np.ndarray]] = None
    ) -> None:
        """
        Add a new keyword to the detection vocabulary.
        
        Args:
            keyword: Keyword string to add
            samples: Optional list of audio samples for the keyword
            
        Raises:
            ValueError: If keyword already exists
            ModelStateError: If model doesn't support dynamic vocabulary
        """
        if keyword in self.keywords:
            raise ValueError(f"Keyword '{keyword}' already exists")
        self.keywords.append(keyword)

    @abstractmethod
    def remove_keyword(self, keyword: str) -> None:
        """
        Remove a keyword from the detection vocabulary.
        
        Args:
            keyword: Keyword string to remove
            
        Raises:
            ValueError: If keyword doesn't exist
            ModelStateError: If model doesn't support dynamic vocabulary
        """
        if keyword not in self.keywords:
            raise ValueError(f"Keyword '{keyword}' does not exist")
        self.keywords.remove(keyword)

    def set_threshold(self, threshold: float) -> None:
        """
        Set the detection confidence threshold.
        
        Args:
            threshold: New threshold value between 0 and 1
            
        Raises:
            ValueError: If threshold is invalid
        """
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")
        self._detection_threshold = threshold
        logger.info(f"Detection threshold set to {threshold}")

    def get_keywords(self) -> List[str]:
        """Get list of current detection keywords"""
        return self.keywords.copy()

    async def normalize_audio(
        self,
        audio: np.ndarray,
        sample_rate: Optional[int] = None
    ) -> Tuple[np.ndarray, int]:
        """
        Normalize audio data to expected format.
        
        Args:
            audio: Input audio samples
            sample_rate: Sample rate of input audio
            
        Returns:
            Tuple of (normalized_audio, sample_rate)
            
        Raises:
            AudioProcessingError: If normalization fails
        """
        try:
            if sample_rate is None:
                sample_rate = self.model_config.sample_rate

            # Validate input
            self._validate_audio_input(audio, sample_rate)
                
            # Ensure correct number of channels (convert to mono if needed)
            if len(audio.shape) > 1 and audio.shape[1] > 1:
                audio = np.mean(audio, axis=1)
                logger.debug("Converted multi-channel audio to mono")
                
            # Resample if needed
            if sample_rate != self.model_config.sample_rate:
                # Note: Actual resampling implementation would go here
                # For now, just log a warning
                logger.warning("Audio resampling not implemented yet")
                
            # Normalize amplitude
            if np.abs(audio).max() > 1.0:
                audio = audio / np.abs(audio).max()
                logger.debug("Normalized audio amplitude")
                
            return audio, self.model_config.sample_rate
            
        except Exception as e:
            raise AudioProcessingError(f"Failed to normalize audio: {str(e)}")

    def _validate_audio_input(
        self,
        audio: np.ndarray,
        sample_rate: Optional[int] = None
    ) -> None:
        """
        Validate audio input data.
        
        Args:
            audio: Input audio samples
            sample_rate: Sample rate of input
            
        Raises:
            ValueError: If audio data is invalid
        """
        if not isinstance(audio, np.ndarray):
            raise ValueError("Audio input must be a numpy array")
            
        if audio.size == 0:
            raise ValueError("Audio input is empty")
            
        if sample_rate is not None and sample_rate < 1:
            raise ValueError("Sample rate must be positive")
            
        if len(audio.shape) > 2:
            raise ValueError("Audio input has too many dimensions")
            
        if np.isnan(audio).any() or np.isinf(audio).any():
            raise ValueError("Audio input contains invalid values (NaN or Inf)")

    def _validate_config(self) -> None:
        """Validate service configuration"""
        try:
            # Ensure model config is the correct type
            if not isinstance(self.model_config, KeywordSpotterConfig):
                raise InvalidConfigError("Invalid model configuration type")
                
            # Basic validation of key parameters
            if self.model_config.sample_rate < 1:
                raise InvalidConfigError("Sample rate must be positive")
                
            if self.model_config.num_channels not in [1, 2]:
                raise InvalidConfigError("Only mono or stereo audio is supported")
                
            if self.model_config.audio_duration <= 0:
                raise InvalidConfigError("Audio duration must be positive")
                
            # Add any additional validation specific to your model
                
        except Exception as e:
            raise InvalidConfigError(f"Configuration validation failed: {str(e)}")

    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the service state"""
        return {
            "name": self.name,
            "initialized": self.is_initialized,
            "model_config": {
                "sample_rate": self.model_config.sample_rate,
                "feature_type": self.model_config.feature_type.value,
                "detection_threshold": self._detection_threshold,
            },
            "keywords": self.get_keywords(),
            "is_streaming": self._is_streaming
        }
