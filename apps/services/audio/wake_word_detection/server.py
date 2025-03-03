"""
Wake Word Detection Service
Provides real-time wake word detection through WebSocket communication.
"""

import os
import numpy as np
import time
from typing import Any, Dict, Optional, List, Callable, Set, Union
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from dataclasses import dataclass
import openwakeword
from openwakeword.model import Model

import packages
from services.bases.server import (
    ServiceConfig,
    FastAPIService,
    EndpointType,
    HTTPMethod,
    WebSocketMessageType,
    WebSocketDataType
)

# Download wake word models at import
openwakeword.utils.download_models()

@dataclass
class AudioConfig:
    """Audio processing configuration"""
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 1280  # 80ms chunks at 16kHz
    CHUNK_DURATION_MS: float = CHUNK_SIZE / SAMPLE_RATE * 1000

@dataclass
class WakeWordConfig:
    """Wake word detection configuration"""
    MODELS_PATH: str = f"{packages.ROOT_PATH}/apps/services/audio/wake_word_detection/impl/openWakeWord/models"
    DETECTION_THRESHOLD: float = 0.5


class WakeWordManager:
    """Manages wake word detection processing"""
    
    def __init__(self, config: WakeWordConfig, debug=False):
        """
        Initialize wake word detection manager.
        
        Args:
            config: Wake word detection configuration
        """
        self.config = config
        self.debug = debug
        
        logger.info("Initializing Wake Word Manager...")
        try:
            model_path = f"{self.config.MODELS_PATH}/Hi_I_Vee.onnx"
            logger.info(f"Loading wake word model: {model_path}")
            logger.info(f"Detection threshold: {self.config.DETECTION_THRESHOLD}")
            
            self.model = Model(
                wakeword_models=[model_path],
                inference_framework="onnx"
            )
            self.audio_buffer = np.array([], dtype=np.int16)
            self.last_detection_time = 0
            self.cooldown_period = 2.0
            logger.info(f"Wake Word model loaded successfully from: {model_path}")
            
            # Log initial model state
            logger.info(f"Available models: {list(self.model.prediction_buffer.keys())}")
        except Exception as e:
            logger.error(f"Failed to initialize Wake Word Manager: {e}")
            raise

    def process_audio(self, audio_data: bytes) -> Dict[str, Union[bool, float, Optional[str]]]:
        """Process audio chunk for wake word detection."""
        try:
            # Convert audio bytes to numpy array
            new_audio = np.frombuffer(audio_data, dtype=np.int16)

            if self.debug:
                logger.debug(f"Received audio chunk: shape={new_audio.shape}, "
                             f"max_amplitude={np.max(np.abs(new_audio))}")
            
            # Append to buffer
            self.audio_buffer = np.append(self.audio_buffer, new_audio)
            buffer_duration_ms = len(self.audio_buffer) / 16  # at 16kHz

            if self.debug:
                logger.debug(f"Audio buffer: {len(self.audio_buffer)} samples ({buffer_duration_ms:.1f}ms)")
            
            results = []
            current_time = time.time()
            
            while len(self.audio_buffer) >= AudioConfig.CHUNK_SIZE:
                chunk = self.audio_buffer[:AudioConfig.CHUNK_SIZE]
                self.audio_buffer = self.audio_buffer[AudioConfig.CHUNK_SIZE:]
                
                # Get model predictions
                if self.debug: logger.debug(f"Processing chunk of size: {len(chunk)}")
                prediction = self.model.predict(chunk)
                
                # Log prediction buffer states
                for mdl_name, scores in self.model.prediction_buffer.items():
                    current_score = float(scores[-1]) if scores else 0
                    if self.debug: logger.debug(f"Model {mdl_name} score: {current_score:.3f}")
                
                wake_word_detected = False
                detection_score = 0
                wake_word = None
                
                # Process each model's predictions
                for mdl, scores in self.model.prediction_buffer.items():
                    current_score = float(scores[-1]) if scores else 0
                    
                    # Check if score exceeds threshold and cooldown period has passed
                    if (current_score > self.config.DETECTION_THRESHOLD and 
                        current_time - self.last_detection_time > self.cooldown_period):
                        wake_word_detected = True
                        detection_score = current_score
                        wake_word = mdl
                        self.last_detection_time = current_time
                        logger.info(f"[{mdl}] Wake Word Detected! Score: {detection_score:.3f}")
                        
                        return {
                            "wake_word_detected": True,
                            "score": detection_score,
                            "wake_word": wake_word
                        }
                    
                    # Keep track of highest score even if not detected
                    detection_score = max(detection_score, current_score)
                
                # Add result for this chunk
                chunk_result = {
                    "wake_word_detected": wake_word_detected,
                    "score": detection_score,
                    "wake_word": wake_word
                }
                results.append(chunk_result)
                if self.debug: logger.debug(f"Chunk processed with score: {detection_score:.3f}")
            
            # Return latest result if we have any
            if results:
                result = results[-1]
                if self.debug: logger.debug(f"Returning result: {result}")
                return result
                
            if self.debug: logger.debug("No results to return")
            return {
                "wake_word_detected": False,
                "score": 0,
                "wake_word": None
            }
            
        except Exception as e:
            logger.error(f"Error processing audio for wake word: {e}")
            return {
                "wake_word_detected": False,
                "score": 0,
                "wake_word": None
            }

