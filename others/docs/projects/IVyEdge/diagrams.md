# Diagrams

[← Back to Main Documentation](../../../../README.md)

Please install [this](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) if you cannot see the diagrams.

## Legend

```mermaid
flowchart LR
    %% Style definitions with black text
    classDef llmProcess fill:#e6ccff,stroke:#333,stroke-width:2px,color:black;
    classDef normalProcess fill:#ffffff,stroke:#333,stroke-width:2px,color:black;
    classDef database fill:#b3e6cc,stroke:#333,stroke-width:2px,color:black;
    classDef input fill:#b3d9ff,stroke:#333,stroke-width:2px,color:black;
    classDef output fill:#ffb366,stroke:#333,stroke-width:2px,color:black;

    L1["LLM Process"]:::llmProcess
    L2["Normal Process"]:::normalProcess
    L3[(Database)]:::database
    L4[/"Input/Output"/]:::input
```

## Architecture

```mermaid
flowchart TD
    %% Style definitions with black text
    classDef frontend fill:#b3d9ff,stroke:#333,stroke-width:2px,color:black;
    classDef backend fill:#e6ccff,stroke:#333,stroke-width:2px,color:black;
    classDef database fill:#b3e6cc,stroke:#333,stroke-width:2px,color:black;

    subgraph "Frontend"
        UI["Web UI"]:::frontend
        VoiceInteraction["Voice Interaction Module"]:::frontend
    end

    subgraph "Backend Servers"
        WakeWordServer["WebSocket Server (Wake Word Detection)"]:::backend
        STTServer["Speech to Text Server"]:::backend
        TTSServer["Text to Speech Server"]:::backend
        LLMSystem["LLM System Server"]:::backend
    end

    subgraph "Databases"
        QueryExamplesDB[(Query Examples Vector DB)]:::database
        CarManualDB[(Car Manual Vector DB)]:::database
        CarInfoDB[(Car Information NoSQL DB)]:::database
        ParsedQueriesDB[(Parsed Queries Vector DB)]:::database
    end

    %% Frontend connections
    UI <--> VoiceInteraction
    VoiceInteraction <--> WakeWordServer
    
    %% Service connections
    WakeWordServer <--> STTServer
    STTServer --> LLMSystem
    
    %% Database connections
    QueryExamplesDB <-.-> LLMSystem
    CarManualDB <-.-> LLMSystem
    CarInfoDB <-.-> LLMSystem
    ParsedQueriesDB <-.-> LLMSystem
    
    %% Response flow
    LLMSystem --> TTSServer
    TTSServer --> VoiceInteraction

    %% Legend
    subgraph "Legend"
        F["Frontend"]:::frontend
        B["Backend"]:::backend
        D[(Database)]:::database
    end
```

## Main

```mermaid
flowchart LR
    classDef default font-size:25px;
    classDef subgraphStyle font-size:25px,text-align:center;
    %% Add default styling for all nodes
    linkStyle default font-size:25px;

    %% Style definitions with black text and larger font
    classDef llmProcess fill:#e6ccff,stroke:#333,stroke-width:2px,color:black;
    classDef normalProcess fill:#ffffff,stroke:#333,stroke-width:2px,color:black;
    classDef database fill:#b3e6cc,stroke:#333,stroke-width:2px,color:black;
    classDef input fill:#b3d9ff,stroke:#333,stroke-width:2px,color:black;
    classDef output fill:#ffb366,stroke:#333,stroke-width:2px,color:black;


    UI["UI"]:::input
    AudioInput["Real Time Audio Input"]
    WakeSystem["WakeWord Detection System (WebSocket Server)"]
    WakeWord{"Wake Word Detected?"}
    Record["Record User Voice"]
    STT["Speech to Text"]
    Transcription["Transcribed Text"]:::output
    LLM["LLM System"]:::llmProcess
    LLMOutput["LLM Output Text"]:::output
    TTS["Text to Speech"]
    AudioResponse[/"Audio Response"/]:::output

    UI --> AudioInput
    AudioInput --> WakeSystem
    WakeSystem --> WakeWord
    WakeWord -->|Yes| Record
    WakeWord -->|No| WakeSystem
    Record --> STT
    STT --> Transcription
    Transcription --> LLM
    LLM --> LLMOutput
    LLMOutput --> TTS
    TTS --> AudioResponse
```

