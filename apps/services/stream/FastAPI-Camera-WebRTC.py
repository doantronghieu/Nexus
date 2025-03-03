import asyncio
import json
import os
import socket
import time
import platform
import psutil
from datetime import datetime
from pathlib import Path

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, DefaultDict, Set, List
import logging
import aiofiles
from fastapi import (
    FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException,
    APIRouter
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FRAMES_DIR: str = "frames"
    
    class Config:
        env_file = ".env"

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    uptime: float
    ws_connections: int

class SystemStats(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_streams: int
    total_frames_captured: int

class ServerInfo(BaseModel):
    hostname: str
    platform: str
    internal_ips: List[str]
    cpu_cores: int
    python_version: str
    total_memory: float  # GB
    total_disk: float   # G
    
class ClientInfo(BaseModel):
    client_id: str
    is_streaming: bool
    last_frame_time: Optional[datetime]
    frames_count: int
    connection_time: datetime

settings = Settings()

start_time = datetime.now()
system_stats = {
    'total_frames': 0,
    'active_streams': 0
}

# Store connected clients
connected_clients: Dict[str, WebSocket] = {}
# Store pending ICE candidates for late connections
ice_candidates: DefaultDict[str, list] = defaultdict(list)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_info: Dict[str, dict] = {}
        
    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.connection_info[client_id] = {
            "connected_at": datetime.now(),
            "last_frame_time": None,
            "frames_count": 0
        }
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            if client_id in self.connection_info:
                del self.connection_info[client_id]
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    def update_client_frame_info(self, client_id: str):
        """
        Update client's frame information when a new frame is received
        """
        if client_id in self.connection_info:
            self.connection_info[client_id]["last_frame_time"] = datetime.now()
            self.connection_info[client_id]["frames_count"] += 1

    async def broadcast_client_update(self, client_id: str,):
        """Broadcast client update to all connected manager clients"""
        client_info = self.connection_info.get(client_id, {})
        client_dir = Path(settings.FRAMES_DIR) / client_id
        frames_count = 0
        if client_dir.exists():
            frames_count = len(list(client_dir.glob("frame_*.jpg")))
        
        update_message = {
            "type": "client_update",
            "client": {
                "client_id": client_id,
                "is_streaming": True,  # Just received a frame
                "last_frame_time": datetime.now().isoformat(),
                "frames_count": frames_count,
                "connection_time": client_info.get("connected_at", datetime.now()).isoformat()
            }
        }
        
        # Broadcast to all connections
        for connection in self.active_connections.values():
            try:
                await connection.send_json(update_message)
            except Exception as e:
                logger.error(f"Error broadcasting update: {e}")
    
    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)
            
    async def broadcast(self, message: dict, exclude: str = None):
        for client_id, connection in self.active_connections.items():
            if client_id != exclude:
                await connection.send_json(message)

manager = ConnectionManager()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/health")
async def health_check() -> HealthResponse:
    """Basic health check endpoint"""
    current_time = datetime.now()
    uptime = (current_time - start_time).total_seconds()
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=current_time.isoformat(),
        uptime=uptime,
        ws_connections=len(connected_clients)
    )

@app.get("/health/system")
async def system_health() -> SystemStats:
    """Detailed system health check"""
    try:
        import psutil
    except ImportError:
        return JSONResponse(
            status_code=501,
            content={"error": "psutil not installed, system stats unavailable"}
        )

    return SystemStats(
        cpu_usage=psutil.cpu_percent(),
        memory_usage=psutil.virtual_memory().percent,
        disk_usage=psutil.disk_usage('/').percent,
        active_streams=len(connected_clients),
        total_frames_captured=system_stats['total_frames']
    )
    
@app.get("/server/info", response_model=ServerInfo)
async def get_server_info():
    """Get detailed server information including internal IP addresses"""
    
    def get_internal_ips() -> List[str]:
        ips = []
        try:
            # Get all network interfaces
            interfaces = psutil.net_if_addrs()
            for interface_name, addresses in interfaces.items():
                for addr in addresses:
                    # Filter for IPv4 addresses and exclude loopback
                    if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                        ips.append(addr.address)
        except Exception as e:
            logger.error(f"Error getting network interfaces: {e}")
        return ips

    try:
        # Get system memory in GB
        memory_gb = psutil.virtual_memory().total / (1024 * 1024 * 1024)
        
        # Get total disk space in GB
        disk_gb = psutil.disk_usage('/').total / (1024 * 1024 * 1024)
        
        return ServerInfo(
            hostname=socket.gethostname(),
            platform=platform.platform(),
            internal_ips=get_internal_ips(),
            cpu_cores=psutil.cpu_count(logical=True),
            python_version=platform.python_version(),
            total_memory=round(memory_gb, 2),
            total_disk=round(disk_gb, 2)
        )
    except Exception as e:
        logger.error(f"Error getting server info: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve server information"
        )
        
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    try:
        await manager.connect(client_id, websocket)
        system_stats['active_streams'] += 1
        
        logger.info(f"New WebSocket connection established for client: {client_id}")
        
        try:
            while True:
                message = await websocket.receive_text()
                data = json.loads(message)
                logger.info(f"Received message from {client_id}: {data['type']}")
                
                if data["type"] == "heartbeat" or data["type"] == "status_request":
                    # Send current system status
                    current_time = datetime.now()
                    uptime = (current_time - start_time).total_seconds()
                    
                    await websocket.send_json({
                        "type": "health_update",
                        "version": "1.0.0",
                        "timestamp": current_time.isoformat(),
                        "uptime": uptime,
                        "ws_connections": len(manager.active_connections),
                        "system_stats": {
                            "cpu_usage": psutil.cpu_percent(),
                            "memory_usage": psutil.virtual_memory().percent,
                            "disk_usage": psutil.disk_usage('/').percent,
                            "active_streams": len(manager.active_connections),
                            "total_frames": system_stats['total_frames']
                        }
                    })
                
                elif data["type"] == "offer":
                    # Handle WebRTC offer
                    await manager.broadcast(
                        {
                            "type": "offer",
                            "offer": data["offer"],
                            "clientId": client_id
                        },
                        exclude=client_id
                    )
                    
                elif data["type"] == "answer":
                    # Handle WebRTC answer
                    if "targetId" in data:
                        await manager.send_personal_message(
                            {
                                "type": "answer",
                                "answer": data["answer"],
                                "clientId": client_id
                            },
                            data["targetId"]
                        )
                        
                elif data["type"] == "ice-candidate":
                    # Handle ICE candidate
                    if "targetId" in data:
                        await manager.send_personal_message(
                            {
                                "type": "ice-candidate",
                                "candidate": data["candidate"],
                                "clientId": client_id
                            },
                            data["targetId"]
                        )
                    
        except WebSocketDisconnect:
            logger.info(f"WebSocket connection closed for client: {client_id}")
            system_stats['active_streams'] -= 1
            manager.disconnect(client_id)
            # Notify other clients about disconnection
            await manager.broadcast(
                {
                    "type": "client-disconnected",
                    "clientId": client_id
                },
                exclude=client_id
            )
            
    except Exception as e:
        logger.error(f"Error in websocket connection: {str(e)}")
        system_stats['active_streams'] = max(0, system_stats['active_streams'] - 1)
        manager.disconnect(client_id)
        
