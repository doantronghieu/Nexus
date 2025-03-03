import asyncio
from abc import ABC, abstractmethod
from fastapi import FastAPI, status, Request, WebSocket, WebSocketDisconnect, Query, File, UploadFile
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
import json
import time
import uuid
from faker import Faker
import base64
import os
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create frames directories if they don't exist
FRAMES_DIR = Path("frames")
PROCESSED_FRAMES_DIR = Path("processed_frames")
FRAMES_DIR.mkdir(exist_ok=True)
PROCESSED_FRAMES_DIR.mkdir(exist_ok=True)

class ImageProcessor(ABC):
    """Abstract base class for image processing operations."""
    
    @abstractmethod
    async def process(self, image_bytes: bytes, save_dir: Path, client_id: str, timestamp: str | None = None) -> Tuple[bytes, str]:
        """
        Process the input image and save it to the specified directory.
        
        Args:
            image_bytes: Raw image bytes
            save_dir: Directory to save the processed image
            client_id: Client identifier for directory organization
            timestamp: Optional timestamp for the image
            
        Returns:
            Tuple[bytes, str]: Processed image bytes and the saved filepath
        """
        pass
    
    def _decode_image(self, image_bytes: bytes) -> np.ndarray:
        """Decode image bytes to numpy array."""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image")
        
        return img
    
    def _encode_image(self, img: np.ndarray, format: str = '.png') -> bytes:
        """Encode numpy array to image bytes."""
        _, processed_img = cv2.imencode(format, img)
        if processed_img is None:
            raise ValueError("Failed to encode image")
        return processed_img.tobytes()
    
    def _save_image(self, image_bytes: bytes, save_dir: Path, client_id: str, timestamp: str | None = None) -> str:
        """Save image to the specified directory."""
        try:
            # Create client directory if it doesn't exist
            client_dir = save_dir / client_id
            client_dir.mkdir(exist_ok=True)
            
            # Generate filename with timestamp
            if not timestamp:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"frame_{timestamp}.jpg"
            filepath = client_dir / filename
            
            # Save the image
            with open(filepath, "wb") as f:
                f.write(image_bytes)
                
            logger.info(f"📸 Frame saved | Client: {client_id} | File: {filename}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"🚨 Error saving frame: {str(e)}")
            raise

class BasicImageProcessor(ImageProcessor):
    """Basic image processor that draws a rectangle and saves the processed image."""
    
    async def process(self, image_bytes: bytes, save_dir: Path, client_id: str, timestamp: str | None = None) -> Tuple[bytes, str]:
        try:
            # Decode and process the image
            img = self._decode_image(image_bytes)
            
            # Get image dimensions
            height, width = img.shape[:2]
            
            # Calculate center rectangle coordinates
            rect_width = width // 3
            rect_height = height // 3
            x1 = (width - rect_width) // 2
            y1 = (height - rect_height) // 2
            x2 = x1 + rect_width
            y2 = y1 + rect_height
            
            # Draw rectangle
            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                color=(0, 255, 0),  # Green color
                thickness=2
            )
            
            # Add timestamp
            cv2.putText(
                img,
                f"Processed: {datetime.now().strftime('%H:%M:%S')}",
                (10, height - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )
            
            # Encode the processed image
            processed_bytes = self._encode_image(img)
            
            # Save the processed image
            saved_path = self._save_image(processed_bytes, save_dir, client_id, timestamp)
            
            return processed_bytes, saved_path
            
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise ValueError(f"Image processing failed: {str(e)}")

class MLConnectionManager:
    """Manages WebSocket connections and message broadcasting for ML processing."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.server_connection: Optional[WebSocket] = None
        self.client_info: Dict[str, Dict[str, Any]] = {}
        self.start_time = datetime.now()
        self.processor = BasicImageProcessor()
        self.stream_metrics: Dict[str, Dict[str, Any]] = {}
        self.last_stream_update: Dict[str, float] = {}
        self.stream_check_interval: Optional[asyncio.Task] = None
        self.stream_check_interval = None

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get current connection statistics."""
        return {
            "active_connections": len(self.active_connections),
            "server_connected": self.server_connection is not None,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "clients": [
                {
                    "id": client_id,
                    "info": info
                }
                for client_id, info in self.client_info.items()
            ]
        }

    async def connect_client(self, websocket: WebSocket, client_name: Optional[str] = None) -> str:
        """Connect a new client WebSocket."""
        await websocket.accept()
        
        # Generate client ID and name
        if client_name:
            unique_id = str(uuid.uuid4())[:8]
            client_id = f"{client_name}_{unique_id}"
        else:
            fake = Faker()
            client_id = f"ml_client_{fake.uuid4()[:8]}"
            client_name = client_id
            
        # Store connection
        self.active_connections[client_id] = websocket
        self.client_info[client_id] = {
            "name": client_name,
            "connected_at": datetime.now().isoformat(),
            "processed_frames": 0,
            "is_streaming": False,
            "is_server": False
        }
        
        logger.info(f"ML Client connected: {client_id}")
        
        # Send connection confirmation
        await websocket.send_json({
            "type": "connection_info",
            "client_id": client_id,
            "name": client_name
        })
        
        return client_id

    async def connect_server(self, websocket: WebSocket) -> None:
        """Connect the main server WebSocket."""
        await websocket.accept()
        self.server_connection = websocket
        
        # Generate server client info
        server_id = f"ml_server_{uuid.uuid4()[:8]}"
        self.client_info[server_id] = {
            "name": "ML Server",
            "connected_at": datetime.now().isoformat(),
            "processed_frames": 0,
            "is_streaming": False,
            "is_server": True
        }
        
        logger.info("Main server connected to ML WebSocket")
        
        await websocket.send_json({
            "type": "connection_info",
            "status": "connected",
            "message": "ML Server WebSocket connected"
        })

    async def disconnect_client(self, client_id: str) -> None:
        """Disconnect a client and clean up resources."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.client_info:
            del self.client_info[client_id]
        if client_id in self.stream_metrics:
            del self.stream_metrics[client_id]
        if client_id in self.last_stream_update:
            del self.last_stream_update[client_id]
            
        logger.info(f"ML Client disconnected: {client_id}")

    async def disconnect_server(self) -> None:
        """Disconnect the main server connection."""
        self.server_connection = None
        logger.info("Main server disconnected from ML WebSocket")

    async def broadcast_to_clients(self, message: Dict[str, Any]) -> None:
        """Broadcast a message to all connected clients."""
        disconnected_clients = []
        
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client {client_id}: {str(e)}")
                disconnected_clients.append(client_id)
                
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            await self.disconnect_client(client_id)

    async def process_frame(self, frame_data: str, client_id: str, timestamp: str | None = None) -> Tuple[bytes, str]:
        """Process a frame and save it."""
        try:
            # Extract frame data
            if frame_data.startswith('data:image/'):
                frame_data = frame_data.split(',')[1]
                
            # Decode base64 data
            image_bytes = base64.b64decode(frame_data)
            
            # Process the frame
            processed_bytes, saved_path = await self.processor.process(
                image_bytes,
                PROCESSED_FRAMES_DIR,
                client_id,
                timestamp
            )
            
            # Update metrics
            if client_id in self.client_info:
                self.client_info[client_id]["processed_frames"] += 1
                self.client_info[client_id]["is_streaming"] = True
                self.last_stream_update[client_id] = time.time()
            
            return processed_bytes, saved_path
            
        except Exception as e:
            logger.error(f"Frame processing error: {str(e)}")
            raise

# Initialize FastAPI app
app = FastAPI(
    title="Machine Learning Processing API",
    description="API for processing images with ML capabilities",
    version="1.0.0",
    root_path="/ml",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize connection manager
manager = MLConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_name: Optional[str] = Query(None)
):
    """WebSocket endpoint for clients to connect and receive processed frames."""
    client_id = None
    try:
        client_id = await manager.connect_client(websocket, client_name)
        
        while True:
            try:
                # Wait for messages
                message = await websocket.receive_text()
                data = json.loads(message)
                
                # Process different message types
                if data["type"] == "frame":
                    try:
                        # Process frame
                        processed_bytes, saved_path = await manager.process_frame(
                            data["content"],
                            client_id,
                            data.get("timestamp")
                        )
                        
                        # Convert processed frame to base64
                        processed_base64 = base64.b64encode(processed_bytes).decode()
                        
                        # Send processed frame back to sender
                        await websocket.send_json({
                            "type": "processed_frame",
                            "client_id": client_id,
                            "content": f"data:image/png;base64,{processed_base64}",
                            "timestamp": data.get("timestamp", datetime.now().isoformat())
                        })
                        
                        # Broadcast processed frame to all clients except sender
                        for other_id, other_socket in manager.active_connections.items():
                            if other_id != client_id:
                                try:
                                    await other_socket.send_json({
                                        "type": "processed_frame",
                                        "client_id": client_id,
                                        "content": f"data:image/png;base64,{processed_base64}",
                                        "timestamp": data.get("timestamp", datetime.now().isoformat())
                                    })
                                except Exception:
                                    pass
                        
                    except Exception as e:
                        logger.error(f"Frame processing error: {str(e)}")
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Frame processing failed: {str(e)}"
                        })
                            
                elif data["type"] == "metrics_request":
                    # Send current metrics
                    if client_id in manager.client_info:
                        await websocket.send_json({
                            "type": "metrics_update",
                            "client_id": client_id,
                            "metrics": {
                                "frameCount": manager.client_info[client_id]["processed_frames"],
                                "fps": calculate_fps(manager.client_info[client_id]),
                                "is_streaming": manager.client_info[client_id]["is_streaming"]
                            }
                        })
                
            except WebSocketDisconnect:
                raise
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
    
    except WebSocketDisconnect:
        if client_id:
            await manager.disconnect_client(client_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        if client_id:
            await manager.disconnect_client(client_id)

@app.websocket("/ws/server")
async def server_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for the main server to connect."""
    try:
        await manager.connect_server(websocket)
        
        while True:
            try:
                # Wait for messages from main server
                message = await websocket.receive_text()
                data = json.loads(message)
                
                # Process different message types
                if data["type"] == "frame":
                    try:
                        # Process frame
                        processed_bytes, saved_path = await manager.process_frame(
                            data["content"],
                            data.get("client_id", "server"),
                            data.get("timestamp")
                        )
                        
                        # Convert processed frame to base64
                        processed_base64 = base64.b64encode(processed_bytes).decode()
                        
                        # Broadcast processed frame
                        await manager.broadcast_to_clients({
                            "type": "processed_frame",
                            "client_id": data.get("client_id", "server"),
                            "content": f"data:image/png;base64,{processed_base64}",
                            "timestamp": data.get("timestamp", datetime.now().isoformat())
                        })
                        
                    except Exception as e:
                        logger.error(f"Frame processing error: {str(e)}")
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Frame processing failed: {str(e)}"
                        })
                
            except WebSocketDisconnect:
                raise
            except Exception as e:
                logger.error(f"Error processing server message: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
                
    except WebSocketDisconnect:
        await manager.disconnect_server()
    except Exception as e:
        logger.error(f"Server WebSocket error: {str(e)}")
        await manager.disconnect_server()

@app.get(
    "/health",
    summary="Health Check",
    description="Endpoint to check if the service is healthy",
    response_description="Returns the health status of the service",
    status_code=status.HTTP_200_OK,
)
async def health_check(request: Request) -> JSONResponse:
    """Performs a health check of the service."""
    logger.info("Health check requested")
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "app": "Machine Learning APIs",
            "connections": manager.get_connection_stats()
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache"
        }
    )

