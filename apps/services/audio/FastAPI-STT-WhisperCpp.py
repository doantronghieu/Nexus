import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from dotenv import load_dotenv
from pydub import AudioSegment

# Load environment variables
load_dotenv()

# Constants
WHISPER_CPP_PATH = "/app/assets/whisper.cpp"
MODEL_PATH = os.path.join(WHISPER_CPP_PATH, "models", "ggml-tiny-q5_1.bin")
UPLOAD_DIR = "/tmp/whisper_uploads"
PORT = int(os.getenv("PORT_SVC_STT_WHISPER_CPP", 8769))

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Configure logger
logger.add("logs/api.log", rotation="1 day")

app = FastAPI(
    title="Whisper.cpp STT API",
    description="Speech-to-Text API using Whisper.cpp",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_audio(input_file_path: str, output_file_path: Optional[str] = None) -> str:
    """
    Convert any audio file to WAV format with 16 kHz sample rate.
    """
    logger.info(f"Preprocessing audio file: {input_file_path}")
    logger.info(f"Input file size: {os.path.getsize(input_file_path)} bytes")

    if output_file_path is None:
        output_file_path = os.path.splitext(input_file_path)[0] + "_processed.wav"
    
    try:
        audio = AudioSegment.from_file(input_file_path)
        
        logger.info(f"Original audio: {audio.channels} channels, {audio.frame_rate} Hz, {audio.sample_width} bytes/sample")
        
        # Convert to mono if needed
        if audio.channels > 1:
            audio = audio.set_channels(1)
            logger.info("Converted to mono")
        
        # Set sample rate to 16kHz
        if audio.frame_rate != 16000:
            audio = audio.set_frame_rate(16000)
            logger.info("Set frame rate to 16000 Hz")
        
        # Set to 16-bit
        if audio.sample_width != 2:
            audio = audio.set_sample_width(2)
            logger.info("Set sample width to 16 bits")
        
        audio.export(output_file_path, format="wav")
        
        logger.info(f"Processed audio saved to: {output_file_path}")
        logger.info(f"Processed file size: {os.path.getsize(output_file_path)} bytes")
        
        return output_file_path
    except Exception as e:
        logger.error(f"Error preprocessing audio: {str(e)}")
        raise Exception(f"Audio preprocessing failed: {str(e)}")

def transcribe(path_audio: str) -> str:
    """
    Transcribe audio using whisper.cpp
    """
    logger.info(f"Transcribing audio file: {path_audio}")
    
    if not os.path.exists(path_audio):
        logger.error(f"Audio file does not exist: {path_audio}")
        return "Error: Audio file not found"
    
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model file does not exist: {MODEL_PATH}")
        return "Error: Model file not found"
    
    command = [
        os.path.join(WHISPER_CPP_PATH, "main"),
        "-m", MODEL_PATH,
        "-t", "11",
        "-p", "1",
        "-f", path_audio,
        "-bs", "1",
        "-bo", "1",
        "-nf",
        "-wt", "0.01",
        "-nt",
        "-ml", "1",
        "-et", "100",
        "-lpt", "0",
        "-mc", "0"
    ]
    
    try:
        logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True, 
            cwd=WHISPER_CPP_PATH
        )
        
        output = result.stdout.strip()
        if not output:
            logger.warning("Transcription output is empty")
            return "Error: Empty transcription result"
        return output
    
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred during transcription: {e}")
        logger.error(f"Error output: {e.stderr}")
        return f"Error: Transcription failed - {e.stderr}"
    except Exception as e:
        logger.error(f"Unexpected error during transcription: {str(e)}")
        return f"Error: Unexpected error - {str(e)}"

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={
        "status": "healthy",
        "service": "whisper.cpp STT",
        "model": "tiny-q5_1",
        "port": PORT
    })

@app.post("/transcribe/")
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    return_timing: Optional[bool] = False
):
    """
    Transcribe audio file endpoint with preprocessing support
    """
    temp_file_path = None
    processed_file_path = None
    
    try:
        start_time = time.time()
        
        # Save uploaded file
        temp_file_path = os.path.join(UPLOAD_DIR, audio_file.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        logger.info(f"Processing audio file: {audio_file.filename}")
        
        # Preprocess audio
        preprocessing_start = time.time()
        processed_file_path = preprocess_audio(temp_file_path)
        preprocessing_time = time.time() - preprocessing_start
        
        # Transcribe
        transcription_start = time.time()
        result = transcribe(processed_file_path)
        transcription_time = time.time() - transcription_start
        
        # Prepare response
        response = {
            "status": "error" if result.startswith("Error:") else "success",
            "filename": audio_file.filename,
            "transcription": result
        }
        
        if return_timing:
            response.update({
                "preprocessing_time": f"{preprocessing_time:.2f}s",
                "transcription_time": f"{transcription_time:.2f}s",
                "total_time": f"{time.time() - start_time:.2f}s"
            })
            
        if result.startswith("Error:"):
            return JSONResponse(content={"error": result}, status_code=400)
            
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    finally:
        # Clean up temporary files
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        if processed_file_path and os.path.exists(processed_file_path):
            os.unlink(processed_file_path)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on port {PORT}")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=PORT,
        log_level="info"
    )