@app.websocket("/ws/health-check")
async def health_check_ws(websocket: WebSocket):
    try:
        client_id = "health-check"
        await manager.connect(client_id, websocket)
        
        logger.info(f"Health check WebSocket connection established")
        
        try:
            while True:
                message = await websocket.receive_text()
                data = json.loads(message)
                
                if data["type"] == "heartbeat":
                    # Respond to heartbeat with current health status
                    current_time = datetime.now()
                    uptime = (current_time - start_time).total_seconds()
                    
                    await websocket.send_json({
                        "type": "health_update",
                        "status": "healthy",
                        "version": "1.0.0",
                        "timestamp": current_time.isoformat(),
                        "uptime": uptime,
                        "ws_connections": len(connected_clients),
                        "system_stats": {
                            "cpu_usage": psutil.cpu_percent(),
                            "memory_usage": psutil.virtual_memory().percent,
                            "disk_usage": psutil.disk_usage('/').percent,
                            "active_streams": len(connected_clients),
                            "total_frames": system_stats['total_frames']
                        }
                    })
                    
        except WebSocketDisconnect:
            logger.info(f"Health check WebSocket connection closed")
            manager.disconnect(client_id)
            
    except Exception as e:
        logger.error(f"Error in health check websocket: {str(e)}")
        manager.disconnect("health-check")

@app.get("/manager/clients")
async def get_connected_clients():
    """Get list of all connected clients with their status"""
    clients_info = []
    for client_id in manager.active_connections:
        client_info = manager.connection_info.get(client_id, {})
        
        # Get frame information
        client_dir = Path(settings.FRAMES_DIR) / client_id
        frames_count = 0
        if client_dir.exists():
            frames_count = len(list(client_dir.glob("frame_*.jpg")))
        
        # Check if client is streaming (received frame in last 5 seconds)
        last_frame_time = client_info.get("last_frame_time")
        is_streaming = False
        if last_frame_time:
            time_diff = (datetime.now() - last_frame_time).total_seconds()
            is_streaming = time_diff < 5

        clients_info.append({
            "client_id": client_id,
            "is_streaming": is_streaming,
            "last_frame_time": last_frame_time.isoformat() if last_frame_time else None,
            "frames_count": frames_count,
            "connection_time": client_info.get("connected_at").isoformat()
        })
    
    return clients_info

@app.get("/manager/clients/{client_id}/latest-frame")
async def get_client_latest_frame(client_id: str):
    """Get the latest frame for a specific client"""
    client_dir = Path(settings.FRAMES_DIR) / client_id
    
    if not client_dir.exists():
        raise HTTPException(status_code=404, detail="No frames found for this client")
    
    # Get all frames and sort by timestamp (newest first)
    frames = list(client_dir.glob("frame_*.jpg"))
    if not frames:
        raise HTTPException(status_code=404, detail="No frames found for this client")
    
    frames.sort(reverse=True)
    latest_frame = frames[0]
    
    return FileResponse(latest_frame)

@app.post("/save-frame/{client_id}")
async def save_frame(client_id: str, frame: UploadFile = File(...)):
    """Save a single frame for a specific client"""
    try:
        # Use a default folder if client_id is undefined or invalid
        safe_client_id = "default" if client_id in ["undefined", "null", ""] else client_id
        
        # Create client directory if it doesn't exist
        client_dir = Path(settings.FRAMES_DIR) / safe_client_id
        client_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = client_dir / f"frame_{timestamp}.jpg"
        
        # Save the frame
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await frame.read()
            await out_file.write(content)
        
        await manager.broadcast_client_update(client_id)
        
        logger.info(f"Frame saved for client {safe_client_id}: {file_path}")
        
        return {
            "status": "success",
            "message": "Frame saved successfully",
            "file_path": str(file_path),
            "timestamp": timestamp
        }
        
    except Exception as e:
        logger.error(f"Error saving frame for client {safe_client_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save frame: {str(e)}"
        )
        
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        ssl_keyfile="./certs/key.pem",
        ssl_certfile="./certs/cert.pem",
    )