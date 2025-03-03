from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
from loguru import logger
import os
import time
from datetime import datetime
import numpy as np
import wave
from openai import OpenAI
from pydantic import BaseModel
from openwakeword.model import Model
import packages
from pathlib import Path
import base64
from abc import ABC, abstractmethod
from typing import Optional, Dict, Union

import openwakeword

openwakeword.utils.download_models()

@dataclass
class AppConfig:
    """Application configuration"""
    JUST_DO_WWD: bool = False  # Flag to only perform wake word detection

@dataclass
class AudioConfig:
    """Audio processing configuration"""
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 1280  # 80ms chunks at 16kHz
    CHUNK_DURATION_MS: float = CHUNK_SIZE / SAMPLE_RATE * 1000  # Duration of each chunk in ms

@dataclass
class WakeWordConfig:
    """Wake word detection configuration"""
    MODELS_PATH: str = f"{packages.APP_PATH}/assets/openWakeWord/models"
    DETECTION_THRESHOLD: float = 0.5  # Confidence threshold for wake word detection

@dataclass
class VoiceActivityConfig:
    """Voice activity detection configuration"""
    SILENCE_THRESHOLD: int = 500  # Amplitude threshold for silence detection
    SILENCE_DURATION: float = 2.0  # Duration of silence in seconds before processing
    
    @property
    def CHUNKS_FOR_SILENCE(self) -> int:
        """Calculate number of chunks needed for silence duration"""
        return int((self.SILENCE_DURATION * 1000) / AudioConfig.CHUNK_DURATION_MS)

@dataclass
class PathConfig:
    """Path configuration"""
    AUDIO_DIR: str = "audio_chunks"
    TTS_OUTPUT_DIR: str = "tts_outputs"

    def __post_init__(self):
        """Create necessary directories"""
        os.makedirs(self.AUDIO_DIR, exist_ok=True)
        os.makedirs(self.TTS_OUTPUT_DIR, exist_ok=True)

# Initialize configurations
app_config = AppConfig()
audio_config = AudioConfig()
wake_word_config = WakeWordConfig()
vad_config = VoiceActivityConfig()
path_config = PathConfig()

class BaseHandler(ABC):
    """Abstract base class for AI service handlers"""
    
    @abstractmethod
    def transcribeAudio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio file to text"""
        pass

    @abstractmethod
    def generateText(self, user_input: str) -> str:
        """Generate text response from user input"""
        pass

    @abstractmethod
    def textToSpeech(self, text: str) -> Optional[bytes]:
        """Convert text to speech"""
        pass

class OpenAIHandler(BaseHandler):
    """OpenAI implementation of BaseHandler"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful voice assistant. Keep your responses concise and natural, as they will be spoken out loud."}
        ]

    def transcribeAudio(self, audio_file_path: str) -> Optional[str]:
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcription.text
        except Exception as e:
            logger.error(f"Error in OpenAI transcription: {e}")
            return None

    def generateText(self, user_input: str) -> str:
        try:
            self.conversation_history.append({"role": "user", "content": user_input})
            
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history
            )
            
            response = completion.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
        except Exception as e:
            logger.error(f"Error in OpenAI text generation: {e}")
            return "I apologize, but I encountered an error processing your request."

    def textToSpeech(self, text: str) -> Optional[bytes]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            tts_file_path = os.path.join(path_config.TTS_OUTPUT_DIR, f"tts_{timestamp}.mp3")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            
            response.stream_to_file(tts_file_path)
            
            with open(tts_file_path, 'rb') as file:
                audio_data = base64.b64encode(file.read())
            
            os.remove(tts_file_path)
            return audio_data
        except Exception as e:
            logger.error(f"Error in OpenAI speech generation: {e}")
            return None

class Services:
    """Service manager class that uses a specific handler implementation"""
    
    def __init__(self, handler: BaseHandler):
        self.handler = handler

    def transcribeAudio(self, audio_file_path: str) -> Optional[str]:
        return self.handler.transcribeAudio(audio_file_path)

    def generateText(self, user_input: str) -> str:
        return self.handler.generateText(user_input)

    def textToSpeech(self, text: str) -> Optional[bytes]:
        return self.handler.textToSpeech(text)

