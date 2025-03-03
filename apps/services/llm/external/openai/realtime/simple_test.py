#!/usr/bin/env python3
"""
Very simple test for OpenAI Realtime API
Uses a minimal approach compatible with older websockets versions
"""
import os
import asyncio
import json
import websockets
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Azure OpenAI config
AZURE_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip('/')
if AZURE_ENDPOINT.startswith("https://"):
    AZURE_ENDPOINT = AZURE_ENDPOINT[8:]  # Remove https://
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
AZURE_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

async def simple_test():
    # Connect to Azure OpenAI
    url = f"wss://{AZURE_ENDPOINT}/openai/deployments/{AZURE_DEPLOYMENT}/realtime?api-version={AZURE_API_VERSION}"
    print(f"Connecting to {url}")
    
    try:
        # Connect with minimal parameters
        ws = await websockets.connect(
            url,
            subprotocols=["http"],
            extra_headers=[("api-key", AZURE_KEY)]
        )
        
        print("Connected!")
        
        # Wait for session.created event
        message = await ws.recv()
        data = json.loads(message)
        if data["type"] == "session.created":
            print("Session created successfully")
        else:
            print(f"Unexpected first message: {data['type']}")
            await ws.close()
            return
        
        # Update session settings
        event_id = str(uuid.uuid4())
        await ws.send(json.dumps({
            "type": "session.update",
            "event_id": event_id,
            "session": {
                "modalities": ["text"],
                "instructions": "You are a helpful assistant for testing. Be very brief."
            }
        }))
        
        # Wait for session.updated event
        message = await ws.recv()
        data = json.loads(message)
        print(f"Received: {data['type']}")
        
        # Send a simple text message
        event_id = str(uuid.uuid4())
        await ws.send(json.dumps({
            "type": "conversation.item.create",
            "event_id": event_id,
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Say hello in exactly five words."
                    }
                ]
            }
        }))
        
        # Wait for conversation.item.created event
        message = await ws.recv()
        data = json.loads(message)
        print(f"Received: {data['type']}")
        
        # Request a response
        event_id = str(uuid.uuid4())
        await ws.send(json.dumps({
            "type": "response.create",
            "event_id": event_id
        }))
        
        # Process the response
        print("\nAI Response: ", end="")
        done = False
        while not done:
            message = await ws.recv()
            data = json.loads(message)
            
            if data["type"] == "response.text.delta":
                delta = data.get("delta", "")
                print(delta, end="", flush=True)
            
            elif data["type"] == "response.done":
                done = True
                print("\n\nResponse complete!")
        
        # Close the connection
        await ws.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simple_test())
