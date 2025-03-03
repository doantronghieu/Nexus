# OpenAI Realtime API Demo

This is a FastAPI application that demonstrates OpenAI's Realtime API features, which allow for low-latency, multi-modal conversational experiences with expressive voice-enabled models. This application supports both the standard OpenAI API and Azure OpenAI.

## Features

- Real-time text streaming with the OpenAI Realtime API
- Support for both WebRTC and WebSocket connections
- Audio input and output (voice conversations)
- Multi-modal conversations (text + audio)
- Azure OpenAI API support
- User-friendly web interface

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key with access to GPT-4o-realtime-preview models, OR
- An Azure OpenAI resource with a GPT-4o realtime deployment
- Modern web browser with WebRTC support

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your API keys:

### For OpenAI API:
```
USE_AZURE_OPENAI=false
OPENAI_API_KEY=your_openai_api_key_here
```

### For Azure OpenAI:
```
USE_AZURE_OPENAI=true
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

Or with custom arguments:
```bash
python main.py --host 127.0.0.1 --port 8080 --reload
```

Then open your browser and navigate to `http://localhost:8000` (or whatever host/port you specified).

## Using the Application

### Web Interface

The web interface allows you to:
- Send text messages to the AI and see real-time streaming responses
- Record and send audio messages (requires microphone permission)
- Configure the session settings
- Switch between OpenAI and Azure OpenAI
- View the conversation history

### Settings Configuration

1. **API Provider**: Choose between standard OpenAI API or Azure OpenAI
2. **Azure Settings** (if using Azure): 
   - Azure Endpoint (e.g., https://your-resource.openai.azure.com)
   - Deployment Name (the name of your GPT-4o realtime deployment)
   - API Version (default: 2024-02-15-preview)
3. **Model**: Select the Realtime model to use
4. **Modalities**: Choose text, audio, or both
5. **Voice**: Select the voice for the assistant's audio responses
6. **System Instructions**: Customize how the assistant behaves

## Technical Details

### Architecture

This application uses a server-side implementation to securely connect to OpenAI's Realtime API:

1. Client (browser) connects to the FastAPI server via WebSocket
2. FastAPI server connects to OpenAI's Realtime API via WebSocket
3. Messages and events are relayed between the client and OpenAI
4. Streaming text and audio are properly handled in both directions

### Realtime API Features Used

- Session management (create session, update settings)
- Text streaming (real-time deltas as the model generates text)
- Audio streaming (voice input and output)
- Voice activity detection (VAD)
- Function calling (optional)

## Troubleshooting

### Connection Issues

If you have problems connecting:

1. Check your API keys and settings in the `.env` file
2. For Azure, verify that your deployment is correctly set up with a GPT-4o realtime model
3. Check console logs for specific error messages (both browser and server logs)

### Audio Problems

If audio recording doesn't work:

1. Make sure your browser has permission to access the microphone
2. Verify that your microphone is working properly
3. Try using a different browser (Chrome or Edge recommended)

## API Keys and Security

**Important**: This application stores API keys in a `.env` file for demonstration purposes. In a production environment, you should use a more secure method for storing API keys.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
