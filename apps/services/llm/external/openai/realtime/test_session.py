#!/usr/bin/env python3
"""
Test script for the RealtimeSession class
Uses the fixed async generator to test sending messages and receiving responses
"""
import packages
import os
import asyncio
from dotenv import load_dotenv
from openai_realtime import RealtimeClient, RealtimeSession

# Load environment variables
load_dotenv()

# Get configuration from environment
use_azure = os.environ.get("USE_AZURE_OPENAI", "false").lower() == "true"

async def test_session():
    print(f"Testing {'Azure' if use_azure else 'Standard'} OpenAI Realtime API...")
    
    # Create a client with the appropriate configuration
    client = RealtimeClient(
        model="gpt-4o-realtime-preview-2024-12-17",
        use_azure=use_azure,
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT") if use_azure else None,
        azure_api_version=os.environ.get("AZURE_OPENAI_API_VERSION") if use_azure else None,
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT") if use_azure else None
    )
    
    print("Connecting to Realtime API...")
    connected = await client.connect()
    
    if not connected:
        print("Failed to connect to the Realtime API")
        return
    
    print("Connected successfully!")
    
    # Create a session for easier interaction
    session = RealtimeSession(client)
    
    # Initialize the session
    await session.initiate_session(
        modalities=["text"],
        instructions="You are a helpful assistant for testing. Be brief and concise."
    )
    
    print("\nSending test message...")
    
    # Send a message and get the response using the async generator
    message = "Hello! Please give me a short greeting and tell me what features the Realtime API provides."
    print(f"User: {message}")
    print("Assistant: ", end="", flush=True)
    
    # Process the response stream
    async for response in session.send_message_and_get_response(message):
        if response["type"] == "delta":
            # Print each delta as it arrives
            print(response["text"], end="", flush=True)
    
    print("\n\nTest completed successfully!")
    
    # Clean up
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_session())
