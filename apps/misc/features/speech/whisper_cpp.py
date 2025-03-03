import packages
from pathlib import Path 
import subprocess
import time
import os
from loguru import logger
from typing import Optional, Dict, Any

PATH_REPO_WHISPER_CPP = f"{packages.ROOT_PATH}/apps/services/audio/speech_to_text/impl/assets/whisper.cpp"
MODEL_PATH = os.path.join(PATH_REPO_WHISPER_CPP, "models", "ggml-tiny.bin")

def transcribe(
    path_audio: str,
    simple_output: bool = True,
    word_timestamps: bool = False,
    enable_timestamps: bool = False,
    diarize: bool = False,
    language: str = "en",
    model_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transcribe audio using whisper.cpp.
    
    Args:
        path_audio: Path to audio file
        simple_output: If True, returns clean text only (default: True)
        word_timestamps: Enable word-level timestamps (default: False)
        enable_timestamps: Enable basic timestamps (default: False)
        diarize: Enable speaker diarization (default: False)
        language: Language code (default: "en")
        model_path: Optional custom model path
    
    Returns:
        Dict with keys:
        - success: bool
        - text: transcription or error message
        - execution_time: float
        - command: str (used command)
    """
    start_time = time.time()
    logger.info(f"Transcribing audio file: {path_audio}")
    
    # Validation checks
    if not os.path.exists(path_audio):
        return {
            "success": False,
            "text": f"Error: Audio file not found: {path_audio}",
            "execution_time": 0,
            "command": ""
        }
    
    model = model_path or MODEL_PATH
    if not os.path.exists(model):
        return {
            "success": False,
            "text": f"Error: Model file not found: {model}",
            "execution_time": 0,
            "command": ""
        }
    
    # Base command with optimized parameters
    command = [
        os.path.join(PATH_REPO_WHISPER_CPP, "build", "bin", "whisper-cli"),
        "-m", model,
        "-f", path_audio,
        "-l", language,
        "-np",           # No progress
    ]
    
    # Add timestamps settings
    if not enable_timestamps:
        command.append("-nt")
    
    # Add word timestamps if requested
    if word_timestamps:
        command.extend(["-ml", "1"])
    
    # Add speaker diarization if requested
    if diarize and "tdrz" in model:
        command.append("-tdrz")
    
    try:
        logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=PATH_REPO_WHISPER_CPP
        )
        
        output = result.stdout.strip()
        if not output:
            return {
                "success": False,
                "text": "Error: Empty transcription result",
                "execution_time": time.time() - start_time,
                "command": " ".join(command)
            }
            
        return {
            "success": True,
            "text": output,
            "execution_time": time.time() - start_time,
            "command": " ".join(command)
        }
    
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed with error code {e.returncode}: {e.stderr}"
        logger.error(error_msg)
        return {
            "success": False,
            "text": error_msg,
            "execution_time": time.time() - start_time,
            "command": " ".join(command)
        }
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "text": error_msg,
            "execution_time": time.time() - start_time,
            "command": " ".join(command)
        }

if __name__ == "__main__":
    # Example file path
    FILE_AUDIO = f"{packages.ROOT_PATH}/data/assets/examples/query.wav"

    # For clean output like terminal (default)
    result = transcribe(
        FILE_AUDIO,
        simple_output=True
    )

    # For detailed output with word timestamps
    # result = transcribe(
    #     FILE_AUDIO,
    #     simple_output=False,
    #     word_timestamps=True,
    #     enable_timestamps=True
    # )

    if result["success"]:
        print(f"\nresult: {result['text']}")
    else:
        print(f"\nError:\n{result['text']}")
        
    print(f"\nExecution time: {result['execution_time']:.2f} seconds")
    # Uncomment to see the command used
    # print(f"\nCommand used:\n{result['command']}")