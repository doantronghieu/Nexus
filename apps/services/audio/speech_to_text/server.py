"""
FastAPI server for Speech-to-Text services.
Provides REST API endpoints and WebSocket support for audio transcription.

Available implementations:
- whisper_cpp: Local CPU-based inference using whisper.cpp library
- openai_whisper: Cloud-based inference using OpenAI's Whisper API
"""

import os
import time
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import importlib
import inspect
from loguru import logger
from pydantic import BaseModel, Field

import packages
from services.bases.server import FastAPIService, ServiceConfig
from services.audio.speech_to_text.core import CoreSpeechToText
from services.audio.speech_to_text.utils import (
    convert_to_wav,
    get_format_from_content,
    SUPPORTED_INPUT_FORMATS,
    SAMPLE_RATE,
    CHANNELS
)

class TranscriptionResponse(BaseModel):
    """Response model for transcription results"""
    text: str
    model: str
    language: str
    execution_time: float
    audio_duration: float
    
    class Config:
        orm_mode = True

class ModelInfo(BaseModel):
    """Model information response"""
    name: str
    type: str
    supported_languages: List[str]
    config: Dict[str, Any]
    
    class Config:
        orm_mode = True

class STTServiceConfig(ServiceConfig):
    """Configuration for STT service"""
    max_upload_size: int = Field(
        default=50 * 1024 * 1024,  # 50MB
        description="Maximum file upload size in bytes"
    )
    default_model: str = Field(
        default="whisper_cpp",
        description="Default model to use (options: whisper_cpp, openai_whisper)"
    )
    supported_input_formats: List[str] = Field(
        default=list(SUPPORTED_INPUT_FORMATS),
        description="List of supported input audio formats"
    )
    # Audio processing settings
    target_sample_rate: int = Field(
        default=SAMPLE_RATE,
        description="Target audio sample rate in Hz"
    )
    target_channels: int = Field(
        default=CHANNELS,
        description="Target number of audio channels"
    )
    temp_dir: str = Field(
        default="/tmp/stt_service",
        description="Directory for temporary files"
    )
    