class AudioProcessor:
    """Handles audio recording and processing"""
    
    def __init__(self, services: Services):
        self.temp_audio_file = os.path.join(path_config.AUDIO_DIR, "temp_recording.wav")
        self.is_recording = False
        self.audio_buffer = []
        self.services = services
        
    def start_recording(self):
        """Start a new recording session"""
        self.is_recording = True
        self.audio_buffer = []
        logger.info("Started recording for speech recognition")
        
    def stop_recording(self) -> Optional[str]:
        """Stop recording and process the audio"""
        self.is_recording = False
        if self.audio_buffer:
            return self.transcribe_audio()
        return None

    def add_audio(self, audio_data: np.ndarray):
        """Add audio chunk to buffer if recording"""
        if self.is_recording:
            self.audio_buffer.extend(audio_data)
            
    def transcribe_audio(self) -> Optional[str]:
        """Transcribe recorded audio to text"""
        if not self.audio_buffer:
            return None
            
        try:
            # Save audio to WAV file
            with wave.open(self.temp_audio_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(audio_config.SAMPLE_RATE)
                wf.writeframes(np.array(self.audio_buffer, dtype=np.int16).tobytes())
            
            # Transcribe using service
            user_text = self.services.transcribeAudio(self.temp_audio_file)
            logger.info(f"Transcription completed: {user_text}")
            return user_text
            
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            return None
        finally:
            if os.path.exists(self.temp_audio_file):
                os.remove(self.temp_audio_file)

    def process_llm_and_tts(self, user_text: str) -> Optional[Dict[str, Union[str, bytes]]]:
        """Process text through LLM and convert response to speech"""
        try:
            # Get LLM response
            llm_response = self.services.generateText(user_text)
            logger.info(f"LLM response: {llm_response}")
            
            # Convert to speech
            tts_response = self.services.textToSpeech(llm_response)
            if tts_response:
                return {
                    "assistant_text": llm_response,
                    "audio": tts_response.decode('utf-8')
                }
            return None
            
        except Exception as e:
            logger.error(f"Error in LLM/TTS processing: {e}")
            return None
        finally:
            self.audio_buffer = []

class WakeWordManager:
    """Manages wake word detection"""
    
    def __init__(self):
        logger.info("Initializing Wake Word Manager...")
        try:
            self.model = Model(
                wakeword_models=[
                    f"{wake_word_config.MODELS_PATH}/Hi_I_Vee.onnx",
                ],
                inference_framework="onnx"
            )
            self.audio_buffer = np.array([], dtype=np.int16)
            self.last_detection_time = 0
            self.cooldown_period = 2.0  # Cooldown in seconds
            logger.info("Wake Word model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Wake Word Manager: {e}")
            raise

    def process_audio(self, audio_data: bytes) -> Dict[str, Union[bool, float, Optional[str]]]:
        """Process audio chunk for wake word detection"""
        try:
            new_audio = np.frombuffer(audio_data, dtype=np.int16)
            self.audio_buffer = np.append(self.audio_buffer, new_audio)
            
            results = []
            current_time = time.time()
            
            while len(self.audio_buffer) >= audio_config.CHUNK_SIZE:
                chunk = self.audio_buffer[:audio_config.CHUNK_SIZE]
                self.audio_buffer = self.audio_buffer[audio_config.CHUNK_SIZE:]
                
                prediction = self.model.predict(chunk)
                
                wake_word_detected = False
                detection_score = 0
                wake_word = None
                
                for mdl, scores in self.model.prediction_buffer.items():
                    # Only trigger if we're past the cooldown period
                    if (scores[-1] > wake_word_config.DETECTION_THRESHOLD and 
                        current_time - self.last_detection_time > self.cooldown_period):
                        wake_word_detected = True
                        detection_score = float(scores[-1])
                        wake_word = mdl
                        self.last_detection_time = current_time  # Update last detection time
                        logger.info(f"[{mdl}] Wake Word Detected. Score: {detection_score:2f}")
                        
                        # Return immediately on first detection
                        return {
                            "wake_word_detected": True,
                            "score": detection_score,
                            "wake_word": wake_word
                        }
                
                # Only add to results if we haven't detected anything
                if not wake_word_detected:
                    results.append({
                        "wake_word_detected": False,
                        "score": detection_score,
                        "wake_word": wake_word
                    })
            
            # If we haven't returned a detection yet, return the last result (or no detection)
            if results:
                return results[-1]
            return {"wake_word_detected": False, "score": 0, "wake_word": None}
            
        except Exception as e:
            logger.error(f"Error processing audio for wake word: {e}")
            return {
                "wake_word_detected": False,
                "score": 0,
                "wake_word": None
            }

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ModeUpdate(BaseModel):
    just_wwd: bool

@app.post("/set_mode")
async def set_mode(mode: ModeUpdate):
    """Endpoint to change the application mode"""
    app_config.JUST_DO_WWD = mode.just_wwd
    logger.info(f"Mode changed to: {'WWD-only' if mode.just_wwd else 'full pipeline'}")
    return {"status": "success", "mode": "WWD-only" if mode.just_wwd else "full pipeline"}

@app.get("/get_mode")
async def get_mode():
    """Endpoint to get current mode"""
    return {"just_wwd": app_config.JUST_DO_WWD}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint handling real-time audio processing and voice interactions.
    
    If JUST_DO_WWD is True, only perform wake word detection.
    Otherwise, perform full pipeline: Wake word -> STT -> LLM -> TTS
    """
    await websocket.accept()
    client_id = id(websocket)
    logger.info(f"WebSocket connection opened. Client ID: {client_id}")
    
    # Initialize wake word manager (always needed)
    wake_word_manager = WakeWordManager()
    logger.info(f"Running in {'WWD-only' if app_config.JUST_DO_WWD else 'full pipeline'} mode")
    
    # Initialize other components only if needed
    handler = None
    services = None
    audio_processor = None
    silence_counter = 0
    
    if not app_config.JUST_DO_WWD:
        handler = OpenAIHandler()
        services = Services(handler)
        audio_processor = AudioProcessor(services)
    
    try:
        while True:
            # Receive audio chunk from client
            audio_data = await websocket.receive_bytes()
            
            # Process audio for wake word detection
            result = wake_word_manager.process_audio(audio_data)
            
            if app_config.JUST_DO_WWD:
                # In WWD-only mode, just send wake word detection results
                if result["wake_word_detected"]:
                    logger.info(f"[WWD-only mode] Wake Word detected. Score: {result['score']:2f}")
                    await websocket.send_json({
                        "status": "success",
                        "wake_word_detected": True,
                        "wake_word": result["wake_word"],
                        "mode": "wwd_only"
                    })
                else:
                    await websocket.send_json({
                        "status": "success",
                        "wake_word_detected": False,
                        "mode": "wwd_only"
                    })
            else:
                # Full pipeline mode
                if result["wake_word_detected"] and not audio_processor.is_recording:
                    audio_processor.start_recording()
                    await websocket.send_json({
                        "status": "success",
                        "wake_word_detected": True,
                        "wake_word": result["wake_word"],
                        "action": "start_recording",
                        "mode": "full_pipeline"
                    })
                
                elif audio_processor.is_recording:
                    audio_data_np = np.frombuffer(audio_data, dtype=np.int16)
                    audio_processor.add_audio(audio_data_np)
                    
                    if np.max(np.abs(audio_data_np)) < vad_config.SILENCE_THRESHOLD:
                        silence_counter += 1
                    else:
                        silence_counter = 0
                    
                    if silence_counter >= vad_config.CHUNKS_FOR_SILENCE:
                        user_text = audio_processor.stop_recording()
                        if user_text:
                            await websocket.send_json({
                                "status": "success",
                                "action": "transcription_complete",
                                "user_text": user_text,
                                "mode": "full_pipeline"
                            })
                            
                            llm_result = audio_processor.process_llm_and_tts(user_text)
                            if llm_result:
                                await websocket.send_json({
                                    "status": "success",
                                    "action": "llm_complete",
                                    "assistant_text": llm_result["assistant_text"],
                                    "tts_audio": llm_result["audio"],
                                    "mode": "full_pipeline"
                                })
                        silence_counter = 0
                else:
                    await websocket.send_json({
                        "status": "success",
                        "wake_word_detected": result["wake_word_detected"],
                        "mode": "full_pipeline"
                    })
            
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {e}")
    finally:
        logger.info(f"WebSocket connection closed. Client ID: {client_id}")
        
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "WebSocket Wake Word Detection server is running",
        "mode": "WWD Only" if app_config.JUST_DO_WWD else "Full Pipeline"
    }

# uvicorn FastAPI_WWD_STT_TTS.py:app --reload

if __name__ == "__main__":
    import uvicorn
    PORT = os.getenv("PORT_SVC_WAKE_WORD_DETECTOR")
    logger.info(f"Starting server on port {PORT}")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=PORT,
        log_level="info"
    )