class WakeWordDetectionService(FastAPIService):
    """FastAPI service for wake word detection through WebSocket"""
    
    # def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
    def __init__(
        self,
        name: str,
        config: Optional[Union[Dict[str, Any], ServiceConfig]] = None,
        routes: Optional[List[Dict[str, Any]]] = None,
        middleware: Optional[List[Dict[str, Any]]] = None,
        dependencies: Optional[List[Callable]] = None   
    ) -> None:
        """
        Initialize wake word detection service.
        
        Args:
            name: Service name
            config: Optional service configuration
        """
        super().__init__(
            name=name, 
            config=config,
        )
        
        # Initialize configurations
        self.audio_config = AudioConfig()
        self.wake_word_config = WakeWordConfig()
        
        # Initialize wake word manager
        self.wake_word_manager = None  # Will be initialized during _initialize_impl
        
        # Define routes - only UI route now
        self.routes = [
            
        ]

    def _setup_app(self) -> FastAPI:
        """
        Override _setup_app to set up the FastAPI application.
        
        Returns:
            FastAPI: Configured FastAPI application
        """
        app = super()._setup_app()
        
        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            # Accept the WebSocket connection
            await self.accept_websocket(websocket)
            client_id = id(websocket)
            
            # Send system log
            await websocket.send_json({
                "type": "log",
                "log_type": "system",
                "message": f"WebSocket connection opened. Client ID: {client_id}"
            })
            
            try:
                # Initialize wake word detector if needed
                if not self.wake_word_manager:
                    await websocket.send_json({
                        "type": "log",
                        "log_type": "warning",
                        "message": "Wake word manager not initialized, creating new instance"
                    })
                    self.wake_word_manager = WakeWordManager(self.wake_word_config)
                
                while True:
                    try:
                        # Receive audio data
                        audio_data = await websocket.receive_bytes()
                        
                        # Send debug log for audio chunk
                        audio_data_np = np.frombuffer(audio_data, dtype=np.int16)
                        await websocket.send_json({
                            "type": "log",
                            "log_type": "debug",
                            "message": f"Received audio chunk: shape={audio_data_np.shape}, max_amplitude={np.max(np.abs(audio_data_np))}"
                        })
                        
                        # Process with wake word detector
                        result = self.wake_word_manager.process_audio(audio_data)
                        
                        # Send result
                        if result["wake_word_detected"]:
                            await websocket.send_json({
                                "type": "result",
                                "data": {
                                    "status": "success",
                                    "wake_word_detected": True,
                                    "wake_word": result["wake_word"],
                                    "score": result["score"]
                                }
                            })
                        else:
                            await websocket.send_json({
                                "type": "result",
                                "data": {
                                    "status": "success",
                                    "wake_word_detected": False,
                                    "wake_word": None,
                                    "score": result["score"]
                                }
                            })
                        
                    except WebSocketDisconnect:
                        await websocket.send_json({
                            "type": "log",
                            "log_type": "system",
                            "message": f"WebSocket disconnected. Client ID: {client_id}"
                        })
                        break
                    except Exception as e:
                        await websocket.send_json({
                            "type": "log",
                            "log_type": "error",
                            "message": f"Error processing audio: {str(e)}"
                        })
                        
            except Exception as e:
                await websocket.send_json({
                    "type": "log",
                    "log_type": "error",
                    "message": f"Error in WebSocket connection: {str(e)}"
                })
            finally:
                await self.disconnect_websocket(websocket)
                await websocket.send_json({
                    "type": "log",
                    "log_type": "system",
                    "message": f"WebSocket connection closed. Client ID: {client_id}"
                })
        
        return app

    def _initialize_impl(self) -> None:
        """Implementation-specific initialization logic."""
        super()._initialize_impl()
        # Initialize wake word manager during service startup
        self.wake_word_manager = WakeWordManager(self.wake_word_config)
        
if __name__ == "__main__":
    # Service configuration
    config = ServiceConfig(
        host="0.0.0.0",  # Allow external connections
        port=int(os.getenv("PORT_SVC_WWD", 6500)),
        cors_origins=["*"],
    )

    # Create and run service
    service = WakeWordDetectionService(
        name="WakeWordDetector",
        config=config
    )
    
    service.run()