import os
import json
import asyncio
import base64
import time
from typing import Dict, Any, List, Optional, Callable, Awaitable, Union
import websockets
from websockets.exceptions import ConnectionClosed

class RealtimeClient:
    """Client for OpenAI's Realtime API using WebSockets"""
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: str = "gpt-4o-realtime-preview-2024-12-17",
                 use_azure: bool = False,
                 azure_endpoint: Optional[str] = None,
                 azure_api_version: Optional[str] = None,
                 azure_deployment: Optional[str] = None):
        
        self.use_azure = use_azure
        
        if use_azure:
            self.api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
            self.azure_endpoint = azure_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
            self.azure_api_version = azure_api_version or os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
            self.model = azure_deployment or model or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
            
            if not self.azure_endpoint:
                raise ValueError("Azure OpenAI endpoint must be provided")
                
            # Normalize Azure endpoint URL
            self.azure_endpoint = self.azure_endpoint.rstrip('/')
            if self.azure_endpoint.startswith("https://"):
                self.azure_endpoint = self.azure_endpoint[8:]
        else:
            self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
            self.model = model
            
        self.websocket = None
        self.is_connected = False
        self.event_handlers = {}
        self.session_id = None
        self.event_queue = asyncio.Queue()
        self.should_listen = False
        self.listener_task = None
    
    async def connect(self, token: Optional[str] = None):
        """Connect to the OpenAI Realtime API WebSocket"""
        if not self.api_key and not token:
            raise ValueError("Either API key or token must be provided")
        
        if self.use_azure:
            # Azure OpenAI websocket URL format
            url = f"wss://{self.azure_endpoint}/openai/deployments/{self.model}/realtime?api-version={self.azure_api_version}"
            
            headers = {}
            if token:
                # Use token-based authentication (for client-side)
                headers = {
                    "api-key": token
                }
            else:
                # Use API key (for server-side)
                headers = {
                    "api-key": self.api_key
                }
        else:
            # Standard OpenAI
            url = f"wss://api.openai.com/v1/realtime?model={self.model}"
            
            headers = {}
            if token:
                # Use token-based authentication (for client-side)
                headers = {
                    "Authorization": f"Bearer {token}"
                }
            else:
                # Use API key (for server-side)
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "OpenAI-Beta": "realtime=v1"
                }
        
        print(f"Connecting to Realtime API at: {url}")
        print(f"Headers: {headers}")
        
        try:
            # For older websockets versions, use connect without extra_headers
            # and with subprotocols
            headers_list = []
            if token:
                # Use token-based authentication (for client-side)
                if self.use_azure:
                    headers_list.append(("api-key", token))
                else:
                    headers_list.append(("Authorization", f"Bearer {token}"))
            else:
                # Use API key (for server-side)
                if self.use_azure:
                    headers_list.append(("api-key", self.api_key))
                else:
                    headers_list.append(("Authorization", f"Bearer {self.api_key}"))
                    headers_list.append(("OpenAI-Beta", "realtime=v1"))
            
            # Connect with the appropriate parameters for older websockets
            self.websocket = await websockets.connect(
                url,
                subprotocols=["http"],
                extra_headers=headers_list
            )
            self.is_connected = True
            print("Successfully connected to Realtime API")
            
            # Start listening for events
            self.should_listen = True
            self.listener_task = asyncio.create_task(self._listen_for_events())
            
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from the WebSocket"""
        self.should_listen = False
        if self.listener_task:
            try:
                self.listener_task.cancel()
                await self.listener_task
            except asyncio.CancelledError:
                pass
        
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
    
    async def send_event(self, event_type: str, data: Dict[str, Any] = None):
        """Send an event to the Realtime API"""
        if not self.is_connected or not self.websocket:
            raise ConnectionError("Not connected to OpenAI Realtime API")
        
        event = {
            "type": event_type,
            "event_id": f"client-{time.time()}-{id(data)}"
        }
        
        if data:
            event.update(data)
        
        print(f"Sending event: {event}")
        await self.websocket.send(json.dumps(event))
    
    async def update_session(self, settings: Dict[str, Any]):
        """Update session settings"""
        await self.send_event("session.update", {"session": settings})
    
    async def create_text_message(self, text: str):
        """Create a text message in the conversation"""
        await self.send_event("conversation.item.create", {
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": text
                    }
                ]
            }
        })
    
    async def create_response(self, options: Dict[str, Any] = None):
        """Create a new response from the model"""
        data = {}
        if options:
            data["response"] = options
        await self.send_event("response.create", data)
    
    async def append_audio(self, audio_base64: str):
        """Append audio to the input buffer"""
        await self.send_event("input_audio_buffer.append", {
            "audio": audio_base64
        })
    
    async def commit_audio(self):
        """Commit the audio buffer"""
        await self.send_event("input_audio_buffer.commit", {})
    
    async def clear_audio_buffer(self):
        """Clear the audio buffer"""
        await self.send_event("input_audio_buffer.clear", {})
    
    async def cancel_response(self, response_id: Optional[str] = None):
        """Cancel a response"""
        data = {}
        if response_id:
            data["response_id"] = response_id
        await self.send_event("response.cancel", data)
    
    def on(self, event_type: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]):
        """Register an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def _handle_event(self, event: Dict[str, Any]):
        """Process an event from the server"""
        event_type = event.get("type")
        if not event_type:
            return
        
        # Put the event in the queue for external processing
        await self.event_queue.put(event)
        
        # Also call any registered event handlers
        handlers = self.event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                print(f"Error in event handler for {event_type}: {e}")
    
    async def _listen_for_events(self):
        """Listen for events from the server"""
        if not self.is_connected or not self.websocket:
            raise ConnectionError("Not connected to OpenAI Realtime API")
        
        try:
            while self.should_listen:
                message = await self.websocket.recv()
                event = json.loads(message)
                print(f"Received event: {event['type']}")
                await self._handle_event(event)
        except ConnectionClosed:
            self.is_connected = False
            print("Connection closed")
        except asyncio.CancelledError:
            print("Listener task cancelled")
        except Exception as e:
            print(f"Error in listen loop: {e}")
    
    async def get_next_event(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """Get the next event from the queue"""
        try:
            if timeout:
                return await asyncio.wait_for(self.event_queue.get(), timeout)
            else:
                return await self.event_queue.get()
        except asyncio.TimeoutError:
            return None


class RealtimeSession:
    """Helper class to manage a realtime session"""
    
    def __init__(self, client: RealtimeClient):
        self.client = client
        self.session_id = None
        self.conversation_id = None
        self.current_response_id = None
        self.response_queue = asyncio.Queue()
        
        # Set up event handlers
        self.client.on("session.created", self._handle_session_created)
        self.client.on("conversation.created", self._handle_conversation_created)
        self.client.on("response.created", self._handle_response_created)
        self.client.on("response.text.delta", self._handle_text_delta)
        self.client.on("response.done", self._handle_response_done)
    
    async def _handle_session_created(self, event):
        self.session_id = event.get("session", {}).get("id")
        print(f"Session created: {self.session_id}")
    
    async def _handle_conversation_created(self, event):
        self.conversation_id = event.get("conversation", {}).get("id")
        print(f"Conversation created: {self.conversation_id}")
    
    async def _handle_response_created(self, event):
        self.current_response_id = event.get("response", {}).get("id")
        print(f"Response created: {self.current_response_id}")
    
    async def _handle_text_delta(self, event):
        delta = event.get("delta", "")
        await self.response_queue.put(("delta", delta))
    
    async def _handle_response_done(self, event):
        response = event.get("response", {})
        await self.response_queue.put(("done", response))
    
    async def initiate_session(self, modalities=None, instructions=None, voice=None):
        """Initialize a session with the given parameters"""
        settings = {}
        
        if modalities:
            settings["modalities"] = modalities
        
        if instructions:
            settings["instructions"] = instructions
        
        if voice:
            settings["voice"] = voice
        
        await self.client.update_session(settings)
    
    async def send_message_and_get_response(self, text: str):
        """Send a text message and generate a response"""
        # Clear the response queue first
        while not self.response_queue.empty():
            await self.response_queue.get()
        
        # Send the text message
        await self.client.create_text_message(text)
        
        # Request a response
        await self.client.create_response()
        
        # Collect deltas until done
        full_text = ""
        response_data = None
        
        while True:
            event_type, data = await self.response_queue.get()
            
            if event_type == "delta":
                full_text += data
                yield {"type": "delta", "text": data, "full_text": full_text}
            
            elif event_type == "done":
                response_data = data
                # Final yield instead of return
                yield {"type": "done", "text": full_text, "response": response_data}
                break