@app.get("/")
async def root(request: Request) -> JSONResponse:
    """Root endpoint that returns the same response as health check."""
    return await health_check(request)

@app.post("/process/basic/")
async def process_image_basic(
    file: UploadFile = File(..., description="Image file to process")
) -> Response:
    """Process an uploaded image using basic image processing."""
    try:
        image_bytes = await file.read()
        processor = BasicImageProcessor()
        processed_bytes, _ = await processor.process(
            image_bytes,
            PROCESSED_FRAMES_DIR,
            "api",
            None
        )
        
        return Response(
            content=processed_bytes,
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Request processing failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Image processing failed: {str(e)}"
        )

def calculate_fps(client_info: Dict[str, Any]) -> float:
    """Calculate the current FPS for a client."""
    try:
        connected_time = (datetime.now() - datetime.fromisoformat(client_info["connected_at"])).total_seconds()
        if connected_time > 0:
            return round(client_info["processed_frames"] / connected_time, 1)
    except Exception:
        pass
    return 0.0

def get_server_config() -> Dict[str, Any]:
    """Get server configuration parameters."""
    return {
        "host": "0.0.0.0",
        "port": 8001,
        "reload": True,
        "workers": 1,
        "log_level": "info"
    }

def main() -> None:
    """Main function to start the FastAPI server with the specified configuration."""
    logger.info("🚀 Starting ML server")
    config = get_server_config()
    logger.info(f"⚙️ Config: {config}")
    uvicorn.run(
        "ml:app",
        host=config["host"],
        port=config["port"],
        reload=config["reload"],
        workers=config["workers"],
        log_level=config["log_level"]
    )

if __name__ == "__main__":
    main()