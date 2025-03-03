# Standard library imports
import asyncio
from contextlib import asynccontextmanager

# Third-party imports
import uvicorn
import websockets
from websockets.exceptions import ConnectionClosed

# FastAPI and related imports
from fastapi import (
    APIRouter,
    FastAPI,
    File,
    HTTPException,
    Path,
    Query,
    Request,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates