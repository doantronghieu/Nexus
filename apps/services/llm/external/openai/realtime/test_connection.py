#!/usr/bin/env python3
"""
Simple script to test connection to the OpenAI Realtime API
This helps ensure your API keys and configuration are working correctly
"""
import packages
import os
import asyncio
from dotenv import load_dotenv
from openai_realtime import RealtimeClient

# Load environment variables
load_dotenv()

# Get configuration from environment
use_azure = os.environ.get("USE_AZURE_OPENAI", "false").lower() == "true"

if use_azure:
    print("Testing Azure OpenAI connection...")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    
    if not all([api_key, endpoint, deployment]):
        print("Error: Missing required Azure OpenAI configuration.")
        print("Please check your .env file contains:")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_ENDPOINT")
        print("- AZURE_OPENAI_DEPLOYMENT")
        exit(1)
    
    print(f"Using Azure endpoint: {endpoint}")
    print(f"Using deployment: {deployment}")
else:
    print("Testing standard OpenAI connection...")
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: Missing OPENAI_API_KEY in environment.")
        print("Please check your .env file contains your OpenAI API key.")
        exit(1)

# Helper function for performing the test
async def test_connection():
    client = RealtimeClient(
        model="gpt-4o-realtime-preview-2024-12-17",
        use_azure=use_azure,
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT") if use_azure else None,
        azure_api_version=os.environ.get("AZURE_OPENAI_API_VERSION") if use_azure else None,
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT") if use_azure else None
    )
    
    print("Attempting to connect to Realtime API...")
    connected = await client.connect()
    
    if not connected:
        print("Failed to connect to the Realtime API.")
        print("Please check your API keys and configuration.")
        return
    
    print("Successfully connected!")
    print("Testing simple exchange with the model...")
    
    # Update session with basic parameters
    await client.update_session({
        "modalities": ["text"],
        "instructions": "You are a helpful assistant for testing purposes. Respond with very brief answers."
    })
    
    # Wait for session initialization
    await asyncio.sleep(1)
    
    # Send a text message
    await client.create_text_message("Hello, this is a test message. Reply with just 'Connection successful!'")
    
    # Request a response
    await client.create_response()
    
    # Collect and output the response
    full_text = ""
    timeout_counter = 0
    
    print("Waiting for response...")
    while timeout_counter < 30:  # Maximum 30 seconds timeout
        event = await client.get_next_event(timeout=1.0)
        if not event:
            timeout_counter += 1
            continue
            
        event_type = event.get("type")
        
        if event_type == "response.text.delta":
            delta = event.get("delta", "")
            full_text += delta
            print(delta, end="", flush=True)
        
        elif event_type == "response.done":
            print("\nResponse complete!")
            break
    
    if not full_text:
        print("No response received from the model.")
    
    # Clean up
    await client.disconnect()
    print("\nConnection test complete!")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_connection())
