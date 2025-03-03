```mermaid
flowchart TB
    subgraph AudioInput["Audio Processing"]
        MIC[Microphone] --> PyAudio[PyAudio Stream]
        PyAudio --> WD[Wake Word Detector]
    end

    subgraph BackendServices["Backend Services"]
        WD --> Queue[Callback Queue]
        Queue --> BG[Background Service]
        BG --> REDIS[(Redis PubSub)]
    end

    subgraph WebServices["Web Services"]
        REDIS --> FAPI[FastAPI Server]
        FAPI -->|WebSocket| ST[Streamlit UI]
        FAPI -->|WebSocket| WC[Web Clients]
    end

    subgraph Monitoring["Monitoring & Control"]
        ST --> Status[Status Display]
        ST --> History[Event History]
        ST --> Metrics[System Metrics]
    end

    classDef input fill:#fce4ec,stroke:#880e4f
    classDef process fill:#e1f5fe,stroke:#01579b
    classDef datastore fill:#fff3e0,stroke:#ff6f00
    classDef interface fill:#f1f8e9,stroke:#33691e
    classDef monitoring fill:#f3e5f5,stroke:#4a148c

    class MIC,PyAudio input
    class WD,BG,FAPI process
    class REDIS,Queue datastore
    class ST,WC interface
    class Status,History,Metrics monitoring
```

To use the system:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis server:
```bash
redis-server
```

3. Run the entire system:
```bash
python run.py
```

Or start components individually:
```bash
# Terminal 1: Background Service
python background_service.py

# Terminal 2: FastAPI Server
python fastapi_server.py

# Terminal 3: Streamlit App
streamlit run streamlit_app.py
```

The system provides:
1. Wake word detection using OpenWakeWord
2. Real-time updates via WebSocket
3. Web interface with Streamlit
4. System monitoring and metrics
5. Event history
6. Configuration management
