#!/usr/bin/env python3
"""
Simple test script for OpenAI Realtime API
Compatible with older websockets library versions
"""
import os
import asyncio
import json
import websockets
from dotenv import load_dotenv
import time
import uuid
import base64

# Load environment variables
load_dotenv()

# Configuration
USE_AZURE = os.environ.get("USE_AZURE_OPENAI", "false").lower() == "true"
MODEL = "gpt-4o-realtime-preview-2024-12-17"

if USE_AZURE:
    API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
    ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip('/')
    if ENDPOINT.startswith("https://"):
        ENDPOINT = ENDPOINT[8:]  # Remove https:// prefix
    API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    
    # Construct Azure websocket URL
    WS_URL = f"wss://{ENDPOINT}/openai/deployments/{DEPLOYMENT}/realtime?api-version={API_VERSION}"
    
    # Azure headers for inclusion in URL
    AUTH_HEADERS = [("api-key", API_KEY)]
else:
    API_KEY = os.environ.get("OPENAI_API_KEY")
    
    # Construct OpenAI websocket URL
    WS_URL = f"wss://api.openai.com/v1/realtime?model={MODEL}"
    
    # OpenAI headers for inclusion in URL
    AUTH_HEADERS = [
        ("Authorization", f"Bearer {API_KEY}"),
        ("OpenAI-Beta", "realtime=v1")
    ]

async def send_event(websocket, event_type, data=None):
    """Send an event to the Realtime API"""
    event = {
        "type": event_type,
        "event_id": f"event_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    }
    if data:
        event.update(data)
    
    print(f"Sending: {event_type}")
    await websocket.send(json.dumps(event))

async def test_realtime_api():
    """Test connection to the Realtime API"""
    print(f"Testing {'Azure' if USE_AZURE else 'Standard'} OpenAI Realtime API")
    print(f"Connecting to: {WS_URL}")
    print(f"Headers: {AUTH_HEADERS}")
    
    try:
        # For older websockets versions, we need to use a custom class
        # that handles the custom headers. Here, we use the websockets.protocol
        # directly, which accepts headers in a different way.
        
        # Connect to the WebSocket using lower-level functions
        websocket = await websockets.connect(
            WS_URL,
            subprotocols=["http"],
            origin="https://example.com",
            extra_headers=AUTH_HEADERS
        )
        
        print("Connected to Realtime API")
        
        try:
            # Wait for session.created event
            session_created = False
            while not session_created:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Received: {data['type']}")
                if data["type"] == "session.created":
                    session_created = True
                    print("Session created successfully")
            
            # Update session settings
            await send_event(websocket, "session.update", {
                "session": {
                    "modalities": ["text"],
                    "instructions": "You are a helpful assistant for testing. Keep responses brief."
                }
            })
            
            # Wait for session.updated event
            session_updated = False
            while not session_updated:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Received: {data['type']}")
                if data["type"] == "session.updated":
                    session_updated = True
                    print("Session updated successfully")
            
            # Create a text message
            await send_event(websocket, "conversation.item.create", {
                "item": {
                    "type": "message",
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Hello! Please give me a short greeting."
                        }
                    ]
                }
            })
            
            # Wait for conversation.item.created event
            await websocket.recv()  # Just consume this event
            
            # Request a response
            await send_event(websocket, "response.create")
            
            # Process response events
            full_text = ""
            receiving = True
            while receiving:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data["type"] == "response.text.delta":
                    delta = data.get("delta", "")
                    full_text += delta
                    print(delta, end="", flush=True)
                
                elif data["type"] == "response.done":
                    print("\nResponse complete!")
                    receiving = False
            
            print("\nTest completed successfully")
        
        finally:
            await websocket.close()
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_realtime_api())
