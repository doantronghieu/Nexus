from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Nuxt.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection opened")
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Print received message
            logger.info(f"Received message: {data}")
            print(f"Received text: {data}")  # Direct console print
            
            # Broadcast message to all connected clients
            for connection in active_connections:
                await connection.send_text(f"Message received: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)
        logger.info("WebSocket connection closed")

# Optional: Regular HTTP endpoint for testing
@app.get("/")
async def root():
    return {"message": "WebSocket server is running"}