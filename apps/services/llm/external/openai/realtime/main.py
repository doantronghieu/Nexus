import os
import json
import base64
import uuid
import time
from typing import List, Optional, Dict, Any, Union
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import aiohttp
import asyncio
import uvicorn
import httpx
import argparse

# Import RealtimeClient and RealtimeSession
from openai_realtime import RealtimeClient, RealtimeSession

# Load environment variables
load_dotenv()

# Configuration classes
class OpenAIConfig(BaseModel):
    api_key: str
    use_azure: bool = False

class AzureOpenAIConfig(OpenAIConfig):
    api_version: str
    azure_endpoint: str
    azure_deployment: Optional[str] = None
    use_azure: bool = True

# Load configuration from environment variables
def get_config() -> Union[OpenAIConfig, AzureOpenAIConfig]:
    """Load OpenAI or Azure OpenAI configuration from environment variables"""
    use_azure = os.environ.get("USE_AZURE_OPENAI", "false").lower() == "true"
    
    if use_azure:
        return AzureOpenAIConfig(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
            azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", None)
        )
    else:
        return OpenAIConfig(
            api_key=os.environ.get("OPENAI_API_KEY", "")
        )

app = FastAPI(title="OpenAI Realtime API Demo")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Serve favicon.ico
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join('static', 'img', 'favicon.ico'))

# Websocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"WebSocket client connected: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"WebSocket client disconnected: {client_id}")

    async def send_text(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def send_json(self, data: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(data)

manager = ConnectionManager()

# Store active OpenAI Realtime API clients
active_clients: Dict[str, RealtimeClient] = {}

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/session-token", response_class=JSONResponse)
async def get_session_token():
    """
    Generate an ephemeral session token for client-side use with the OpenAI Realtime API
    """
    try:
        config = get_config()
        
        # For demo purposes, return a mock session token to avoid API calls errors
        # In a production environment, you would uncomment the actual API calls below
        
        # Create a demo session token that will work with our websocket endpoint
        mock_session = {
            "id": f"sess_{uuid.uuid4().hex[:8]}",
            "object": "realtime.session",
            "model": "gpt-4o-realtime-preview-2024-12-17" if not isinstance(config, AzureOpenAIConfig) else config.azure_deployment or "gpt-4o-realtime",
            "modalities": ["audio", "text"],
            "instructions": "You are a helpful assistant. Respond concisely and clearly.",
            "voice": "alloy",
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "input_audio_transcription": {"model": "whisper-1"},
            "turn_detection": {"type": "server_vad", "threshold": 0.5, "prefix_padding_ms": 300, "silence_duration_ms": 500},
            "tools": [],
            "tool_choice": "auto",
            "temperature": 0.7,
            "max_response_output_tokens": 200,
            "client_secret": {
                "value": f"mock_token_{uuid.uuid4().hex}", 
                "expires_at": int(time.time()) + 3600  # Expires in 1 hour
            }
        }
        
        # Log connection details for debugging
        print(f"API configuration: {config}")
        
        # TODO: Replace with real API call for production
        # This is just a mock token for testing
        return mock_session
        
        # The actual API call code is commented out below:
        # 
        # if isinstance(config, AzureOpenAIConfig):
        #     # Azure OpenAI
        #     if not config.api_key or not config.azure_endpoint:
        #         raise HTTPException(status_code=500, detail="Azure OpenAI API key or endpoint not found")
        #     
        #     headers = {
        #         "api-key": config.api_key,
        #         "Content-Type": "application/json"
        #     }
        #     
        #     model_or_deployment = config.azure_deployment or "gpt-4o-realtime"
        #     
        #     data = {
        #         "model": model_or_deployment,
        #         "modalities": ["audio", "text"],
        #         "instructions": "You are a helpful assistant. Respond concisely and clearly."
        #     }
        #     
        #     # Call the Azure OpenAI session token endpoint
        #     url = f"{config.azure_endpoint}/openai/deployments/{model_or_deployment}/realtime/sessions?api-version={config.api_version}"
        #     
        # else:
        #     # Standard OpenAI
        #     if not config.api_key:
        #         raise HTTPException(status_code=500, detail="OpenAI API key not found in environment variables")
        #     
        #     headers = {
        #         "Authorization": f"Bearer {config.api_key}",
        #         "Content-Type": "application/json"
        #     }
        #     
        #     data = {
        #         "model": "gpt-4o-realtime-preview-2024-12-17",
        #         "modalities": ["audio", "text"],
        #         "instructions": "You are a helpful assistant. Respond concisely and clearly."
        #     }
        #     
        #     # Call the OpenAI session token endpoint
        #     url = "https://api.openai.com/v1/realtime/sessions"
        # 
        # # Make the API call
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         url,
        #         headers=headers,
        #         json=data,
        #         timeout=30.0
        #     )
        #     
        #     if response.status_code != 200:
        #         raise HTTPException(
        #             status_code=response.status_code,
        #             detail=f"Error from API: {response.text}"
        #         )
        #         
        #     session_data = response.json()
        #     return session_data
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating session token: {str(e)}")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    print(f"New WebSocket connection: {client_id}")
    
    try:
        # Check if this client already has an OpenAI connection
        openai_client = active_clients.get(client_id)
        if not openai_client:
            print(f"No OpenAI client for {client_id}, will create one when needed")
        
        # This is a server-side websocket that bridges between the client and OpenAI
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(f"Received WebSocket message: {message.get('type', 'unknown')}")
            
            # Process different message types
            msg_type = message.get("type")
            
            if msg_type == "voice_message":
                # Handle voice messages
                if not openai_client:
                    # Create a new client on demand
                    config = get_config()
                    openai_client = RealtimeClient(
                        model="gpt-4o-realtime-preview-2024-12-17",
                        use_azure=isinstance(config, AzureOpenAIConfig),
                        azure_endpoint=getattr(config, 'azure_endpoint', None),
                        azure_api_version=getattr(config, 'api_version', None),
                        azure_deployment=getattr(config, 'azure_deployment', None)
                    )
                    
                    # Connect to OpenAI
                    connected = await openai_client.connect()
                    if not connected:
                        await manager.send_json(
                            {"type": "error", "message": "Failed to connect to OpenAI Realtime API"},
                            client_id
                        )
                        continue
                    
                    # Store the client
                    active_clients[client_id] = openai_client
                    
                    # Set up the session
                    await openai_client.update_session({
                        "modalities": ["audio", "text"],
                        "instructions": "You are a helpful assistant. Respond concisely and clearly."
                    })
                
                # Process the voice message
                voice_text = message.get("text", "")
                await manager.send_json(
                    {"type": "processing", "message": "Processing voice message"},
                    client_id
                )
                
                try:
                    # Send as text for now (audio would require base64 encoding)
                    await openai_client.create_text_message(voice_text)
                    await openai_client.create_response()
                    
                    # Monitor for deltas and forward them to the websocket
                    while True:
                        event = await openai_client.get_next_event(timeout=10.0)
                        if not event:
                            break
                            
                        event_type = event.get("type")
                        
                        # Forward text deltas to the client
                        if event_type == "response.text.delta":
                            delta = event.get("delta", "")
                            await manager.send_json(
                                {"type": "text_delta", "data": {"delta": delta}},
                                client_id
                            )
                        
                        # When the response is done, send the final message
                        elif event_type == "response.done":
                            # Extract the full text from output items
                            output_items = event.get("response", {}).get("output", [])
                            full_text = ""
                            
                            for item in output_items:
                                if item.get("type") == "message" and item.get("role") == "assistant":
                                    for content_part in item.get("content", []):
                                        if content_part.get("type") == "text":
                                            full_text += content_part.get("text", "")
                            
                            await manager.send_json(
                                {"type": "response_done", "data": {"text": full_text}},
                                client_id
                            )
                            break
                        
                except Exception as e:
                    print(f"Error processing voice message: {e}")
                    await manager.send_json(
                        {"type": "error", "message": f"Error: {str(e)}"},
                        client_id
                    )
            
            elif msg_type == "settings_update":
                # Handle settings updates
                settings = message.get("settings", {})
                
                # If client doesn't exist yet, create one with the new settings
                if not openai_client:
                    config = get_config()
                    
                    # Override with client settings if provided
                    use_azure = settings.get("useAzure", isinstance(config, AzureOpenAIConfig))
                    model = settings.get("model", "gpt-4o-realtime-preview-2024-12-17")
                    
                    azure_endpoint = None
                    azure_deployment = None
                    azure_api_version = None
                    
                    if use_azure:
                        azure_endpoint = settings.get("azureEndpoint", getattr(config, 'azure_endpoint', None))
                        azure_deployment = settings.get("azureDeployment", getattr(config, 'azure_deployment', None))
                        azure_api_version = settings.get("azureApiVersion", getattr(config, 'api_version', "2024-02-15-preview"))
                    
                    openai_client = RealtimeClient(
                        model=model,
                        use_azure=use_azure,
                        azure_endpoint=azure_endpoint,
                        azure_api_version=azure_api_version,
                        azure_deployment=azure_deployment
                    )
                    
                    # Connect to OpenAI
                    connected = await openai_client.connect()
                    if not connected:
                        await manager.send_json(
                            {"type": "error", "message": "Failed to connect to OpenAI Realtime API"},
                            client_id
                        )
                        continue
                    
                    # Store the client
                    active_clients[client_id] = openai_client
                
                # Update OpenAI session settings
                session_settings = {}
                
                # Convert frontend settings to OpenAI format
                if "modalities" in settings:
                    session_settings["modalities"] = settings["modalities"]
                
                if "voice" in settings:
                    session_settings["voice"] = settings["voice"]
                
                if "instructions" in settings:
                    session_settings["instructions"] = settings["instructions"]
                
                # Update the session if we have settings
                if session_settings and openai_client:
                    try:
                        await openai_client.update_session(session_settings)
                        await manager.send_json(
                            {"type": "settings_updated", "settings": settings},
                            client_id
                        )
                    except Exception as e:
                        print(f"Error updating session: {e}")
                        await manager.send_json(
                            {"type": "error", "message": f"Error updating settings: {str(e)}"},
                            client_id
                        )
            
            else:
                # Echo other messages back (for debugging/testing)
                await manager.send_json(
                    {"type": "echo", "data": message},
                    client_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        
        # Clean up the OpenAI client if it exists
        if client_id in active_clients:
            client = active_clients[client_id]
            await client.disconnect()
            del active_clients[client_id]
            print(f"Cleaned up OpenAI client for {client_id}")
    
    except Exception as e:
        print(f"WebSocket error: {e}")
        import traceback
        traceback.print_exc()
        manager.disconnect(client_id)

@app.post("/text-message")
async def send_text_message(client_id: str = Form(...), message: str = Form(...)):
    """
    Handle a text message from the client
    """
    # Send the message to OpenAI's Realtime API
    
    try:
        # Get the client
        client = active_clients.get(client_id)
        if not client:
            print(f"No client found for ID: {client_id}, creating a new one")
            # Create a new client
            config = get_config()
            
            client = RealtimeClient(
                model="gpt-4o-realtime-preview-2024-12-17",
                use_azure=isinstance(config, AzureOpenAIConfig),
                azure_endpoint=getattr(config, 'azure_endpoint', None),
                azure_api_version=getattr(config, 'api_version', None),
                azure_deployment=getattr(config, 'azure_deployment', None)
            )
            
            # Connect to OpenAI
            connected = await client.connect()
            if not connected:
                raise HTTPException(status_code=500, detail="Failed to connect to OpenAI Realtime API")
                
            # Store the client
            active_clients[client_id] = client
            
            # Set up the session
            await client.update_session({
                "modalities": ["text"],
                "instructions": "You are a helpful assistant. Respond concisely and clearly."
            })
        
        # Send the text message to OpenAI
        await client.create_text_message(message)
        
        # Notify the client that message was received
        await manager.send_json(
            {
                "type": "text_status",
                "data": {
                    "status": "Message sent to OpenAI",
                    "message": message
                }
            },
            client_id
        )
        
        # Request a response from OpenAI
        await client.create_response()
        
        # Monitor for deltas and forward them to the websocket
        while True:
            event = await client.get_next_event(timeout=30.0)
            if not event:
                break
                
            event_type = event.get("type")
            
            # Forward text deltas to the client
            if event_type == "response.text.delta":
                delta = event.get("delta", "")
                await manager.send_json(
                    {
                        "type": "text_delta",
                        "data": {
                            "delta": delta
                        }
                    },
                    client_id
                )
            
            # When the response is done, send the final message
            elif event_type == "response.done":
                output_items = event.get("response", {}).get("output", [])
                full_text = ""
                
                # Extract the text from the output items
                for item in output_items:
                    if item.get("type") == "message" and item.get("role") == "assistant":
                        for content_part in item.get("content", []):
                            if content_part.get("type") == "text":
                                full_text += content_part.get("text", "")
                
                await manager.send_json(
                    {
                        "type": "response_done",
                        "data": {
                            "text": full_text
                        }
                    },
                    client_id
                )
                break
        
        return {"status": "message sent"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

def parse_args():
    parser = argparse.ArgumentParser(description="OpenAI Realtime API Demo")
    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"), help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")), help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    uvicorn.run("main_new:app", host=args.host, port=args.port, reload=args.reload)
