import asyncio
from fastapi import FastAPI, status, Request, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any, List, Literal, Union, Tuple, Optional
import json
from loguru import logger
import time
import uuid
from faker import Faker
import base64
import os
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np

# Configure loguru logger with emojis for better readability
logger.remove()  # Remove default handler
logger.add(
    sink=lambda msg: print(msg),
    format="<green>{time:HH:mm:ss}</green> | {message}",
    colorize=True,
    enqueue=True,
)

app = FastAPI(
    title="Stream Service",
    description="Stream Service API",
    version="1.0.0"
)

# Configure CORS middleware with more specific settings for ngrok
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Create frames directory if it doesn't exist
FRAMES_DIR = Path("frames")
FRAMES_DIR.mkdir(exist_ok=True)

# Constants
STREAMING_TIMEOUT = 5  # Seconds without frames before considering stream inactive

class StreamMetrics:
    def __init__(self):
        self.frame_count = 0
        self.start_time = None
        self.last_update_time = time.time()
        self.fps = 0

    def update(self, is_streaming: bool = True):
        current_time = time.time()
        if is_streaming:
            if not self.start_time:
                self.start_time = current_time
            self.frame_count += 1
            duration = current_time - self.start_time
            if duration > 0:
                self.fps = round(self.frame_count / duration, 1)
        else:
            self.frame_count = 0
            self.start_time = None
            self.fps = 0
        self.last_update_time = current_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "frame_count": self.frame_count,
            "start_time": self.start_time,
            "fps": self.fps,
            "last_update_time": self.last_update_time
        }

def generate_readable_uuid(
    mode: Literal["full", "uuid", "name", "readable"] = "full"
) -> Union[str, Tuple[str, str, str]]:
    """
    Generate a unique readable identifier combining UUID and a fake name.
    """
    fake = Faker()
    
    unique_id = str(uuid.uuid4())
    random_name = fake.name().replace(' ', '_').lower()
    readable_identifier = f"{random_name}_{unique_id[:8]}"
    
    if mode == "uuid":
        return unique_id
    elif mode == "name":
        return random_name
    elif mode == "readable":
        return readable_identifier
    elif mode == "full":
        return unique_id, random_name, readable_identifier
    else:
        valid_modes = ["full", "uuid", "name", "readable"]
        raise ValueError(f"Invalid mode. Valid modes are: {valid_modes}")

