
"""
Piper Text-to-Speech implementation.
Provides integration with the Piper CLI tool for high-quality speech synthesis.
"""

import os
import subprocess
from typing import Dict, Any, Optional, Union, List, Literal
from pathlib import Path
import asyncio

from pydantic import Field, ConfigDict
from loguru import logger

import packages
from services.audio.text_to_speech.core import CoreTextToSpeech, TTSConfig, AudioConfig


PATH_ASSETS = f"{packages.APP_PATH}/services/audio/text_to_speech/impl/assets/piper"


class PiperConfig(TTSConfig):
    """Configuration for Piper TTS"""
    
    model_config = ConfigDict(protected_namespaces=())
    
    # Base AI model fields
    name: str = Field("piper", description="Model name")
    version: str = Field("1.0.0", description="Model version")
    type: Literal["text", "image", "audio", "multimodal"] = Field(
        "audio", 
        description="Type of the model"
    )
    
    # Paths
    tts_model_path: str = Field(
        f"{PATH_ASSETS}/models/en_US-ryan-high.onnx",
        description="Path to Piper model file"
    )
    data_dir: str = Field(
        f"{PATH_ASSETS}/data",
        description="Path to Piper data directory"
    )
    output_dir: str = Field(
        f"{PATH_ASSETS}/outputs",
        description="Directory for output files"
    )
    download_dir: str = Field(
        f"{PATH_ASSETS}/download",
        description="Directory for downloaded files"
    )
    
    # Voice settings
    voice_id: str = Field("ryan", description="Voice identifier")
    language: str = Field("en-US", description="Voice language")
    
    # Performance settings
    use_cuda: bool = Field(False, description="Use CUDA for inference")
    max_chunk_size: int = Field(1024, description="Maximum audio chunk size")

class PiperTTS(CoreTextToSpeech):
    """
    Piper-based text-to-speech implementation.
    
    Implements speech synthesis using the Piper CLI tool with support for:
    - Multiple voices and languages
    - CUDA acceleration
    - Custom model paths
    - Audio format conversion
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        model_config: Optional[PiperConfig] = None,
        audio_config: Optional[AudioConfig] = None
    ) -> None:
        """Initialize Piper TTS service"""
        super().__init__(name, config, model_config, audio_config)
        
        # Initialize paths
        self.ensure_directories()
        
        # Available models/voices cache
        self._available_models = []
        self._model_info = {}
        
    def get_default_model_config(self) -> PiperConfig:
        """Get default model configuration"""
        return PiperConfig()
        
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the service state"""
        base_info = super().get_service_info()
        base_info.update({
            "voice": self.model_config.voice_id,
            "language": self.model_config.language,
            "output_formats": self.supported_audio_formats,
        })
        return base_info

    def _validate_config(self) -> None:
        pass
        # """Validate service configuration"""
        # try:
        #     # Check if Piper is installed
        #     result = subprocess.run(['piper', '--version'], capture_output=True, text=True)
        #     if result.returncode != 0:
        #         raise ValueError("Piper not found. Please install Piper CLI tool.")
            
        #     # Validate paths
        #     if not os.path.exists(self.model_config.tts_model_path):
        #         raise ValueError(f"Model file not found: {self.model_config.tts_model_path}")
            
        #     if not os.path.exists(self.model_config.data_dir):
        #         raise ValueError(f"Data directory not found: {self.model_config.data_dir}")
            
        # except Exception as e:
        #     raise ValueError(f"Configuration validation failed: {str(e)}")

    def ensure_directories(self) -> None:
        """Ensure required directories exist"""
        os.makedirs(self.model_config.output_dir, exist_ok=True)
        os.makedirs(self.model_config.download_dir, exist_ok=True)
        os.makedirs(self.model_config.data_dir, exist_ok=True)

    async def generate_audio(
        self,
        text: str,
        audio_config: Optional[AudioConfig] = None,
        voice_override: Optional[str] = None
    ) -> bytes:
        """Generate audio from text using Piper

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
            
            # Prepare output path with unique hash
            output_path = os.path.join(
                self.model_config.output_dir,
                f"output_{hash(text)}_{hash(str(config))}.wav"
            )
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Build command using the working implementation approach
            command = [
                'piper',
                '--model', os.path.join(self.model_config.tts_model_path),
                '--data-dir', os.path.join(self.model_config.data_dir),
                '--download-dir', os.path.join(self.model_config.download_dir),
                '--output_file', output_path
            ]
            
            # Add config options
            if config.sample_rate:
                command.extend(['--sample-rate', str(config.sample_rate)])
            if config.speed != 1.0:
                command.extend(['--speed', str(config.speed)])
            
            if self.model_config.use_cuda:
                command.append('--cuda')

            # Run piper command
            try:
                process = await asyncio.create_subprocess_exec(
                    *command,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate(text.encode())
                
                if process.returncode != 0:
                    raise RuntimeError(f"Piper failed: {stderr.decode()}")
                
                # Read generated audio
                with open(output_path, 'rb') as f:
                    audio_data = f.read()
                
                # Cleanup
                os.remove(output_path)
                
                return audio_data
                
            except Exception as e:
                logger.error(f"Piper command failed: {str(e)}")
                raise RuntimeError(f"Speech synthesis failed: {str(e)}")
                
        except Exception as e:
            logger.error(f"Audio generation failed: {str(e)}")
            raise RuntimeError(f"Speech synthesis failed: {str(e)}")

    @property
    def supported_models(self) -> List[str]:
        """Get list of supported model names/identifiers"""
        return ["en_US-ryan-high"]  # Add more as needed
    
    @property
    def available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices with their properties"""
        return [{
            "id": "ryan",
            "name": "Ryan",
            "language": "en-US",
            "gender": "male",
        }]  # Add more as needed

    @property
    def supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return ["en-US"]  # Add more as needed

    @property
    def supported_audio_formats(self) -> List[str]:
        """Get list of supported output audio formats"""
        return ["wav"]  # Add more as needed

    async def preprocess_input(self, input_text: str) -> str:
        """Preprocess input text"""
        # Add any text preprocessing here
        return input_text.strip()

    async def postprocess_output(self, audio_data: bytes) -> bytes:
        """Postprocess generated audio data"""
        return audio_data  # Add any audio post-processing here

if __name__ == "__main__":
    # Example usage
    config = PiperConfig()
    
    service = PiperTTS(
        name="PiperTTS",
        model_config=config,
        audio_config=AudioConfig()
    )
    
    async def test():
        try:
            service.initialize()
            audio_data = await service.synthesize_text(
                "Hello! This is a test of the Piper text-to-speech system."
            )
            print(f"Generated {len(audio_data)} bytes of audio")
        finally:
            service.shutdown()
    
    import asyncio
    asyncio.run(test())