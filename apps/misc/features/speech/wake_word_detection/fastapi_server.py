from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from openwakeword.model import Model
import asyncio
import json
import time
from typing import Dict, List, Optional
from dataclasses import asdict, dataclass
import logging
from config import model_config, server_config, audio_config, app_config

@dataclass
class WakeWordEvent:
    """Data class for wake word detection events."""
    event: str = 'wake_word'
    wake_word: str = model_config.WAKE_WORD
    confidence: float = 0.0
    timestamp: float = 0.0

class AudioProcessor:
    """Process audio data and detect wake words."""
    def __init__(self):
        self.logger = app_config.setup_logging('AudioProcessor')
        try:
            self.model = Model(
                wakeword_models=[model_config.WAKE_WORD],
                inference_framework=model_config.INFERENCE_FRAMEWORK
            )
            self.logger.info(f"Wake word model loaded successfully: {model_config.WAKE_WORD}")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
        
    def process_audio(self, audio_data: np.ndarray) -> Optional[WakeWordEvent]:
        try:
            # Ensure audio data is in correct format
            if audio_data.dtype != np.int16:
                audio_data = (audio_data * 32767).astype(np.int16)
            
            # Process audio through wake word model
            prediction = self.model.predict(audio_data)
            
            # Check predictions against threshold
            for mdl, scores in self.model.prediction_buffer.items():
                confidence = float(scores[-1])
                if confidence > model_config.CONFIDENCE_THRESHOLD:
                    self.logger.info(f"Wake word detected with confidence: {confidence}")
                    return WakeWordEvent(
                        wake_word=mdl,
                        confidence=confidence,
                        timestamp=time.time()
                    )
            return None
            
        except Exception as e:
            self.logger.error(f"Error processing audio data: {e}")
            return None

class ConnectionManager:
    """Manage WebSocket connections and audio processing."""
    def __init__(self):
        self.logger = app_config.setup_logging('ConnectionManager')
        self.active_connections: List[WebSocket] = []
        self.audio_processor = AudioProcessor()
        
    async def connect(self, websocket: WebSocket):
        """Accept and store new WebSocket connection."""
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            self.logger.info(f"New client connected. Total connections: {len(self.active_connections)}")
        except Exception as e:
            self.logger.error(f"Error accepting WebSocket connection: {e}")
            raise
        
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        try:
            self.active_connections.remove(websocket)
            self.logger.info(f"Client disconnected. Remaining connections: {len(self.active_connections)}")
        except ValueError:
            pass
            
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                self.logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
                
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
            
    async def process_audio_message(self, websocket: WebSocket, data: bytes):
        """Process incoming audio data from WebSocket."""
        try:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(data, dtype=np.float32)
            
            # Process audio data
            result = self.audio_processor.process_audio(audio_data)
            
            # Send detection result if wake word found
            if result:
                await websocket.send_json(asdict(result))
                
        except Exception as e:
            self.logger.error(f"Error processing audio message: {e}")
            try:
                await websocket.send_json({
                    'event': 'error',
                    'message': str(e),
                    'timestamp': time.time()
                })
            except Exception:
                pass

class FastAPIServer:
    def __init__(self):
        self.app = FastAPI(
            title="Wake Word Detection API",
            description="Browser-based wake word detection system",
            version="1.0.0"
        )
        self.logger = app_config.setup_logging('FastAPIServer')
        self.connection_manager = ConnectionManager()
        
        # Add CORS middleware with proper configuration
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:3000",  # Your Nuxt.js app
                "http://localhost:5000",  # FastAPI server
                "null",  # Allow connections from local files
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
        
    def _setup_routes(self):
        """Configure FastAPI routes."""
        
        @self.app.get("/health", response_model=dict)
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "timestamp": time.time(),
                "websocket_clients": len(self.connection_manager.active_connections)
            }

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            try:
                # 2. Handle WebSocket connection with proper error handling
                await websocket.accept()
                self.logger.info(f"WebSocket connected: {websocket.client}")
                
                # 3. Keep connection alive and handle messages
                while True:
                    try:
                        data = await websocket.receive_bytes()
                        # Process your audio data here
                        # await self.connection_manager.process_audio_message(websocket, data)
                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")
                        break
                        
            except Exception as e:
                self.logger.error(f"WebSocket error: {e}")
            finally:
                try:
                    await websocket.close()
                except:
                    pass
                self.logger.info("WebSocket connection closed")
        
        @self.app.get("/health", response_model=dict)
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "timestamp": time.time(),
                "websocket_clients": len(self.connection_manager.active_connections)
            }

        @self.app.options("/health")
        async def health_check_preflight():
            """Handle OPTIONS preflight request for health check."""
            return JSONResponse(
                status_code=200,
                content={"status": "ok"},
                headers={
                    "Access-Control-Allow-Origin": "http://localhost:3000",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                }
            )

        
        @self.app.get("/config")
        async def get_config():
            """Get current system configuration."""
            return {
                "model": asdict(model_config),
                "audio": asdict(audio_config),
                "server": asdict(server_config)
            }

def create_app():
    server = FastAPIServer()
    return server.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:create_app",
        host="0.0.0.0",
        port=5000,
        factory=True,
        reload=True
    )