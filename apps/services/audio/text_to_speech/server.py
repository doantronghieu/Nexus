"""
FastAPI server providing text-to-speech synthesis using multiple TTS engines.
Supports real-time synthesis via WebSocket and REST endpoints.
"""

import os
from typing import Dict, Any, Optional, List, Union, Callable
from fastapi import (
    FastAPI, 
    APIRouter,
    WebSocket, 
    Request, 
    WebSocketDisconnect, 
    HTTPException
)
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from datetime import datetime
import json
from loguru import logger

import packages
from services.bases.server import (
    ServiceConfig, 
    FastAPIService,
    EndpointType,
    HTTPMethod,
    WebSocketMessageType,
    WebSocketDataType
)
from services.audio.text_to_speech.impl.piper import PiperTTS, PiperConfig
from services.audio.text_to_speech.impl.openai_tts import OpenAITTS, OpenAITTSConfig
from services.audio.text_to_speech.core import AudioConfig, CoreTextToSpeech

class SynthesisRequest(BaseModel):
    """Request model for text synthesis"""
    text: str = Field(..., description="Text to synthesize")
    engine: str = Field("piper", description="TTS engine to use")
    voice: Optional[str] = Field(None, description="Voice identifier")
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Speech speed")
    format: str = Field("wav", description="Output audio format")

class EngineInfo(BaseModel):
    """Response model for engine information"""
    name: str
    supported_voices: List[Dict[str, Any]]
    supported_languages: List[str]
    supported_formats: List[str]
    config: Dict[str, Any]