## LLM System Flow

```mermaid
flowchart LR
    classDef default font-size:25px;
    %% Add default styling for all nodes
    linkStyle default font-size:25px;

    %% Style definitions with black text
    classDef llmProcess fill:#e6ccff,stroke:#333,stroke-width:2px,color:black;
    classDef normalProcess fill:#ffffff,stroke:#333,stroke-width:2px,color:black;
    classDef database fill:#b3e6cc,stroke:#333,stroke-width:2px,color:black;
    classDef input fill:#b3d9ff,stroke:#333,stroke-width:2px,color:black;
    classDef output fill:#ffb366,stroke:#333,stroke-width:2px,color:black;
    
    UserQuery[/"User Query"/]:::input
    Categorize["Categorize User Query"]:::llmProcess
    Category{"Query Category"}
    ChooseFlow["Choose Appropriate Flow"]
    Execute["Execute Selected Flow"]
    FlowResult["Flow Result"]
    Feedback{"Human Feedback"}
    PrepareResponse["Prepare Final Response"]:::llmProcess
    Results[/"Return Results to User"/]:::output
    
    subgraph "Available Flows"
        CarManual["Car Manual Flow"]:::llmProcess
        CarControl["Car Control Flow"]:::llmProcess
        General["General Flow"]:::llmProcess
    end

    subgraph "Vector Database"
        QueryExamples[(User -> Query-Category examples)]:::database
    end

    UserQuery --> Categorize
    QueryExamples -.->|Similar Examples| Categorize
    Categorize --> Category
    Category --> ChooseFlow
    ChooseFlow --> |Select One| Execute
    Execute --> FlowResult
    FlowResult --> Feedback
    
    Feedback -->|OK| PrepareResponse
    Feedback -->|Not OK| Categorize
    PrepareResponse --> Results
    
    CarManual -.-> ChooseFlow
    CarControl -.-> ChooseFlow
    General -.-> ChooseFlow
```

### RAG

```mermaid
flowchart LR
    %% Style definitions with black text
    classDef llmProcess fill:#e6ccff,stroke:#333,stroke-width:2px,color:black;
    classDef normalProcess fill:#ffffff,stroke:#333,stroke-width:2px,color:black;
    classDef database fill:#b3e6cc,stroke:#333,stroke-width:2px,color:black;
    classDef input fill:#b3d9ff,stroke:#333,stroke-width:2px,color:black;
    classDef output fill:#ffb366,stroke:#333,stroke-width:2px,color:black;

    UserQuery[/"User Query"/]:::input
    Retrieval["Custom Retrieval Algorithm"]:::llmProcess
    Response[/"Response to User"/]:::output
    
    subgraph "Vector Database"
        CarManualDB[(Car Manual Chunks)]:::database
    end

    UserQuery --> Retrieval
    CarManualDB -.->|Data Chunks| Retrieval
    Retrieval --> Response
```

### Control

