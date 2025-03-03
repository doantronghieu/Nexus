"""
Audio preprocessing utilities for speech-to-text services.
Provides functions for converting various audio formats to WAV.
"""

import os
import tempfile
import asyncio
import shutil
from typing import Optional, Tuple
from pathlib import Path
import subprocess
from loguru import logger

SUPPORTED_INPUT_FORMATS = {
    'mp3', 'wav', 'm4a', 'ogg', 'flac', 'aac',
    'wma', 'aiff', 'opus', 'webm'
}

# Standard audio parameters
SAMPLE_RATE = 16000
CHANNELS = 1
BIT_DEPTH = 16

async def convert_to_wav(
    audio_data: bytes,
    input_format: Optional[str] = None,
    sample_rate: int = SAMPLE_RATE,
    channels: int = CHANNELS
) -> Tuple[bytes, float]:
    """
    Convert audio data to WAV format with specific parameters
    
    Args:
        audio_data: Input audio data as bytes
        input_format: Optional input format (e.g., 'mp3', 'ogg')
        sample_rate: Target sample rate in Hz
        channels: Number of audio channels
        
    Returns:
        Tuple[bytes, float]: WAV audio data and duration in seconds
        
    Raises:
        ValueError: If conversion fails
    """
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create input file with correct extension
            input_path = os.path.join(temp_dir, f"input.{input_format or 'tmp'}")
            output_path = os.path.join(temp_dir, "output.wav")
            
            # Write input file
            with open(input_path, 'wb') as f:
                f.write(audio_data)
            
            # Build ffmpeg command
            command = [
                'ffmpeg',
                '-i', input_path,
                '-ar', str(sample_rate),    # Sample rate
                '-ac', str(channels),       # Channels
                '-acodec', 'pcm_s16le',    # 16-bit PCM
                '-y',                       # Overwrite output
                output_path
            ]
            
            # Run conversion
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise ValueError(f"FFmpeg conversion failed: {stderr.decode()}")
            
            # Get duration using ffprobe
            duration = await get_audio_duration(output_path)
            
            # Read converted file
            with open(output_path, 'rb') as f:
                wav_data = f.read()
            
            return wav_data, duration
            
    except Exception as e:
        logger.error(f"Audio conversion failed: {str(e)}")
        raise ValueError(f"Audio conversion failed: {str(e)}")

async def get_audio_duration(file_path: str) -> float:
    """
    Get audio file duration using ffprobe
    
    Args:
        file_path: Path to audio file
        
    Returns:
        float: Duration in seconds
    """
    try:
        command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise ValueError(f"FFprobe failed: {stderr.decode()}")
        
        return float(stdout.decode().strip())
        
    except Exception as e:
        logger.error(f"Failed to get audio duration: {str(e)}")
        return 0.0

def check_ffmpeg() -> bool:
    """Check if ffmpeg is installed and available"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_format_from_content(audio_data: bytes) -> Optional[str]:
    """
    Try to determine audio format from file content
    
    Args:
        audio_data: Audio file content as bytes
        
    Returns:
        Optional[str]: Detected format or None
    """
    # Common audio file signatures
    signatures = {
        b'ID3': 'mp3',
        b'RIFF': 'wav',
        b'OggS': 'ogg',
        b'fLaC': 'flac',
        b'FORM': 'aiff'
    }
    
    # Check file signatures
    for sig, fmt in signatures.items():
        if audio_data.startswith(sig):
            return fmt
            
    return None