class TTSService(FastAPIService):
    """FastAPI service for text-to-speech synthesis"""
    
    def __init__(
        self,
        name: str,
        config: Optional[Union[Dict[str, Any], ServiceConfig]] = None,
        routes: Optional[List[Dict[str, Any]]] = None,
        middleware: Optional[List[Dict[str, Any]]] = None,
        dependencies: Optional[List[Callable]] = None   
    ) -> None:
        """Initialize TTS service"""
        super().__init__(
            name=name, 
            config=config,
            routes=routes,
            middleware=middleware,
            dependencies=dependencies
        )
        
        # Initialize TTS engines
        self.engines: Dict[str, CoreTextToSpeech] = {}
        self._initialize_engines()
        
        # Streaming state
        self._active_streams: Dict[str, Dict[str, Any]] = {}

    def _initialize_engines(self) -> None:
        """Initialize available TTS engines"""
        try:
            # Initialize Piper
            piper = PiperTTS(
                name="PiperTTS",
                model_config=PiperConfig()
            )
            piper.initialize()
            self.engines["piper"] = piper
            
            openai_tts = OpenAITTS(
                name="OpenAITTS",
                model_config=OpenAITTSConfig()
            )
            self.engines["openai"] = openai_tts
            
            logger.info(f"Initialized {len(self.engines)} TTS engines")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engines: {str(e)}")
            raise

    async def synthesize_text(
        self,
        request: SynthesisRequest
    ) -> StreamingResponse:
        """
        Synthesize text to speech via HTTP POST
        """
        try:
            # Get requested engine
            engine = self.engines.get(request.engine)
            if not engine:
                raise HTTPException(
                    status_code=400,
                    detail=f"Engine {request.engine} not found"
                )
            
            # Configure audio settings
            audio_config = AudioConfig(
                format=request.format,
                speed=request.speed
            )
            
            # Generate audio with voice override
            audio_data = await engine.synthesize_text(
                text=request.text,
                audio_config=audio_config,
                voice_override=request.voice
            )
            
            # Return streaming response
            return StreamingResponse(
                content=iter([audio_data]),
                media_type=f"audio/{request.format}",
                headers={
                    "Content-Disposition": f"attachment; filename=speech.{request.format}"
                }
            )
            
        except Exception as e:
            logger.error(f"Synthesis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_engines(self) -> List[str]:
        """Get list of available TTS engines"""
        return list(self.engines.keys())

    async def get_engine_info(
        self,
        engine_id: str
    ) -> EngineInfo:
        """
        Get information about a specific engine
        """
        engine = self.engines.get(engine_id)
        if not engine:
            raise HTTPException(
                status_code=404,
                detail=f"Engine {engine_id} not found"
            )
        
        return EngineInfo(
            name=engine.name,
            supported_voices=engine.available_voices,
            supported_languages=engine.supported_languages,
            supported_formats=engine.supported_audio_formats,
            config=engine.get_model_info()
        )

    def _setup_app(self) -> FastAPI:
        """Setup FastAPI application"""
        app = super()._setup_app()
        
        # Configure CORS for both HTTP and WebSocket
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )
        
        # Register REST endpoints properly
        self.router.add_api_route(
            "/synthesize",
            self.synthesize_text,
            methods=["POST"],
            response_class=StreamingResponse
        )
        
        self.router.add_api_route(
            "/engines",
            self.get_engines,
            methods=["GET"]
        )
        
        self.router.add_api_route(
            "/engine/{engine_id}/info",
            self.get_engine_info,
            methods=["GET"],
            response_model=EngineInfo
        )
        
        # Register WebSocket endpoint directly on app
        app.add_api_websocket_route(
            path="/ws",
            endpoint=self.handle_websocket
        )
        
        app.include_router(self.router, prefix=self.config.api_prefix)
        
        return app

    async def handle_websocket(self, websocket: WebSocket) -> None:
        """Handle WebSocket connection and messages"""
        logger.info("WebSocket connection attempt...")
        
        await self.accept_websocket(websocket)
        stream_id = str(id(websocket))
        logger.info(f"WebSocket connected: {stream_id}")
        
        try:
            # Send initial connection success message
            await websocket.send_json({
                "type": "connection",
                "status": "connected",
                "stream_id": stream_id
            })
            
            while True:
                try:
                    message = await websocket.receive_json()
                    logger.debug(f"Received WebSocket message: {message}")
                    
                    if message.get("type") == "synthesize":
                        await self._handle_synthesis_request(
                            websocket=websocket,
                            stream_id=stream_id,
                            message=message
                        )
                    else:
                        logger.warning(f"Unknown message type: {message.get('type')}")
                        
                except WebSocketDisconnect:
                    logger.info(f"WebSocket disconnected: {stream_id}")
                    break
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "error": "Invalid message format"
                    })
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "error": str(e)
                    })
                    
        finally:
            logger.info(f"Cleaning up WebSocket connection: {stream_id}")
            await self.disconnect_websocket(websocket)
            # Cleanup any active streams
            if stream_id in self._active_streams:
                del self._active_streams[stream_id]

    async def _handle_synthesis_request(
        self,
        websocket: WebSocket,
        stream_id: str,
        message: Dict[str, Any]
    ) -> None:
        """Handle synthesis request over WebSocket"""
        try:
            # Debug logging for incoming request
            logger.info(f"Synthesis request received: {json.dumps(message, indent=2)}")
            
            # Parse request
            request = SynthesisRequest(**message["data"])
            logger.info(f"Using voice: {request.voice}")
            
            # Get engine
            engine = self.engines.get(request.engine)
            if not engine:
                raise ValueError(f"Engine {request.engine} not found")
            
            # Configure audio
            audio_config = AudioConfig(
                format=request.format,
                speed=request.speed
            )
            
            # Setup stream tracking
            self._active_streams[stream_id] = {
                "start_time": datetime.utcnow(),
                "engine": request.engine,
                "cancel": False,
                "request_id": message.get("requestId")
            }
            
            try:
                # Send progress update
                await websocket.send_json({
                    "type": "status",
                    "status": "generating",
                    "requestId": message.get("requestId")
                })
                
                # Generate audio with voice override
                audio_data = await engine.synthesize_text(
                    text=request.text,
                    audio_config=audio_config,
                    voice_override=request.voice
                )
                
                # Send audio data
                await websocket.send_bytes(audio_data)
                
                # Send completion status
                await websocket.send_json({
                    "type": "status",
                    "status": "completed",
                    "requestId": message.get("requestId"),
                    "size": len(audio_data)
                })
                
                logger.info(f"Sent {len(audio_data)} bytes of audio data")
                
            except Exception as e:
                # Send error status
                await websocket.send_json({
                    "type": "error",
                    "requestId": message.get("requestId"),
                    "error": str(e)
                })
                raise
            
        except Exception as e:
            logger.error(f"Synthesis failed: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "requestId": message.get("requestId"),
                "error": str(e)
            })
            
        finally:
            # Cleanup stream tracking
            if stream_id in self._active_streams:
                del self._active_streams[stream_id]

if __name__ == "__main__":
    # Service configuration
    config = ServiceConfig(
        host="0.0.0.0",  # Allow external connections
        port=int(os.getenv("PORT_SVC_TTS", 6501)),
        cors_origins=["*"],
    )
    
    # Create and run service
    service = TTSService(
        name="TextToSpeech",
        config=config
    )
    
    service.run()