```mermaid
flowchart LR
    classDef default font-size:25px;
    %% Add default styling for all nodes
    linkStyle default font-size:25px;

    %% Style definitions with black text
    classDef llmProcess fill:#e6ccff,stroke:#333,stroke-width:2px,color:black;
    classDef normalProcess fill:#ffffff,stroke:#333,stroke-width:2px,color:black;
    classDef database fill:#b3e6cc,stroke:#333,stroke-width:2px,color:black;
    classDef input fill:#b3d9ff,stroke:#333,stroke-width:2px,color:black;
    classDef output fill:#ffb366,stroke:#333,stroke-width:2px,color:black;

    UserQuery[/"User Query"/]
    SeparateTasks["Separate Tasks"]
    GatherTasks["Gather Completed Tasks"]
    FinalResponse[/"Consolidated Response"/]
    
    subgraph "Tasks Processing"
        direction TB
        Task1["Task 1"]
        Task2["Task 2"]
        Task3["Task 3"]
    end
    
    subgraph "Single Task Processing"
        direction LR
        ParseQuery["Parse User Query"]:::llmProcess
        Execute["Execute Operation"]
        TaskResponse["Task Response"]
        
        subgraph "Parsed Query JSON"
            JSON["action: get/update
            field_path: climate.ac
            new_value: false"]
        end
        
        subgraph "Databases"
            CarDB[(Car Properties)]:::database
            ParsedQueriesDB[(User Query -> Parsed version examples)]:::database
        end
    end

    UserQuery --> SeparateTasks:::llmProcess
    SeparateTasks --> Task1 & Task2 & Task3
    
    Task1 & Task2 & Task3 --> GatherTasks
    GatherTasks --> FinalResponse
    
    %% Single Task Flow Detail
    Task1 -.->|Example Flow| ParseQuery
    ParsedQueriesDB -.->|Similar Examples| ParseQuery
    ParseQuery --> JSON
    JSON --> Execute
    CarDB -.->|GET/UPDATE| Execute
    Execute --> TaskResponse
    TaskResponse -.-> GatherTasks

    %% Style applications with black text
    class UserQuery,FinalResponse input;
    class TaskResponse,JSON output;
```

### General

```mermaid
flowchart LR
    %% Style definitions with black text
    classDef llmProcess fill:#e6ccff,stroke:#333,stroke-width:2px,color:black;
    classDef normalProcess fill:#ffffff,stroke:#333,stroke-width:2px,color:black;
    classDef database fill:#b3e6cc,stroke:#333,stroke-width:2px,color:black;
    classDef input fill:#b3d9ff,stroke:#333,stroke-width:2px,color:black;
    classDef output fill:#ffb366,stroke:#333,stroke-width:2px,color:black;

    UserQuery[/"User Query"/]:::input
    GenerateParams["Generate Function Parameters"]:::llmProcess
    ExecuteFuncs["Execute Functions"]
    Response[/"Return Results to User"/]:::output
    
    subgraph "Available Functions"
        Weather["query_weather"]
        Navigation["query_navigation"]
    end

    UserQuery --> GenerateParams
    GenerateParams --> ExecuteFuncs
    Weather & Navigation -.-> ExecuteFuncs
    ExecuteFuncs --> Response
```

### Map

```mermaid
graph TB
    subgraph User["User Interaction"]
        UI["Frontend UI"]
        Query["User Query"]
        Map["Map Display"]
    end

    subgraph LLM["LLM Processing"]
        Parser["Query Parser"]
        Style["Action: search/confirm_place"]
    end

    subgraph MapOperations["Map Operations"]
        Search["Search Places"]
        Confirm["Confirm Place"]
        Directions["Get Directions"]
    end

    subgraph Storage["Data Storage"]
        Redis["Redis Cache"]
        RedisTTL["TTL: 1 hour"]
    end

    subgraph External["External Services"]
        Mapbox["Mapbox APIs"]
        direction1["Directions API"]
        direction2["Search API"]
        direction3["Retrieve API"]
    end

    subgraph Backend["FastAPI Backend"]
        API["API Endpoints"]
        MapClient["Map Client"]
        RedisToolkit["Redis Toolkit"]
    end

    %% User Flow
    Query --> Parser
    Parser --> Style
    Style --> API

    %% API Flow
    API --> MapClient
    MapClient --> Search
    MapClient --> Confirm
    MapClient --> Directions

    %% Map Operations
    Search --> direction2
    Confirm --> direction3
    Confirm -.-> |Auto trigger| Directions
    Directions --> direction1

    %% Results Display
    Search --> |Places List| Map
    Confirm --> |Selected Place| Map
    
    %% Storage Flow
    Directions --> |Store with ID| Redis
    Redis -- |Get by ID| --> UI

    %% UI Flow
    UI --> Query
    API --> UI

    %% External Services
    direction1 --> Mapbox
    direction2 --> Mapbox
    direction3 --> Mapbox

    %% Redis Connection
    RedisToolkit --> Redis

    class UI,Query,API,MapClient,Redis,Mapbox,Map highlighted
    classDef highlighted fill:#f9f,stroke:#333,stroke-width:2px
```