def save_frame(frame_data: str, client_id: str, timestamp: str = None) -> str:
    """
    Save a base64 encoded frame to the frames directory.
    Returns the saved file path.
    """
    try:
        # Remove the data URL prefix if present
        if frame_data.startswith('data:image/'):
            frame_data = frame_data.split(',')[1]
            
        # Decode base64 data
        image_data = base64.b64decode(frame_data)
        
        # Create client directory if it doesn't exist
        client_dir = FRAMES_DIR / client_id
        client_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        if not timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"frame_{timestamp}.jpg"
        filepath = client_dir / filename
        
        # Save the image
        with open(filepath, "wb") as f:
            f.write(image_data)
            
        logger.info(f"📸 Frame saved | Client: {client_id} | File: {filename}")
        return str(filepath)
    except Exception as e:
        logger.error(f"🚨 Error saving frame: {str(e)}")
        raise

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # client_id -> WebSocket
        self.start_time: float = time.time()
        self.client_info: Dict[str, Dict[str, Any]] = {}
        self.stream_monitoring_task = None
        self.stream_metrics: Dict[str, StreamMetrics] = {}
        self.disconnect_events: Dict[str, asyncio.Event] = {}

    @property
    def uptime(self) -> float:
        return time.time() - self.start_time

    async def broadcast_metrics(self, client_id: str):
        """
        Broadcast stream metrics to all connected clients
        """
        if client_id in self.stream_metrics and client_id in self.client_info:
            metrics = self.stream_metrics[client_id].to_dict()
            metrics_data = {
                "type": "metrics_update",
                "client_id": client_id,
                "frame_count": metrics["frame_count"],
                "fps": metrics["fps"],
                "start_time": metrics["start_time"],
                "is_streaming": self.client_info[client_id]["is_streaming"]
            }

            disconnected = []
            for cid, websocket in self.active_connections.items():
                try:
                    await websocket.send_json(metrics_data)
                except Exception as e:
                    logger.error(f"🚨 Metrics broadcast error for client {cid}: {str(e)}")
                    disconnected.append(cid)

            # Clean up disconnected clients
            for cid in disconnected:
                await self.disconnect(cid)

    async def connect(self, websocket: WebSocket, client_name: Optional[str] = None) -> str:
        await websocket.accept()
        
        # Generate client identifier
        if client_name:
            unique_id = str(uuid.uuid4())[:8]
            client_id = f"{client_name}_{unique_id}"
        else:
            _, _, client_id = generate_readable_uuid(mode="full")
        
        self.active_connections[client_id] = websocket
        self.client_info[client_id] = {
            "id": client_id,
            "display_name": client_name or client_id.split('_')[0],
            "connected_at": time.time(),
            "message_count": 0,
            "frames_captured": 0,
            "is_streaming": False
        }
        self.stream_metrics[client_id] = StreamMetrics()
        self.disconnect_events[client_id] = asyncio.Event()

        # Start stream monitoring if not already running
        if not self.stream_monitoring_task:
            self.stream_monitoring_task = asyncio.create_task(self.monitor_streams())
        
        logger.info(f"🔌 WS connect | {client_id} | Active clients: {len(self.active_connections)}")
        
        # Notify client of their assigned ID
        await websocket.send_json({
            "type": "client_info",
            "client_id": client_id,
            "display_name": self.client_info[client_id]["display_name"]
        })
        
        # Send current streaming status and metrics to new client for all active streams
        for cid, info in self.client_info.items():
            if info["is_streaming"]:
                await self.broadcast_streaming_status(cid, True)
                await self.broadcast_metrics(cid)

        # Broadcast new connection
        await self.broadcast(f"{self.client_info[client_id]['display_name']} joined", "Server")
        return client_id

    async def disconnect(self, client_id: str):
        """
        Handle client disconnection with proper cleanup
        """
        try:
            if client_id in self.client_info:
                client_info = self.client_info[client_id]
                display_name = client_info["display_name"]
                frames_captured = client_info["frames_captured"]
                
                logger.info(f"📊 Disconnect stats | Client: {client_id} | Frames: {frames_captured}")
                
                # Clean up all client-related data
                if client_id in self.active_connections:
                    del self.active_connections[client_id]
                if client_id in self.client_info:
                    del self.client_info[client_id]
                if client_id in self.stream_metrics:
                    del self.stream_metrics[client_id]
                
                # Signal disconnect event
                if client_id in self.disconnect_events:
                    self.disconnect_events[client_id].set()
                    del self.disconnect_events[client_id]
                    
                logger.info(f"❌ WS disconnect | {client_id} | Active clients: {len(self.active_connections)}")

                # Stop monitoring if no connections left
                if not self.active_connections and self.stream_monitoring_task:
                    self.stream_monitoring_task.cancel()
                    self.stream_monitoring_task = None

                # Broadcast disconnect status
                await self.broadcast(f"{display_name} left", "Server")
                await self.broadcast_client_disconnect(client_id)

        except Exception as e:
            logger.error(f"🚨 Error during client disconnect: {str(e)}")

    async def broadcast(self, message: str, sender_id: str):
        """
        Broadcast a message to all connected clients
        """
        logger.info(f"📢 Broadcast | From: {sender_id} | Msg: {message}")
        disconnected = []

        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json({
                    "type": "message",
                    "sender": sender_id,
                    "content": message
                })
            except WebSocketDisconnect:
                disconnected.append(client_id)
                logger.warning(f"⚠️ Client {client_id} dropped during broadcast")
            except Exception as e:
                logger.error(f"🚨 Broadcast error for client {client_id}: {str(e)}")
                disconnected.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected:
            await self.disconnect(client_id)

    async def broadcast_frame(self, frame_data: Dict, sender_id: str):
        """
        Broadcast frame data to all connected clients except the sender
        """
        if sender_id in self.client_info:
            disconnected = []

            # Update metrics for the sender
            if sender_id in self.stream_metrics:
                self.stream_metrics[sender_id].update()
                await self.broadcast_metrics(sender_id)

            for client_id, websocket in self.active_connections.items():
                if client_id != sender_id:
                    try:
                        await websocket.send_json({
                            "type": "frame",
                            "sender_id": sender_id,
                            "content": frame_data["content"],
                            "timestamp": frame_data.get("timestamp", datetime.now().isoformat()),
                            "is_stream": frame_data.get("isStream", False)
                        })
                    except Exception as e:
                        logger.error(f"🚨 Frame broadcast error for client {client_id}: {str(e)}")
                        disconnected.append(client_id)

            # Clean up disconnected clients
            for client_id in disconnected:
                await self.disconnect(client_id)

    async def broadcast_streaming_status(self, client_id: str, is_streaming: bool):
        """
        Broadcast a client's streaming status to all connected clients
        """
        disconnected = []
        
        # Update metrics for streaming status change
        if client_id in self.stream_metrics:
            metrics = self.stream_metrics[client_id]
            if not is_streaming:
                metrics = StreamMetrics()  # Reset metrics when stopping stream
            self.stream_metrics[client_id] = metrics

        for cid, websocket in self.active_connections.items():
            try:
                await websocket.send_json({
                    "type": "streaming_status",
                    "client_id": client_id,
                    "is_streaming": is_streaming
                })
            except Exception as e:
                logger.error(f"🚨 Streaming status broadcast error for client {cid}: {str(e)}")
                disconnected.append(cid)

        # Clean up disconnected clients
        for cid in disconnected:
            await self.disconnect(cid)

    async def broadcast_client_disconnect(self, client_id: str):
        """
        Broadcast client disconnection to all remaining clients
        """
        disconnected = []
        for cid, websocket in self.active_connections.items():
            try:
                await websocket.send_json({
                    "type": "client_disconnect",
                    "client_id": client_id
                })
            except Exception as e:
                logger.error(f"🚨 Client disconnect broadcast error for client {cid}: {str(e)}")
                disconnected.append(cid)

        # Clean up any newly disconnected clients
        for cid in disconnected:
            await self.disconnect(cid)

    async def monitor_streams(self):
        """
        Monitor stream activity and update streaming status
        """
        while True:
            try:
                current_time = time.time()
                for client_id in list(self.stream_metrics.keys()):
                    if client_id in self.client_info:
                        metrics = self.stream_metrics[client_id]
                        was_streaming = self.client_info[client_id]["is_streaming"]
                        
                        # Check if stream is inactive
                        if current_time - metrics.last_update_time > STREAMING_TIMEOUT:
                            if client_id in self.client_info:  # Double-check client still exists
                                self.client_info[client_id]["is_streaming"] = False
                                if was_streaming:  # Only broadcast if status changed
                                    await self.broadcast_streaming_status(client_id, False)
                                    await self.broadcast_metrics(client_id)
                                    logger.info(f"🎥 Stream timeout | Client: {client_id}")

                await asyncio.sleep(1)  # Check every second
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"🚨 Stream monitoring error: {str(e)}")
                await asyncio.sleep(1)  # Continue monitoring even after error

    async def handle_frame(self, client_id: str, frame_data: Dict):
        """
        Handle incoming frame data from a client
        """
        try:
            if client_id not in self.client_info:
                return

            # Save the frame
            filepath = save_frame(
                frame_data["content"],
                client_id,
                frame_data.get("timestamp")
            )
            
            # Update stats
            self.client_info[client_id]["frames_captured"] += 1
            was_streaming = self.client_info[client_id]["is_streaming"]
            self.client_info[client_id]["is_streaming"] = True
            
            # Send confirmation back to client
            websocket = self.active_connections.get(client_id)
            if websocket:
                await websocket.send_json({
                    "type": "frame_saved",
                    "filepath": filepath,
                    "frame_number": self.client_info[client_id]["frames_captured"]
                })

            # Update and broadcast metrics
            if client_id in self.stream_metrics:
                self.stream_metrics[client_id].update(True)
                await self.broadcast_metrics(client_id)

            # Broadcast frame to other clients
            await self.broadcast_frame(frame_data, client_id)

            # Broadcast streaming status if changed
            if not was_streaming:
                await self.broadcast_streaming_status(client_id, True)
                logger.info(f"🎥 Stream started | Client: {client_id}")

        except Exception as e:
            logger.error(f"🚨 Frame handling error: {str(e)}")
            if websocket := self.active_connections.get(client_id):
                await websocket.send_json({
                    "type": "frame_error",
                    "message": str(e)
                })

    def increment_message_count(self, client_id: str):
        """
        Increment message count for a client
        """
        if client_id in self.client_info:
            self.client_info[client_id]["message_count"] += 1

    def get_connection_stats(self) -> Dict[str, Any]:
        """
        Get current connection statistics
        """
        return {
            "active_connections": len(self.active_connections),
            "uptime_seconds": round(self.uptime, 2),
            "clients": [
                {
                    "id": info["id"],
                    "display_name": info["display_name"],
                    "connected_for": round(time.time() - info["connected_at"], 2),
                    "message_count": info["message_count"],
                    "frames_captured": info["frames_captured"],
                    "is_streaming": info["is_streaming"]
                }
                for info in self.client_info.values()
            ]
        }

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_name: Optional[str] = Query(None)
):
    """
    WebSocket endpoint for real-time communication
    """
    client_id = None
    try:
        # Connect and get client ID
        client_id = await manager.connect(websocket, client_name)
        
        while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Handle frame capture
                if message_data.get("type") == "frame":
                    await manager.handle_frame(client_id, message_data)
                    continue
                
                # Handle regular messages
                manager.increment_message_count(client_id)
                
                if client_id in manager.client_info:
                    display_name = manager.client_info[client_id]["display_name"]
                    await manager.broadcast(data, display_name)
                else:
                    logger.warning(f"⚠️ Message received from unknown client: {client_id}")

            except json.JSONDecodeError:
                # Handle plain text messages
                if client_id in manager.client_info:
                    display_name = manager.client_info[client_id]["display_name"]
                    manager.increment_message_count(client_id)
                    await manager.broadcast(data, display_name)
                else:
                    logger.warning(f"⚠️ Text message received from unknown client: {client_id}")

    except WebSocketDisconnect:
        if client_id:
            await manager.disconnect(client_id)
            
    except Exception as e:
        logger.error(f"💥 WS error for client {client_id}: {str(e)}")
        if client_id:
            await manager.disconnect(client_id)

