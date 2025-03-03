"""
OpenAI Whisper implementation of speech-to-text service.
Provides integration with OpenAI's Whisper API for cloud-based transcription.
"""
import packages
import os
import tempfile
from typing import Dict, Any, Optional, List, Union
import numpy as np
from loguru import logger
from pydantic import Field
import soundfile as sf
from openai import OpenAI

from services.audio.speech_to_text.core import CoreSpeechToText, STTConfig

class OpenAIWhisperConfig(STTConfig):
    """Configuration for OpenAI Whisper service"""
    
    api_key: str = Field(
        "",
        description="OpenAI API key (will use OPENAI_API_KEY env var if not provided)"
    )
    model: str = Field(
        "whisper-1",
        description="OpenAI Whisper model to use"
    )
    response_format: str = Field(
        "json",
        description="Response format (json, text, srt, verbose_json, vtt)"
    )
    temperature: float = Field(
        0.0,
        description="Sampling temperature (0-1)"
    )
    timestamp_granularities: Optional[List[str]] = Field(
        None,
        description="Timestamp granularities (word, segment)"
    )
    prompt: Optional[str] = Field(
        None,
        description="Optional text to guide the model's style or continue a previous segment"
    )

class OpenAIWhisperService(CoreSpeechToText):
    """
    Speech-to-text service using OpenAI's Whisper API.
    Provides cloud-based transcription via OpenAI's API.
    """
    
    def __init__(
        self,
        name: str = "openai_whisper",
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[OpenAIWhisperConfig] = None
    ) -> None:
        """Initialize OpenAI Whisper service"""
        super().__init__(name, config, model_config)
        
        # Initialize client
        self.client = None

    def initialize(self) -> None:
        """Initialize the service"""
        # Check for API key
        api_key = self.model_config.api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("No OpenAI API key provided. Please set OPENAI_API_KEY environment variable or provide it in the config.")
        else:
            self.client = OpenAI(api_key=api_key)
        
        logger.info(f"Initialized {self.name} service")

    def get_default_model_config(self) -> OpenAIWhisperConfig:
        """Get default OpenAI Whisper configuration"""
        return OpenAIWhisperConfig()

    def validate_audio(self, audio: Union[bytes, np.ndarray, str]) -> bool:
        """
        Validate audio input
        
        Args:
            audio: Audio data as bytes, numpy array, or file path
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if isinstance(audio, str):
                # Validate file path
                if not os.path.exists(audio):
                    logger.error(f"Audio file not found: {audio}")
                    return False
                    
                # Check extension - OpenAI supports more formats than whisper.cpp
                ext = os.path.splitext(audio)[1].lower().lstrip('.')
                if ext not in ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm', 'flac', 'ogg']:
                    logger.error(f"Unsupported audio format: {ext}")
                    return False
                    
            elif isinstance(audio, (bytes, np.ndarray)):
                # Basic validation for binary/array data
                if len(audio) == 0:
                    logger.error("Empty audio data")
                    return False
                    
            else:
                logger.error(f"Unsupported audio type: {type(audio)}")
                return False
                
            # Check client is initialized
            if not self.client:
                logger.error("OpenAI client not initialized, API key may be missing")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Audio validation error: {str(e)}")
            return False

    def transcribe(
        self,
        audio: Union[bytes, np.ndarray, str],
        language: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Transcribe audio to text using OpenAI's Whisper API
        
        Args:
            audio: Audio data or file path
            language: Optional language override
            **kwargs: Additional parameters
            
        Returns:
            str: Transcribed text
            
        Raises:
            ValueError: If audio is invalid
            RuntimeError: If transcription fails
        """
        if not self.validate_audio(audio):
            raise ValueError("Invalid audio input")
            
        try:
            # Handle audio input
            if isinstance(audio, (bytes, np.ndarray)):
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    if isinstance(audio, bytes):
                        temp_file.write(audio)
                    else:
                        sf.write(temp_file.name, audio, self.model_config.sample_rate)
                    path_audio = temp_file.name
            else:
                path_audio = audio
            
            # Prepare API parameters
            params = {
                "model": self.model_config.model,
                "response_format": self.model_config.response_format,
                "temperature": self.model_config.temperature
            }
            
            # Add optional parameters
            if language:
                params["language"] = language
                
            if self.model_config.prompt:
                params["prompt"] = self.model_config.prompt
                
            # Add timestamp granularities if specified and using verbose_json
            if self.model_config.timestamp_granularities and self.model_config.response_format == "verbose_json":
                params["timestamp_granularities"] = self.model_config.timestamp_granularities
                
            # Add any additional kwargs
            params.update({k: v for k, v in kwargs.items() if v is not None})
            
            # Open file and send request
            with open(path_audio, "rb") as audio_file:
                # Make API call
                transcription = self.client.audio.transcriptions.create(
                    file=audio_file,
                    **params
                )
            
            # Extract text based on response format
            if self.model_config.response_format in ["json", "verbose_json"]:
                return transcription.text
            else:
                return str(transcription)
                
        except Exception as e:
            error_msg = f"Transcription error: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
            
        finally:
            # Cleanup temp file if created
            if isinstance(audio, (bytes, np.ndarray)) and 'path_audio' in locals() and os.path.exists(path_audio):
                try:
                    os.remove(path_audio)
                except Exception as e:
                    logger.error(f"Error removing temp file: {str(e)}")

    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        # From the OpenAI Whisper documentation (ISO-639-1 codes)
        return [
            "af", "ar", "hy", "az", "be", "bs", "bg", "ca", "zh", "hr", 
            "cs", "da", "nl", "en", "et", "fi", "fr", "gl", "de", "el", 
            "he", "hi", "hu", "is", "id", "it", "ja", "kn", "kk", "ko", 
            "lv", "lt", "mk", "ms", "mr", "mi", "ne", "no", "fa", "pl", 
            "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "tl", 
            "ta", "th", "tr", "uk", "ur", "vi", "cy"
        ]

    def get_service_info(self) -> Dict[str, Any]:
        """Get service information"""
        info = super().get_service_info()
        info.update({
            "model": self.model_config.model,
            "response_format": self.model_config.response_format,
            "temperature": self.model_config.temperature,
            "timestamp_granularities": self.model_config.timestamp_granularities,
            "api_provider": "OpenAI Cloud API"
        })
        return info

def main():
    """Test the OpenAI Whisper service implementation"""
    try:
        # Initialize service
        service = OpenAIWhisperService(
            name="openai_whisper_test",
            model_config=OpenAIWhisperConfig(
                response_format="text"
            )
        )
        
        # Example file path - replace with an actual test file
        import packages
        file_audio = f"{packages.ROOT_PATH}/data/assets/examples/query.wav"
        
        # Initialize service
        service.initialize()
        
        # Test transcription
        logger.info(f"Transcribing: {file_audio}")
        result = service.transcribe(file_audio)
        logger.info(f"\nTranscription result:\n{result}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        
    finally:
        if 'service' in locals():
            service.shutdown()

if __name__ == "__main__":
    main()
