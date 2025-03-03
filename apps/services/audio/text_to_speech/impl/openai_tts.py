"""
OpenAI Text-to-Speech implementation.
Provides integration with OpenAI's TTS API for high-quality speech synthesis.
"""

import os
from typing import Dict, Any, Optional, List, Literal
import aiohttp

from pydantic import Field, ConfigDict
from loguru import logger

import packages
from services.audio.text_to_speech.core import CoreTextToSpeech, TTSConfig, AudioConfig


class OpenAITTSConfig(TTSConfig):
    """Configuration for OpenAI TTS"""
    
    model_config = ConfigDict(protected_namespaces=())
    
    # Base AI model fields
    name: str = Field("openai_tts", description="Model name")
    version: str = Field("1.0.0", description="Model version")
    type: Literal["text", "image", "audio", "multimodal"] = Field(
        "audio", 
        description="Type of the model"
    )
    
    # OpenAI specific settings
    api_key: Optional[str] = Field(None, description="OpenAI API key (defaults to env var)")
    tts_model: str = Field("tts-1", description="OpenAI TTS model (tts-1 or tts-1-hd)")
    
    # Voice configuration
    voice_id: str = Field("alloy", description="Voice identifier")
    language: str = Field("en", description="Primary language code")
    
    # Performance settings
    speed: float = Field(1.0, ge=0.25, le=4.0, description="Speech speed multiplier")


class OpenAITTS(CoreTextToSpeech):
    """
    OpenAI-based text-to-speech implementation.
    
    Implements speech synthesis using OpenAI's TTS API with support for:
    - Multiple voices
    - Multiple audio formats
    - Speed control
    - Different quality models
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[OpenAITTSConfig] = None,
        audio_config: Optional[AudioConfig] = None
    ) -> None:
        """Initialize OpenAI TTS service"""
        super().__init__(name, config, model_config, audio_config)
        
        # Get API key from config or environment
        self._api_key = self.model_config.api_key or os.environ.get("OPENAI_API_KEY")
        if not self._api_key:
            logger.warning("No OpenAI API key provided. Please set OPENAI_API_KEY environment variable.")
    
    def get_default_model_config(self) -> OpenAITTSConfig:
        """Get default model configuration"""
        return OpenAITTSConfig()
        
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the service state"""
        base_info = super().get_service_info()
        base_info.update({
            "voice": self.model_config.voice_id,
            "language": self.model_config.language,
            "output_formats": self.supported_audio_formats,
            "tts_model": self.model_config.tts_model,
        })
        return base_info

    async def generate_audio(
        self,
        text: str,
        audio_config: Optional[AudioConfig] = None,
        voice_override: Optional[str] = None
    ) -> bytes:
        """Generate audio from text using OpenAI's TTS API

        Args:
            text: Input text to synthesize
            audio_config: Optional audio configuration settings
            voice_override: Optional voice ID to override default voice

        Returns:
            Generated audio data as bytes
        """
        try:
            # Use provided config or default
            config = audio_config or self.audio_config or AudioConfig()
            
            # Use voice override if provided
            voice = voice_override or self.model_config.voice_id
            
            # Map our format to OpenAI's format
            format_mapping = {
                "wav": "wav",
                "mp3": "mp3",
                "opus": "opus",
                "aac": "aac",
                "flac": "flac",
                "pcm": "pcm",
            }
            # Default to mp3 if format not supported
            response_format = format_mapping.get(config.format.lower(), "mp3")
            
            # Set speed from config or model_config
            speed = config.speed or self.model_config.speed
            
            # Check if API key is available
            if not self._api_key:
                raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
                
            # Call OpenAI API
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_config.tts_model,
                "input": text,
                "voice": voice,
                "response_format": response_format,
                "speed": speed
            }
            
            logger.debug(f"Calling OpenAI TTS API with voice: {voice}, format: {response_format}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(f"OpenAI API error: {response.status} - {error_text}")
                    
                    # Get audio data
                    audio_data = await response.read()
                    
                    logger.info(f"Generated {len(audio_data)} bytes of audio data")
                    return audio_data
                
        except Exception as e:
            logger.error(f"OpenAI TTS generation failed: {str(e)}")
            raise RuntimeError(f"Speech synthesis failed: {str(e)}")

    @property
    def supported_models(self) -> List[str]:
        """Get list of supported model names/identifiers"""
        return ["tts-1", "tts-1-hd"]
    
    @property
    def available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices with their properties"""
        return [
            {"id": "alloy", "name": "Alloy", "language": "en", "gender": "neutral"},
            {"id": "echo", "name": "Echo", "language": "en", "gender": "male"},
            {"id": "fable", "name": "Fable", "language": "en", "gender": "male"},
            {"id": "onyx", "name": "Onyx", "language": "en", "gender": "male"},
            {"id": "nova", "name": "Nova", "language": "en", "gender": "female"},
            {"id": "shimmer", "name": "Shimmer", "language": "en", "gender": "female"},
            {"id": "ash", "name": "Ash", "language": "en", "gender": "neutral"},
            {"id": "coral", "name": "Coral", "language": "en", "gender": "female"},
            {"id": "sage", "name": "Sage", "language": "en", "gender": "male"},
        ]

    @property
    def supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        # Based on Whisper's supported languages per the documentation
        return [
            "af", "ar", "hy", "az", "be", "bs", "bg", "ca", "zh", "hr", "cs", "da", 
            "nl", "en", "et", "fi", "fr", "gl", "de", "el", "he", "hi", "hu", "is", 
            "id", "it", "ja", "kn", "kk", "ko", "lv", "lt", "mk", "ms", "mr", "mi", 
            "ne", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", 
            "sv", "tl", "ta", "th", "tr", "uk", "ur", "vi", "cy"
        ]

    @property
    def supported_audio_formats(self) -> List[str]:
        """Get list of supported output audio formats"""
        return ["mp3", "opus", "aac", "flac", "wav", "pcm"]

    async def preprocess_input(self, input_text: str) -> str:
        """Preprocess input text"""
        # Normalize text and ensure it doesn't exceed OpenAI's character limit
        processed_text = input_text.strip()
        if len(processed_text) > 4096:
            logger.warning(f"Text exceeds OpenAI's character limit (4096). Truncating...")
            processed_text = processed_text[:4096]
        return processed_text


if __name__ == "__main__":
    # Example usage
    config = OpenAITTSConfig()
    
    service = OpenAITTS(
        name="OpenAITTS",
        model_config=config,
        audio_config=AudioConfig(format="mp3")
    )
    
    async def test():
        try:
            audio_data = await service.synthesize_text(
                "Hello! This is a test of the OpenAI text-to-speech system."
            )
            print(f"Generated {len(audio_data)} bytes of audio")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    import asyncio
    asyncio.run(test())
