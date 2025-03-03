```mermaid
graph TD
    A[Swift App] --> B[Apple Car Play]
    A -->|Backend powered by Devices Nvidia Jetson| C[Back End]
    C -->|LLM services| D[agents, ...]
    C -->|Audio services| E[speech to text, text to speech, wake word detection]
    C -->|General services| F[map, music, infortainment]
    C --> A
    User --> B
    User --> A
    C -->|Connects to| G[Comma3x]
    G -->|Connects to| H[Car]
```