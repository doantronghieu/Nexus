from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import logging
from collections import deque
import os
from datetime import datetime
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
AUDIO_DIR = "audio_chunks"
MAX_CHUNKS = 5

class AudioChunkManager:
    def __init__(self, directory=AUDIO_DIR, max_chunks=MAX_CHUNKS):
        self.directory = directory
        self.max_chunks = max_chunks
        os.makedirs(directory, exist_ok=True)
        
    def cleanup_old_chunks(self):
        """Remove all but the latest N chunks from the directory"""
        # Get list of all chunk files
        pattern = os.path.join(self.directory, "chunk_*.wav")
        chunks = glob.glob(pattern)
        
        # Sort by creation time (newest first)
        chunks.sort(key=os.path.getctime, reverse=True)
        
        # Remove old chunks
        for chunk in chunks[self.max_chunks:]:
            try:
                os.remove(chunk)
                logger.debug(f"Removed old chunk: {chunk}")
            except Exception as e:
                logger.error(f"Error removing chunk {chunk}: {e}")
    
    def save_chunk(self, data):
        """Save a new chunk and cleanup old ones"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        chunk_path = os.path.join(self.directory, f"chunk_{timestamp}.wav")
        
        try:
            with open(chunk_path, "wb") as f:
                f.write(data)
            logger.debug(f"Saved new chunk: {chunk_path}")
            
            # Clean up after saving new chunk
            self.cleanup_old_chunks()
            
            return chunk_path
        except Exception as e:
            logger.error(f"Error saving chunk: {e}")
            return None
    
    def get_current_chunks(self):
        """Get list of current chunk files"""
        pattern = os.path.join(self.directory, "chunk_*.wav")
        chunks = glob.glob(pattern)
        chunks.sort(key=os.path.getctime, reverse=True)
        return chunks[:self.max_chunks]

# Dictionary to store audio buffers for each client
client_buffers = {}
# Create audio chunk manager
chunk_manager = AudioChunkManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Create a buffer for this client
    client_id = id(websocket)
    client_buffers[client_id] = deque(maxlen=MAX_CHUNKS)
    
    logger.info(f"WebSocket connection opened. Client ID: {client_id}")
    
    try:
        while True:
            # Receive the binary audio data
            data = await websocket.receive_bytes()
            
            # Store in memory buffer
            client_buffers[client_id].append(data)
            
            # Save to file and cleanup old files
            saved_path = chunk_manager.save_chunk(data)
            
            if saved_path:
                current_chunks = chunk_manager.get_current_chunks()
                logger.info(f"Active chunks: {len(current_chunks)}/{MAX_CHUNKS}")
                logger.info(f"Latest chunk saved: {os.path.basename(saved_path)}")
            
            # Send acknowledgment back to client
            await websocket.send_text("Audio chunk received")
            
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
    finally:
        # Clean up when client disconnects
        if client_id in client_buffers:
            del client_buffers[client_id]
        logger.info(f"WebSocket connection closed. Client ID: {client_id}")

@app.get("/")
async def root():
    return {"message": "WebSocket Audio server is running"}

# Add endpoint to get current chunks info
@app.get("/chunks")
async def get_chunks():
    chunks = chunk_manager.get_current_chunks()
    return {
        "total_chunks": len(chunks),
        "chunks": [os.path.basename(chunk) for chunk in chunks]
    }

# uvicorn audio:app --reload