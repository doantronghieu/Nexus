"""
FastAPI Service Base Class
Provides HTTP and WebSocket functionality with support for templates and multiple data types.
"""

import os
import sys
import json
import asyncio
from typing import Any, Dict, Optional, List, Callable, Set, Union
from datetime import datetime
from enum import Enum
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request, Response, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import websockets
from websockets.exceptions import ConnectionClosed
from loguru import logger
from pydantic import BaseModel, Field, field_validator

import packages
from services.bases.service import BaseService

class EndpointType(str, Enum):
    """Endpoint types for route definitions"""
    HTTP = "http"
    WEBSOCKET = "websocket"

class HTTPMethod(str, Enum):
    """HTTP methods enum for route definitions"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class WebSocketDataType(str, Enum):
    """Data types for WebSocket messages"""
    TEXT = "text"
    JSON = "json"
    BYTES = "bytes"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    BINARY = "binary"

class WebSocketMessageType(str, Enum):
    """Message types for structured communication"""
    MESSAGE = "message"      # Regular message
    ERROR = "error"         # Error message
    SYSTEM = "system"       # System message
    HEARTBEAT = "heartbeat" # Heartbeat message
    FILE = "file"          # File transfer
    STREAM = "stream"      # Media stream

class ServiceConfig(BaseModel):
    """Pydantic model for service configuration validation"""
    # "0.0.0.0", "localhost"
    host: Optional[str] = Field(default="0.0.0.0", description="Service host address")
    port: Optional[int] = Field(default=8000, ge=1, le=65535, description="Service port number")
    api_prefix: Optional[str] = Field(default="", description="API prefix for all routes")
    websocket_ping_interval: Optional[float] = Field(
        default=30.0, 
        gt=0, 
        description="Interval in seconds for WebSocket heartbeat"
    )
    max_reconnect_attempts: Optional[int] = Field(
        default=5, 
        ge=0, 
        description="Maximum WebSocket client reconnection attempts"
    )
    max_message_size: Optional[int] = Field(
        default=10 * 1024 * 1024,  # 10MB
        gt=0,
        description="Maximum allowed WebSocket message size in bytes"
    )
    cors_origins: Optional[List[str]] = Field(
        default=["*"],
        description="Allowed CORS origins"
    )
    environment: Optional[str] = Field(
        default="development",
        description="Service environment (development, staging, production)"
    )
    version: Optional[str] = Field(
        default="1.0.0",
        description="Service version"
    )
    log_level: Optional[str] = Field(
        default="info",
        description="Logging level"
    )
    reload: Optional[bool] = Field(
        default=False,
        description="Enable auto-reload for development"
    )
    workers: Optional[int] = Field(
        default=1,
        ge=1,
        description="Number of worker processes"
    )
    ssl_keyfile: Optional[str] = Field(
        default=None,
        description="Path to SSL key file"
    )
    ssl_certfile: Optional[str] = Field(
        default=None,
        description="Path to SSL certificate file"
    )
    ssl_ca_certs: Optional[str] = Field(
        default=None,
        description="Path to SSL CA certificates file"
    )

    @field_validator('host')
    def validate_host(cls, value):
        if not value:
            raise ValueError("Host cannot be empty")
        return value

    @field_validator('cors_origins')
    def validate_cors_origins(cls, value):
        if not isinstance(value, list):
            raise ValueError("cors_origins must be a list")
        return value

class FastAPIService(BaseService):
    """
    FastAPI service base class with HTTP and WebSocket support.
    Features:
    - HTTP endpoints with method-based routing
    - WebSocket support (both server and client)
    - Multiple data type handling (text, JSON, binary, media)
    - Template serving with Jinja2
    - Static file serving
    - Automatic OpenAPI documentation
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Union[Dict[str, Any], ServiceConfig]] = None,
        routes: Optional[List[Dict[str, Any]]] = None,
        middleware: Optional[List[Dict[str, Any]]] = None,
        dependencies: Optional[List[Callable]] = None   
    ) -> None:
        """Initialize the FastAPI service."""
        super().__init__(name, config)
        self.routes = routes or []
        self.middleware = middleware or []
        self.dependencies = dependencies or []
        self.router = APIRouter()
        
        # WebSocket connection tracking
        self.active_websockets: Set[WebSocket] = set()
        self.client_connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.client_tasks: Dict[str, asyncio.Task] = {}
        
        # Create service template directory if it doesn't exist
        os.makedirs(self.service_template_dir, exist_ok=True)
        
        # Initialize templates with base and service-specific directories
        self.templates = Jinja2Templates(
            directory=[
                f"{packages.APP_PATH}/services/bases/templates",
                self.service_template_dir
            ]
        )
        
        # Convert dict to ServiceConfig if needed
        self.config = config if isinstance(config, ServiceConfig) else ServiceConfig(**config)
        
        # Setup FastAPI application
        self.app = self._setup_app()

    @property
    def service_template_dir(self) -> str:
        """Default implementation for service-specific template directory.
        Uses __file__ from the child class's perspective."""
        module = sys.modules[self.__class__.__module__]
        return os.path.join(os.path.dirname(module.__file__), "templates")

    
    def _get_template_context(self, request: Request) -> Dict[str, Any]:
        """
        Get the base template context including server configuration.
        
        Args:
            request: The FastAPI request object
            
        Returns:
            Dict containing template context variables
        """
        protocol = "https" if request.url.scheme == "https" else "http"
        ws_protocol = "wss" if protocol == "https" else "ws"
        base_url = f"{protocol}://{self.config.host}:{self.config.port}"
        ws_url = f"{ws_protocol}://{self.config.host}:{self.config.port}"
        
        return {
            "request": request,
            "service_name": self.name,
            "server_config": {
                "host": self.config.host,
                "port": self.config.port,
                "api_prefix": self.config.api_prefix,
                "base_url": base_url,
                "ws_url": ws_url,
                "full_api_url": f"{base_url}{self.config.api_prefix}",
                "full_ws_url": f"{ws_url}{self.config.api_prefix}/ws",
                "environment": self.config.environment,
                "version": self.config.version,
            }
        }

    def _setup_app(self) -> FastAPI:
        """Setup FastAPI application with middleware and routes."""
        app = FastAPI(
            title=f"{self.name} Service",
            description=f"API for {self.name} service",
            version=self.config.version,
            lifespan=self._create_lifespan(),
            openapi_url=f"{self.config.api_prefix}/openapi.json",
            docs_url=f"{self.config.api_prefix}/docs",
            redoc_url=f"{self.config.api_prefix}/redoc"
        )
        
        # Setup CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add custom middleware
        for middleware_config in self.middleware:
            app.add_middleware(**middleware_config)

        # Add error handlers
        app.add_exception_handler(Exception, self._error_handler)
        
        # Mount static files
        static_dir = f"{packages.APP_PATH}/services/bases/static"
        os.makedirs(static_dir, exist_ok=True)
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
        
        # Register dashboard endpoint (root)
        @app.get("/", response_class=HTMLResponse)
        async def dashboard(request: Request):
            return self.templates.TemplateResponse(
                "index.html",
                self._get_template_context(request)
            )
        
        # Register UI route directly with the app (no prefix)
        app.get("/ui", response_class=HTMLResponse)(self.ui_endpoint)
        
        # Register WebSocket testing interface endpoint
        @app.get("/websocket", response_class=HTMLResponse)
        async def websocket_test(request: Request):
            return self.templates.TemplateResponse(
                "websocket.html",
                self._get_template_context(request)
            )

        # # Register default WebSocket endpoint
        # @self.router.websocket("/ws")
        # async def websocket_endpoint(websocket: WebSocket):
        #     await self.handle_websocket(websocket)
        
        # Register health check endpoint
        @app.get("/health")
        async def health():
            return {
                "service": self.name,
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": self.config.version,
                "environment": self.config.environment,
                "server_connections": len(self.active_websockets),
                "client_connections": len(self.client_connections)
            }
        
        # Register routes from child services first
        for route_config in self.routes:
            self._register_route(route_config)
            
        # Include router in app with prefix
        app.include_router(self.router, prefix=self.config.api_prefix)
        
        return app
    
    async def ui_endpoint(self, request: Request) -> HTMLResponse:
        """
        Endpoint to serve the testing UI.
        
        Args:
            request: FastAPI request object
            
        Returns:
            HTMLResponse containing the UI template
        """
        return self.templates.TemplateResponse(
            "ui.html",
            self._get_template_context(request)
        )
    
    def _register_route(self, route_config: Dict[str, Any]) -> None:
        """
        Register a route with the FastAPI router.
        
        Args:
            route_config: Dictionary containing route configuration
        """
        path = route_config["path"]
        handler = route_config["handler"]
        endpoint_type = route_config.get("endpoint_type", EndpointType.HTTP)
        
        if endpoint_type == EndpointType.WEBSOCKET:
            self.router.websocket(path)(handler)
        else:
            if isinstance(route_config["method"], str):
                method = HTTPMethod[route_config["method"].upper()]
            else:
                method = route_config["method"]
                
            route_decorator = getattr(self.router, method.value.lower())
            route_decorator(
                path,
                response_model=route_config.get("response_model"),
                status_code=route_config.get("status_code", 200),
                tags=route_config.get("tags", []),
                summary=route_config.get("summary"),
                description=route_config.get("description"),
                dependencies=route_config.get("dependencies", []),
                response_class=route_config.get("response_class")
            )(handler)

    def _validate_config(self) -> None:
        """
        Validate service configuration. Must be implemented by concrete services.
        
        Raises:
            ValueError: If configuration is invalid
        """
        pass

    async def _error_handler(self, request: Request, exc: Exception) -> Response:
        """
        Global error handler for all endpoints.
        
        Args:
            request: The FastAPI request object
            exc: The exception that occurred
            
        Returns:
            JSONResponse containing error details
        """
        logger.error(f"Error processing request: {str(exc)}")
        
        status_code = 500
        if isinstance(exc, HTTPException):
            status_code = exc.status_code
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": str(exc),
                "type": exc.__class__.__name__,
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path,
                "method": request.method,
                "client": request.client.host if request.client else None
            }
        )

    def _create_lifespan(self):
        """Create FastAPI lifespan context manager for startup and shutdown events."""
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Startup
            logger.info(f"Starting {self.name} service on {self.config.host}:{self.config.port}")
            
            try:
                # Start heartbeat if configured
                if self.config.websocket_ping_interval:
                    self.heartbeat_task = asyncio.create_task(self.heartbeat())
                yield
            finally:
                # Shutdown
                logger.info(f"Shutting down {self.name} service")
                
                # Cancel heartbeat task if it exists
                if hasattr(self, 'heartbeat_task'):
                    self.heartbeat_task.cancel()
                    try:
                        await self.heartbeat_task
                    except asyncio.CancelledError:
                        pass
                
                # Cleanup WebSocket connections
                await self._cleanup_websockets()
        
        return lifespan

    async def handle_websocket(self, websocket: WebSocket) -> None:
        """
        Default WebSocket handler for managing WebSocket connections and messages.
        
        Args:
            websocket: The WebSocket connection
        """
        await self.accept_websocket(websocket)
        try:
            file_metadata = None  # Store metadata for incoming file
            while True:
                try:
                    # Receive message with type detection
                    message = await websocket.receive()
                    
                    if message["type"] == "websocket.disconnect":
                        break
                    
                    timestamp = datetime.utcnow().isoformat()
                    
                    # Handle different message types
                    if message["type"] == "websocket.receive":
                        if "text" in message:
                            try:
                                # Parse JSON message
                                data = json.loads(message["text"])
                                msg_type = data.get("type", "text")

                                if msg_type == "file":
                                    # Store metadata for next binary message
                                    file_metadata = data
                                    continue
                                
                                # Handle other message types
                                response = {
                                    "type": WebSocketMessageType.MESSAGE,
                                    "data_type": WebSocketDataType.JSON,
                                    "data": data,
                                    "timestamp": timestamp
                                }
                                await websocket.send_json(response)
                                
                            except json.JSONDecodeError:
                                await websocket.send_json({
                                    "type": WebSocketMessageType.ERROR,
                                    "data_type": WebSocketDataType.TEXT,
                                    "data": "Invalid JSON format",
                                    "timestamp": timestamp
                                })
                        
                        elif "bytes" in message:
                            # Check message size
                            if len(message["bytes"]) > self.config.max_message_size:
                                await websocket.send_json({
                                    "type": WebSocketMessageType.ERROR,
                                    "data_type": WebSocketDataType.TEXT,
                                    "data": "Message size exceeds limit",
                                    "timestamp": timestamp
                                })
                                continue
                            
                            # Handle binary data
                            binary_data = message["bytes"]
                            
                            if file_metadata:
                                # Process file with metadata
                                data_type = self._detect_binary_type(binary_data)
                                response = {
                                    "type": WebSocketMessageType.FILE,
                                    "data_type": data_type,
                                    "metadata": file_metadata,
                                    "size": len(binary_data),
                                    "timestamp": timestamp
                                }
                                await websocket.send_json(response)
                                file_metadata = None
                            else:
                                # Handle raw binary data
                                data_type = self._detect_binary_type(binary_data)
                                response = {
                                    "type": WebSocketMessageType.FILE,
                                    "data_type": data_type,
                                    "size": len(binary_data),
                                    "timestamp": timestamp
                                }
                                await websocket.send_json(response)
                    
                except WebSocketDisconnect:
                    logger.debug("WebSocket disconnected")
                    break
                except Exception as e:
                    error_response = {
                        "type": WebSocketMessageType.ERROR,
                        "data_type": WebSocketDataType.TEXT,
                        "error": str(e),
                        "timestamp": timestamp
                    }
                    await websocket.send_json(error_response)
                    logger.error(f"Error in WebSocket handler: {str(e)}")
        finally:
            await self.disconnect_websocket(websocket)

    def _detect_binary_type(self, data: bytes) -> WebSocketDataType:
        """
        Detect the type of binary data based on magic numbers or patterns.
        
        Args:
            data: Binary data to analyze
            
        Returns:
            WebSocketDataType indicating the detected type
        """
        if len(data) < 4:
            return WebSocketDataType.BINARY
            
        # Image formats
        if data.startswith(b'\xFF\xD8\xFF'):  # JPEG
            return WebSocketDataType.IMAGE
        if data.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
            return WebSocketDataType.IMAGE
        if data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):  # GIF
            return WebSocketDataType.IMAGE
            
        # Audio formats
        if data.startswith(b'RIFF'):  # WAV
            return WebSocketDataType.AUDIO
        if data.startswith(b'ID3') or data.startswith(b'\xFF\xFB'):  # MP3
            return WebSocketDataType.AUDIO
            
        # Video formats
        if data.startswith(b'\x00\x00\x00\x18ftyp') or data.startswith(b'\x00\x00\x00\x1cftyp'):  # MP4
            return WebSocketDataType.VIDEO
            
        return WebSocketDataType.BINARY

    # Server-side WebSocket methods
    async def accept_websocket(self, websocket: WebSocket) -> None:
        """
        Accept and track a WebSocket connection.
        
        Args:
            websocket: The WebSocket connection to accept
        """
        await websocket.accept()
        self.active_websockets.add(websocket)
        logger.debug(f"WebSocket client connected. Active connections: {len(self.active_websockets)}")

    async def disconnect_websocket(self, websocket: WebSocket) -> None:
        """
        Disconnect and remove a WebSocket connection.
        
        Args:
            websocket: The WebSocket connection to disconnect
        """
        if websocket in self.active_websockets:
            self.active_websockets.remove(websocket)
            logger.debug(f"WebSocket client disconnected. Active connections: {len(self.active_websockets)}")

    async def broadcast_server_message(
        self, 
        message: Union[str, Dict], 
        message_type: WebSocketMessageType = WebSocketMessageType.MESSAGE,
        exclude: Optional[WebSocket] = None
    ) -> None:
        """
        Broadcast a message to all server-side WebSocket clients.
        
        Args:
            message: Message to broadcast (string or dictionary)
            message_type: Type of message to send
            exclude: Optional WebSocket connection to exclude from broadcast
        """
        if isinstance(message, dict):
            message = json.dumps({
                "type": message_type,
                "data": message,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        disconnect_tasks = []
        for websocket in self.active_websockets:
            if websocket != exclude:
                try:
                    await websocket.send_text(message)
                except WebSocketDisconnect:
                    disconnect_tasks.append(self.disconnect_websocket(websocket))
                except Exception as e:
                    logger.error(f"Error broadcasting message: {str(e)}")
                    disconnect_tasks.append(self.disconnect_websocket(websocket))
        
        if disconnect_tasks:
            await asyncio.gather(*disconnect_tasks)
    
    # Client-side WebSocket methods
    async def connect_to_websocket(
        self,
        url: str,
        connection_id: str,
        message_handler: Callable[[str], Any],
        reconnect: bool = True,
        max_retries: Optional[int] = None,
        retry_delay: float = 1.0
    ) -> None:
        """
        Connect to a remote WebSocket server as a client.
        
        Args:
            url: WebSocket server URL to connect to
            connection_id: Unique identifier for this connection
            message_handler: Callback function to handle received messages
            reconnect: Whether to attempt reconnection on disconnection
            max_retries: Maximum number of reconnection attempts
            retry_delay: Delay between reconnection attempts
        """
        max_retries = max_retries or self.config.max_reconnect_attempts
        
        async def connection_handler():
            retry_count = 0
            while True:
                try:
                    async with websockets.connect(url) as websocket:
                        self.client_connections[connection_id] = websocket
                        logger.info(f"Connected to WebSocket server: {url} (ID: {connection_id})")
                        
                        retry_count = 0
                        
                        while True:
                            try:
                                message = await websocket.recv()
                                await message_handler(message)
                            except ConnectionClosed:
                                break
                            except Exception as e:
                                logger.error(f"Error handling message from {url}: {str(e)}")
                                break
                
                except Exception as e:
                    logger.error(f"WebSocket client connection error: {str(e)}")
                    
                    if connection_id in self.client_connections:
                        del self.client_connections[connection_id]
                    
                    if not reconnect or (max_retries is not None and retry_count >= max_retries):
                        logger.error(f"Max retries ({max_retries}) reached for {url}")
                        break
                    
                    retry_count += 1
                    await asyncio.sleep(retry_delay)
                    logger.info(f"Attempting reconnection to {url} (attempt {retry_count}/{max_retries})")
                    continue
                
                if not reconnect:
                    break
        
        # Cancel existing task if any
        if connection_id in self.client_tasks:
            self.client_tasks[connection_id].cancel()
            try:
                await self.client_tasks[connection_id]
            except asyncio.CancelledError:
                pass
        
        task = asyncio.create_task(connection_handler())
        self.client_tasks[connection_id] = task

    async def send_client_message(
        self,
        connection_id: str,
        message: Union[str, Dict, bytes],
        message_type: WebSocketMessageType = WebSocketMessageType.MESSAGE
    ) -> bool:
        """
        Send a message through a client WebSocket connection.
        
        Args:
            connection_id: Client connection identifier
            message: Message to send (string, dict, or bytes)
            message_type: Type of message
            
        Returns:
            bool: Success status
        """
        if connection_id not in self.client_connections:
            logger.error(f"No active connection found for ID: {connection_id}")
            return False
        
        websocket = self.client_connections[connection_id]
        try:
            if isinstance(message, bytes):
                await websocket.send(message)
            else:
                if isinstance(message, dict):
                    message = {
                        "type": message_type,
                        "data": message,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    message = json.dumps(message)
                await websocket.send(message)
            return True
        except Exception as e:
            logger.error(f"Error sending message through client connection {connection_id}: {str(e)}")
            return False

    async def broadcast_all(
        self,
        message: Union[str, Dict, bytes],
        message_type: WebSocketMessageType = WebSocketMessageType.MESSAGE,
        exclude_server: Optional[WebSocket] = None,
        exclude_clients: Optional[List[str]] = None
    ) -> None:
        """
        Broadcast a message to all WebSocket connections (both server and client).
        
        Args:
            message: Message to broadcast
            message_type: Type of message
            exclude_server: Server connection to exclude
            exclude_clients: Client connections to exclude
        """
        # Broadcast to server connections
        await self.broadcast_server_message(message, message_type, exclude_server)
        
        # Broadcast to client connections
        exclude_clients = exclude_clients or []
        for connection_id, websocket in self.client_connections.items():
            if connection_id not in exclude_clients:
                try:
                    if isinstance(message, bytes):
                        await websocket.send(message)
                    else:
                        if isinstance(message, dict):
                            message = {
                                "type": message_type,
                                "data": message,
                                "timestamp": datetime.utcnow().isoformat()
                            }
                            message = json.dumps(message)
                        await websocket.send(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to client {connection_id}: {str(e)}")

    async def disconnect_client(self, connection_id: str) -> None:
        """
        Disconnect a client WebSocket connection.
        
        Args:
            connection_id: Client connection identifier
        """
        if connection_id in self.client_tasks:
            self.client_tasks[connection_id].cancel()
            try:
                await self.client_tasks[connection_id]
            except asyncio.CancelledError:
                pass
            del self.client_tasks[connection_id]
        
        if connection_id in self.client_connections:
            websocket = self.client_connections[connection_id]
            try:
                await websocket.close()
            except Exception as e:
                logger.error(f"Error closing client connection {connection_id}: {str(e)}")
            del self.client_connections[connection_id]
            
        logger.debug(f"Disconnected client connection: {connection_id}")

    async def _cleanup_websockets(self) -> None:
        """Clean up all active WebSocket connections (both server and client)."""
        # Clean up server connections
        server_tasks = []
        for websocket in self.active_websockets:
            try:
                server_tasks.append(websocket.close())
            except Exception as e:
                logger.error(f"Error closing server websocket: {str(e)}")
        
        # Clean up client connections
        client_tasks = []
        for connection_id, websocket in self.client_connections.items():
            try:
                if not websocket.closed:
                    client_tasks.append(websocket.close())
            except Exception as e:
                logger.error(f"Error closing client websocket {connection_id}: {str(e)}")
        
        # Cancel client tasks
        for task_id, task in self.client_tasks.items():
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    logger.debug(f"Cancelled client task {task_id}")
        
        # Wait for all cleanup tasks to complete
        if server_tasks or client_tasks:
            await asyncio.gather(*server_tasks, *client_tasks, return_exceptions=True)
        
        # Clear all connection tracking
        self.active_websockets.clear()
        self.client_connections.clear()
        self.client_tasks.clear()

    async def heartbeat(self) -> None:
        """Send periodic heartbeat messages to all connections."""
        while True:
            try:
                message = {
                    "type": WebSocketMessageType.HEARTBEAT,
                    "timestamp": datetime.utcnow().isoformat()
                }
                await self.broadcast_all(message, message_type=WebSocketMessageType.HEARTBEAT)
                await asyncio.sleep(self.config.websocket_ping_interval)
            except Exception as e:
                logger.error(f"Error in heartbeat: {str(e)}")
                await asyncio.sleep(1)

    def _execute(self, *args: Any, **kwargs: Any) -> None:
        """
        Execute the FastAPI service by running the uvicorn server.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        host = self.config.host
        port = self.config.port
        
        logger.info(f"Starting {self.name} service at http://{host}:{port}")
        
        # Start the uvicorn server
        uvicorn.run(
            self.app,
            host=self.config.host,
            port=self.config.port,
            reload=self.config.reload,
            workers=self.config.workers if self.config.workers > 1 else None,
            ssl_keyfile=self.config.ssl_keyfile,
            ssl_certfile=self.config.ssl_certfile,
            ssl_ca_certs=self.config.ssl_ca_certs,
            log_level=self.config.log_level.lower(),
        )

    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get the current status of all WebSocket connections.
        
        Returns:
            Dict containing connection status information
        """
        return {
            "server_connections": {
                "count": len(self.active_websockets),
                "connections": [str(ws.client) for ws in self.active_websockets]
            },
            "client_connections": {
                "count": len(self.client_connections),
                "connections": list(self.client_connections.keys())
            }
        }

    def get_service_info(self) -> Dict[str, Any]:
        """
        Get comprehensive service information.
        
        Returns:
            Dict containing service information
        """
        return {
            "name": self.name,
            "version": self.config.version,
            "environment": self.config.environment,
            "start_time": self.created_at.isoformat(),
            "config": {
                k: v for k, v in self.config.items()
                if k not in ["secrets", "credentials", "keys", "ssl_keyfile", "ssl_certfile", "ssl_ca_certs"]
            },
            "connections": self.get_connection_status(),
            "endpoints": {
                "http": [
                    {
                        "path": route.path,
                        "methods": list(route.methods) if hasattr(route, 'methods') else None,
                        "name": route.name,
                        "response_model": str(route.response_model) if hasattr(route, 'response_model') else None
                    }
                    for route in self.app.routes
                    if not str(route.path).endswith("/ws")
                ],
                "websocket": [
                    {
                        "path": route.path,
                        "name": route.name
                    }
                    for route in self.app.routes
                    if str(route.path).endswith("/ws")
                ]
            },
            "health": {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "server_connections": len(self.active_websockets),
                "client_connections": len(self.client_connections)
            }
        }

    def run(self) -> None:
        """
        Run the service. This method initializes and executes the service.
        """
        try:
            self.initialize()
            self._execute()
        except Exception as e:
            logger.error(f"Service execution failed: {str(e)}")
            raise
        finally:
            self.shutdown()

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """
        Make the service callable. Equivalent to calling run().
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        self.run()

if __name__ == "__main__":
    # Example usage
    config = ServiceConfig(
        host="localhost",
        port=8000,
        api_prefix="/api/v1",
        environment="development",
        version="1.0.0",
        cors_origins=["*"],
        websocket_ping_interval=30,
        max_message_size=10 * 1024 * 1024,  # 10MB
        log_level="info",
        reload=True
    )
    
    service = FastAPIService(
        name="ExampleAPI",
        config=config
    )
    
    service.run()