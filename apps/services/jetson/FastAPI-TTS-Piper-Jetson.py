import os
import time
import wave
import tempfile
import logging
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
from piper import PiperVoice
from piper.download import ensure_voice_exists, find_voice, get_voices

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
CACHE_DIR = os.environ.get('PIPER_CACHE', './piper_cache')
DEFAULT_MODEL = 'en_US-ryan-high'
voice = None
voices_info = None

@app.on_event("startup")
async def startup_event():
    global voice, voices_info
    logger.info("Starting up the server")
    # Download voice info
    try:
        voices_info = get_voices(CACHE_DIR, update_voices=True)
        logger.info("Successfully downloaded Piper voice list")
    except Exception as error:
        logger.error(f"Failed to download Piper voice list: {error}")
        voices_info = get_voices(CACHE_DIR)
    
    # Resolve aliases for backwards compatibility
    aliases_info = {}
    for voice_info in voices_info.values():
        for voice_alias in voice_info.get("aliases", []):
            aliases_info[voice_alias] = {"_is_alias": True, **voice_info}
    voices_info.update(aliases_info)
    
    # Load default model
    logger.info(f"Loading default model: {DEFAULT_MODEL}")
    load_model(DEFAULT_MODEL)
    logger.info("Server startup complete")

def load_model(model_name):
    global voice, voices_info
    if not os.path.isfile(os.path.join(CACHE_DIR, model_name)):
        ensure_voice_exists(model_name, CACHE_DIR, CACHE_DIR, voices_info)
    model, config = find_voice(model_name, [CACHE_DIR])
    voice = PiperVoice.load(model, config_path=config, use_cuda=True)

@app.post("/tts")
async def text_to_speech(text: str = Form(...)):
    global voice
    logger.info(f"Received text-to-speech request")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            output_audio_path = temp_file.name
        
        logger.info(f"Temporary file will be created at: {output_audio_path}")

        logger.info("Starting text-to-speech conversion")
        tts_start = time.time()

        with wave.open(output_audio_path, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(22050)  # Default sample rate for Piper

            voice.synthesize(text, wav_file)

        tts_time = time.time() - tts_start
        logger.info(f"Text-to-speech conversion completed in {tts_time:.2f} seconds")

        return FileResponse(
            output_audio_path, 
            media_type="audio/wav", 
            filename="response.wav",
            background=BackgroundTask(lambda: os.unlink(output_audio_path))
        )

    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT_SVC_TTS_PIPER")))