@app.get(
    "/ws/stats",
    summary="WebSocket Statistics",
    description="Get current WebSocket connection statistics",
    response_description="Returns WebSocket statistics including active connections and client information",
    status_code=status.HTTP_200_OK,
)
async def websocket_stats() -> JSONResponse:
    """
    Get WebSocket connection statistics
    """
    logger.debug("📊 WS stats requested")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=manager.get_connection_stats()
    )

@app.get(
    "/health",
    summary="Health Check",
    description="Endpoint to check if the service is healthy",
    response_description="Returns the health status of the service",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
)
async def health_check(request: Request) -> JSONResponse:
    """
    Performs a health check of the service.
    """
    logger.debug("💓 Health check")
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-cache",
        "Ngrok-Skip-Browser-Warning": "true"
    }
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "app": "Main APIs",
        },
        headers=headers
    )

@app.get("/")
async def root(request: Request) -> JSONResponse:
    """
    Root endpoint that returns the same response as health check.
    """
    logger.debug("🏠 Root access")
    return await health_check(request)

def get_server_config() -> Dict[str, Any]:
    """
    Get server configuration parameters.
    """
    return {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "workers": 1,
        "log_level": "info"
    }

def main() -> None:
    """
    Main function to start the FastAPI server with the specified configuration.
    """
    logger.info("🚀 Starting server")
    config = get_server_config()
    logger.info(f"⚙️ Config: {config}")
    uvicorn.run(
        "server:app",
        host=config["host"],
        port=config["port"],
        reload=config["reload"],
        workers=config["workers"],
        log_level=config["log_level"]
    )

if __name__ == "__main__":
    main()