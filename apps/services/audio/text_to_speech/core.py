"""
Abstract base class for Text-to-Speech services.
Provides domain-specific abstractions and interfaces for implementing
various text-to-speech engines.
"""

from abc import abstractmethod
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field

import packages
from services.bases.ai import AIService, AIModelConfig

class TTSConfig(AIModelConfig):
    """Configuration model for Text-to-Speech services"""
    
    # Audio configuration
    sample_rate: int = Field(22050, ge=8000, le=48000, description="Audio sample rate in Hz")
    audio_channels: int = Field(1, ge=1, le=2, description="Number of audio channels")
    bits_per_sample: int = Field(16, ge=8, le=32, description="Bits per audio sample")
    
    # Voice configuration
    language: str = Field("en", description="Primary language code (e.g., 'en', 'es')")
    voice_id: Optional[str] = Field(None, description="Identifier for specific voice")
    gender: Optional[str] = Field(None, description="Voice gender")
    
    # Generation parameters
    max_text_length: int = Field(1000, ge=1, description="Maximum input text length")
    
    class Config:
        extra = "allow"  # Allow additional fields in derived configs

class AudioConfig(BaseModel):
    """Configuration for audio output settings"""
    
    format: str = Field("wav", description="Output audio format")
    sample_rate: Optional[int] = Field(None, description="Override default sample rate")
    volume: float = Field(1.0, ge=0.0, le=2.0, description="Audio volume multiplier")
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Speech speed multiplier")
    pitch: float = Field(1.0, ge=0.5, le=2.0, description="Voice pitch multiplier")

    class Config:
        extra = "allow"  # Allow additional fields in derived configs

class CoreTextToSpeech(AIService):
    """
    Abstract base class for Text-to-Speech services.
    
    Implements common functionality and defines interface for TTS engines:
    - Text preprocessing and normalization
    - Audio generation and post-processing
    - Format conversion and configuration
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[TTSConfig] = None,
        audio_config: Optional[AudioConfig] = None
    ) -> None:
        """Initialize TTS service"""
        super().__init__(name, config, model_config)
        self.audio_config = audio_config or AudioConfig()

    def get_default_model_config(self) -> TTSConfig:
        """Get default TTS model configuration"""
        return TTSConfig()

    async def synthesize_text(
        self,
        text: str,
        audio_config: Optional[AudioConfig] = None,
        voice_override: Optional[str] = None
    ) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Input text to synthesize
            audio_config: Optional override for audio configuration
            voice_override: Optional voice ID to override default voice
            
        Returns:
            Audio data as bytes
            
        Raises:
            ValueError: If text exceeds maximum length
            RuntimeError: If synthesis fails
        """
        if len(text) > self.model_config.max_text_length:
            raise ValueError(f"Text length exceeds maximum of {self.model_config.max_text_length}")
            
        try:
            # Preprocess input
            text = await self.preprocess_input(text)
            
            # Generate audio with config and voice override
            audio_data = await self.generate_audio(
                text=text,
                audio_config=audio_config,
                voice_override=voice_override
            )
            
            # Post-process output
            audio_data = await self.postprocess_output(audio_data)
            
            return audio_data
                
        except Exception as e:
            raise RuntimeError(f"Speech synthesis failed: {str(e)}")

    @abstractmethod
    async def generate_audio(
        self,
        text: str,
        audio_config: Optional[AudioConfig] = None,
        voice_override: Optional[str] = None
    ) -> bytes:
        """
        Generate audio from text
        
        Args:
            text: Text to synthesize
            audio_config: Audio configuration settings
            voice_override: Optional voice ID to override default voice
            
        Returns:
            Generated audio data as bytes
            
        Raises:
            RuntimeError: If audio generation fails
        """
        raise NotImplementedError("Subclasses must implement generate_audio()")

    async def preprocess_input(self, input_text: str) -> str:
        """Preprocess input text before synthesis"""
        return input_text.strip()

    async def postprocess_output(self, audio_data: bytes) -> bytes:
        """Postprocess generated audio data"""
        return audio_data

    @property
    @abstractmethod
    def supported_models(self) -> List[str]:
        """Get list of supported model names/identifiers"""
        raise NotImplementedError("Subclasses must implement supported_models")
    
    @property
    @abstractmethod
    def available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices with their properties"""
        raise NotImplementedError("Subclasses must implement available_voices")

    @property
    @abstractmethod
    def supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        raise NotImplementedError("Subclasses must implement supported_languages")

    @property
    @abstractmethod
    def supported_audio_formats(self) -> List[str]:
        """Get list of supported output audio formats"""
        raise NotImplementedError("Subclasses must implement supported_audio_formats")

    async def predict(self, input_text: str) -> bytes:
        """
        Implementation of base predict method using text synthesis
        
        Args:
            input_text: Text to synthesize
            
        Returns:
            Generated audio data
        """
        return await self.synthesize_text(input_text)