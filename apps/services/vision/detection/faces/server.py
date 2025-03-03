import packages
from context.infra.services_info import PORT_SVC_FACE
import os
import base64
import json
import tempfile
import logging
from datetime import datetime
from pathlib import Path
from typing import List
from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import cv2 as cv
import numpy as np
from deepface import DeepFace

# Configure logging to suppress DeepFace logs
logging.getLogger('deepface').setLevel(logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging

app = FastAPI()

# Get base directory for faces detection service
BASE_DIR = Path(__file__).resolve().parent
LIBFACEDETECTION_DIR = BASE_DIR / "impl" / "libfacedetection"
MODEL_PATH = LIBFACEDETECTION_DIR / "opencv_dnn" / "python" / "face_detection_yunet_2023mar_int8bq.onnx"

# Create directories if they don't exist
STATIC_DIR = BASE_DIR / "static"
DB_DIR = STATIC_DIR / "db"

for directory in [STATIC_DIR, DB_DIR]:
    os.makedirs(directory, exist_ok=True)

# Initialize database file if it doesn't exist
DB_FILE = DB_DIR / "faces_db.json"
if not DB_FILE.exists():
    with open(DB_FILE, 'w') as f:
        json.dump({"faces": []}, f)

# Mount static directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup Jinja2 templates
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

def initialize_face_detector():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
    return cv.FaceDetectorYN.create(
        model=str(MODEL_PATH),
        config='',
        input_size=(320, 320),
        score_threshold=0.6,
        nms_threshold=0.3,
        top_k=5000,
    )

# Initialize face detector
try:
    yunet = initialize_face_detector()
except Exception as e:
    print(f"Error initializing face detector: {str(e)}")
    yunet = None

def extract_face(image, bbox, margin=0.2):
    """Extract face from image with margin around the bounding box."""
    x, y, w, h = map(int, bbox[:4])
    
    margin_x = int(w * margin)
    margin_y = int(h * margin)
    
    start_x = max(0, x - margin_x)
    start_y = max(0, y - margin_y)
    end_x = min(image.shape[1], x + w + margin_x)
    end_y = min(image.shape[0], y + h + margin_y)
    
    face = image[start_y:end_y, start_x:end_x]
    return face, (start_x, start_y, end_x - start_x, end_y - start_y)

def get_name_from_path(db_path):
    """Extract name from the database path."""
    try:
        filename = os.path.basename(db_path)
        name = filename.split('_')[0]
        return name
    except:
        return "Unknown"

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.get("/widget")
async def widget(request: Request):
    return templates.TemplateResponse("widget.html", {
        "request": request,
        "port": PORT_SVC_FACE
    })

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                image_data = data.split(',')[1] if ',' in data else data
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv.imdecode(nparr, cv.IMREAD_COLOR)

                if image is None:
                    await websocket.send_json({
                        "error": "Invalid image data"
                    })
                    continue

                yunet.setInputSize((image.shape[1], image.shape[0]))
                _, faces = yunet.detect(image)

                detected_faces = []
                if faces is not None:
                    for face in faces:
                        face_img, _ = extract_face(image, face)
                        
                        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=True) as tmp_file:
                            cv.imwrite(tmp_file.name, face_img)
                            
                            try:
                                db_results = DeepFace.find(
                                    img_path=tmp_file.name,
                                    db_path=str(DB_DIR),
                                    enforce_detection=False,
                                    silent=True  # Suppress DeepFace progress bars
                                )
                                
                                if len(db_results) > 0 and len(db_results[0]) > 0:
                                    match = db_results[0].iloc[0]
                                    name = get_name_from_path(match.get("identity", ""))
                                    confidence = float(match.get("distance", 1.0))
                                    detected_faces.append({
                                        "name": name,
                                        "confidence": confidence
                                    })
                                else:
                                    detected_faces.append({
                                        "name": "Unknown",
                                        "confidence": 1.0
                                    })
                            except Exception as e:
                                detected_faces.append({
                                    "name": "Unknown",
                                    "confidence": 1.0
                                })

                await websocket.send_json({
                    "faces": detected_faces,
                    "count": len(detected_faces)
                })

            except Exception as e:
                await websocket.send_json({
                    "error": str(e)
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/register")
async def register_face(
    image_data: str = Form(),
    name: str = Form()
):
    try:
        if yunet is None:
            return JSONResponse(
                status_code=500,
                content={"error": "Face detector not initialized"}
            )

        base64_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(base64_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv.imdecode(nparr, cv.IMREAD_COLOR)

        if image is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid image data"}
            )

        yunet.setInputSize((image.shape[1], image.shape[0]))
        _, faces = yunet.detect(image)

        if faces is None or len(faces) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "No face detected"}
            )

        face_img, _ = extract_face(image, faces[0])
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        face_filename = f"{name}_{timestamp}.jpg"
        face_path = str(DB_DIR / face_filename)

        if not cv.imwrite(face_path, face_img):
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to save face image"}
            )

        db_data = {"faces": []}
        if DB_FILE.exists():
            with open(DB_FILE, 'r') as f:
                db_data = json.load(f)

        db_data["faces"].append({
            "name": name,
            "path": face_filename,
            "timestamp": timestamp
        })

        with open(DB_FILE, 'w') as f:
            json.dump(db_data, f)

        return {"success": True, "message": f"Face registered for {name}"}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Registration failed: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT_SVC_FACE)