"""
Whisper.cpp implementation of speech-to-text service.
Provides integration with whisper.cpp for efficient CPU-based transcription.
"""

import os
import time
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import numpy as np
from loguru import logger
from pydantic import Field
import soundfile as sf

import packages
from services.audio.speech_to_text.core import CoreSpeechToText, STTConfig

# Constants from whisper.cpp
# Constants from whisper.cpp
PATH_REPO_WHISPER_CPP = os.path.normpath(f"{packages.ROOT_PATH}/apps/services/audio/speech_to_text/impl/assets/whisper.cpp")
MODEL_PATH = os.path.normpath(os.path.join(PATH_REPO_WHISPER_CPP, "models", "ggml-tiny.bin"))
WHISPER_CLI = os.path.normpath(os.path.join(PATH_REPO_WHISPER_CPP, "build", "bin", "whisper-cli")).replace("//", "/")

class WhisperConfig(STTConfig):
    """Configuration for Whisper.cpp service"""
    
    model_path: str = Field(
        MODEL_PATH,
        description="Path to whisper.cpp model file"
    )
    word_timestamps: bool = Field(False, description="Enable word-level timestamps")
    enable_timestamps: bool = Field(False, description="Enable basic timestamps")
    diarize: bool = Field(False, description="Enable speaker diarization")

class WhisperCPPService(CoreSpeechToText):
    """
    Speech-to-text service using whisper.cpp implementation.
    Provides efficient CPU-based transcription using the whisper.cpp library.
    """
    
    def __init__(
        self,
        name: str = "whisper_cpp",
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[WhisperConfig] = None
    ) -> None:
        """Initialize WhisperCPP service"""
        super().__init__(name, config, model_config)
        
        # Set paths
        self.executable_path = WHISPER_CLI
        self.whisper_dir = os.path.dirname(WHISPER_CLI)
        
        # Ensure executable exists
        if not os.path.exists(self.executable_path):
            raise RuntimeError(
                f"whisper-cli executable not found at {self.executable_path}. "
                "Please build whisper.cpp first."
            )

    def get_default_model_config(self) -> WhisperConfig:
        """Get default WhisperCPP configuration"""
        return WhisperConfig()

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
                    
                # Basic extension check
                ext = Path(audio).suffix.lower()
                if ext not in ['.wav']:
                    logger.error(f"Unsupported audio format: {ext}. Only WAV files are supported.")
                    return False
                    
            elif isinstance(audio, (bytes, np.ndarray)):
                # Basic validation for binary/array data
                if len(audio) == 0:
                    logger.error("Empty audio data")
                    return False
                    
            else:
                logger.error(f"Unsupported audio type: {type(audio)}")
                return False
            
            # Validate model file exists
            if not os.path.exists(self.model_config.model_path):
                logger.error(f"Model file not found: {self.model_config.model_path}")
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
        Transcribe audio to text
        
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
            
            # Build command
            command = [
                os.path.normpath(self.executable_path).replace("//", "/"),
                "-m", os.path.normpath(self.model_config.model_path).replace("//", "/"),
                "-f", os.path.normpath(path_audio),
                "-l", language or self.model_config.language,
                "-np",  # No progress
            ]
            
            # Add optional parameters
            if not self.model_config.enable_timestamps:
                command.append("-nt")  # No timestamps
            if self.model_config.word_timestamps:
                command.extend(["-ml", "1"])  # Word-level timestamps
            if self.model_config.diarize and "tdrz" in self.model_config.model_path:
                command.append("-tdrz")

            # Run transcription
            logger.debug(f"Running command: {' '.join(command)}")
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.whisper_dir
            )
            
            output = result.stdout.strip()
            if not output:
                raise RuntimeError("Empty transcription result")
                
            return output
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Transcription failed: {e.stderr}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
            
        except Exception as e:
            error_msg = f"Transcription error: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
            
        finally:
            # Cleanup temp file if created
            if isinstance(audio, (bytes, np.ndarray)) and os.path.exists(path_audio):
                try:
                    os.remove(path_audio)
                except Exception as e:
                    logger.error(f"Error removing temp file: {str(e)}")

    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        # Core supported languages in whisper.cpp
        # This is a simplified list - models may support different languages
        return [
            "en",  # English
            "zh",  # Chinese
            "de",  # German 
            "es",  # Spanish
            "ru",  # Russian
            "ko",  # Korean
            "fr",  # French
            "ja",  # Japanese
            "pt",  # Portuguese
            "tr",  # Turkish
            "pl",  # Polish
            "ca",  # Catalan
            "nl",  # Dutch
            "ar",  # Arabic
            "sv",  # Swedish
            "it",  # Italian
            "id",  # Indonesian
            "hi",  # Hindi
            "fi",  # Finnish
            "vi",  # Vietnamese
        ]

def main():
    """Test the WhisperCPP service implementation"""
    try:
        # Initialize service with timestamps disabled
        service = WhisperCPPService(
            name="whisper_test",
            model_config=WhisperConfig(
                word_timestamps=False,
                enable_timestamps=False
            )
        )
        
        # Example file path
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