class STTServer(FastAPIService):
    """
    Speech-to-Text service server providing REST API endpoints
    and a testing interface for audio transcription.
    """
    
    def __init__(
        self,
        name: str = "speech_to_text",
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize STT server"""
        # Convert dict config to STTServiceConfig if needed
        if isinstance(config, dict):
            config = STTServiceConfig(**config)
        else:
            config = config or STTServiceConfig(**self.get_default_config())
            
        super().__init__(name, config)
        
        # Dictionary to store model implementations
        self.models: Dict[str, CoreSpeechToText] = {}
        
        # Create temp directory
        os.makedirs(self.config.temp_dir, exist_ok=True)
        
        # Load available implementations
        self._load_implementations()

    def get_default_config(self) -> Dict[str, Any]:
        """Get default server configuration"""
        return {
            "host": "0.0.0.0",
            "port": int(os.getenv("PORT_SVC_STT", 6502)),
            "api_prefix": "/api/v1",
            "cors_origins": ["*"],
            "max_upload_size": 50 * 1024 * 1024,  # 50MB
            "default_model": os.getenv("DEFAULT_STT_MODEL", "whisper_cpp"),
            "supported_input_formats": list(SUPPORTED_INPUT_FORMATS),
            "target_sample_rate": SAMPLE_RATE,
            "target_channels": CHANNELS,
            "temp_dir": "/tmp/stt_service"
        }

    def _load_implementations(self) -> None:
        """Load available STT implementations"""
        impl_dir = os.path.join(packages.ROOT_PATH, "apps/services/audio/speech_to_text/impl")
        
        for file in os.listdir(impl_dir):
            if file.endswith(".py") and not file.startswith("__"):
                try:
                    # Import implementation module
                    module_name = f"services.audio.speech_to_text.impl.{file[:-3]}"
                    module = importlib.import_module(module_name)
                    
                    # Find service class
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, CoreSpeechToText) and 
                            obj != CoreSpeechToText):
                            
                            # Initialize service
                            service = obj()
                            service.initialize()
                            
                            # Store in models dict
                            self.models[service.name] = service
                            logger.info(f"Loaded STT implementation: {service.name}")
                            
                except Exception as e:
                    logger.error(f"Error loading implementation {file}: {str(e)}")

    def _setup_app(self) -> FastAPI:
        """Setup FastAPI application"""
        app = super()._setup_app()
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )
        
        # Register routes directly with router
        self.router.add_api_route(
            "/models",
            self.get_models,
            methods=["GET"],
            response_model=List[ModelInfo],
            summary="Get available models",
            description="Returns list of available STT models and their configurations"
        )
        
        self.router.add_api_route(
            "/transcribe",
            self.transcribe,
            methods=["POST"],
            response_model=TranscriptionResponse,
            summary="Transcribe audio",
            description="Transcribe uploaded audio file using specified model"
        )
        
        self.router.add_api_route(
            "/config/{model}",
            self.get_model_config,
            methods=["GET"],
            response_model=Dict[str, Any],
            summary="Get model config",
            description="Returns configuration parameters for specified model"
        )

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            try:
                logger.info("WebSocket connection attempt...")
                await websocket.accept()
                logger.info("WebSocket connection accepted")
                await self.handle_websocket(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}")
        
        # Include router with prefix
        app.include_router(self.router, prefix=self.config.api_prefix)
        
        return app

    async def get_models(self) -> List[ModelInfo]:
        """Get list of available models"""
        return [
            ModelInfo(
                name=name,
                type=model.__class__.__name__,
                supported_languages=model.get_supported_languages(),
                config=model.get_service_info()
            )
            for name, model in self.models.items()
        ]

    async def get_model_config(self, model: str) -> Dict[str, Any]:
        """Get configuration for specified model"""
        if model not in self.models:
            raise HTTPException(status_code=404, detail=f"Model {model} not found")
            
        return self.models[model].get_service_info()

    async def transcribe(
        self,
        file: UploadFile = File(...),
        model: str = Form(None),
        language: Optional[str] = Form(None)
    ) -> TranscriptionResponse:
        """
        Transcribe audio file
        
        Args:
            file: Audio file upload
            model: Model name to use (optional, uses default if not specified)
            language: Optional language code
            
        Returns:
            TranscriptionResponse with results
            
        Raises:
            HTTPException: If request is invalid
        """
        # Use default model if none specified
        model = model or self.config.default_model
        
        # Validate model
        if model not in self.models:
            raise HTTPException(status_code=404, detail=f"Model {model} not found")
            
        try:
            # Read file content
            content = await file.read()
            
            # Validate file size
            if len(content) > self.config.max_upload_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum size is {self.config.max_upload_size/1024/1024:.1f}MB"
                )
            
            # Get file format
            file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
            if not file_ext:
                # Try to detect format from content
                detected_format = get_format_from_content(content)
                if not detected_format:
                    raise HTTPException(
                        status_code=400,
                        detail="Could not determine audio format"
                    )
                file_ext = detected_format
            
            # Validate format
            if file_ext not in self.config.supported_input_formats:
                raise HTTPException(
                    status_code=415,
                    detail=f"Unsupported audio format. Supported formats: {', '.join(self.config.supported_input_formats)}"
                )
            
            # Convert to WAV if needed
            start_time = time.time()
            if file_ext != 'wav':
                logger.info(f"Converting {file_ext} to WAV format...")
                content, duration = await convert_to_wav(
                    content,
                    input_format=file_ext,
                    sample_rate=self.config.target_sample_rate,
                    channels=self.config.target_channels
                )
            else:
                duration = 0.0  # Will be set after transcription
            
            # Get model service
            service = self.models[model]
            
            # Transcribe
            text = service.transcribe(content, language=language)
            execution_time = time.time() - start_time
            
            return TranscriptionResponse(
                text=text,
                model=model,
                language=language or service.model_config.language,
                execution_time=execution_time,
                audio_duration=duration
            )
            
        except ValueError as e:
            logger.error(f"Audio preprocessing failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Audio preprocessing failed: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )

    async def ui_endpoint(self, request: Request) -> HTMLResponse:
        """Render testing interface"""
        # Get models and convert to dict for JSON serialization
        models = [model.dict() for model in await self.get_models()]
        
        # Add to template context with correct port
        context = self._get_template_context(request)
        context.update({
            "models": models,
            # Use server's configured port instead of request port
            "ws_url": f"ws://{request.url.hostname}:{self.config.port}/ws"
        })
        
        return self.templates.TemplateResponse("ui.html", context)

if __name__ == "__main__":
    # Create and run server
    config = {
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT_SVC_STT", 6502)),
        "api_prefix": "/api/v1",
        "cors_origins": ["*"],
        "max_upload_size": 50 * 1024 * 1024,  # 50MB
        "default_model": os.getenv("DEFAULT_STT_MODEL", "whisper_cpp"),
    }
    
    # Create and run service
    service = STTServer(
        name="speech_to_text",
        config=config
    )
    
    service.run()