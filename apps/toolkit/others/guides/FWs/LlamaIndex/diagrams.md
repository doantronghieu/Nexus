# LlamaIndex diagrams

## Full

```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': { 'fontSize': '40px', 'fontFamily': 'Arial' }}}%%
graph TD
    %% Node styles
    classDef user fill:#e6f3ff,stroke:#4da6ff,stroke-width:4px,shape:circle
    classDef ui fill:#ffccff,stroke:#ff66ff,stroke-width:4px,shape:rectangle
    classDef agent fill:#e6ffed,stroke:#00cc66,stroke-width:4px,shape:rectangle
    classDef tool fill:#f2f2f2,stroke:#999999,stroke-width:4px,shape:circle
    classDef storage fill:#ffe6e6,stroke:#ff6666,stroke-width:4px,shape:cylinder
    classDef process fill:#fff0e6,stroke:#ffa64d,stroke-width:4px,shape:diamond
    classDef resource fill:#e6e6ff,stroke:#6666ff,stroke-width:4px,shape:hexagon
    classDef security fill:#ff9999,stroke:#ff3333,stroke-width:4px,shape:octagon
    classDef multioption fill:#f0f0f0,stroke:#333333,stroke-width:6px
    classDef io fill:#d4f1f4,stroke:#40e0d0,stroke-width:4px,shape:parallelogram
    classDef dataflow fill:#fff,stroke:#333,stroke-width:4px,stroke-dasharray: 5 5
    classDef configurable stroke-dasharray: 5 5,stroke-width:6px
    classDef configurableMulti fill:#f0f0f0,stroke:#333333,stroke-width:6px,stroke-dasharray: 5 5

    subgraph LlamaIndexFramework[LlamaIndex Framework]
        %% Core Components
        subgraph CoreComponents[Core Components]
            style CoreComponents fill:#e6f3ff80,stroke:#4da6ff,color:#000000,stroke-width:4px
            User((User 👤)):::user
            UI[LlamaIndex Interface 📱]:::ui
            MainAgent[Main LLM Agent 🤖]:::configurableMulti
            LLM{{Language Model 🧠}}:::configurable
            EmbeddingModel{{Embedding Model 🔢}}:::configurable
        end

        %% Data Processing and Indexing (combined)
        subgraph DataProcessingAndIndexing[Data Processing and Indexing]
            style DataProcessingAndIndexing fill:#e6ffed80,stroke:#00cc66,color:#000000,stroke-width:4px
            subgraph DataLoadingSystem[Data Loading]
                Readers[Data Connectors/Readers 📚]:::multioption
                NodeParser[Node Parser 🔪]:::configurableMulti
                TextSplitter[Text Splitter ✂️]:::configurable
                Transformations{Transformations 🔄}:::configurableMulti
                IngestionPipeline{Ingestion Pipeline 🚀}:::process
                Caching((Caching 💾)):::configurable
            end

            subgraph IndexingSystem[Indexing]
                IndexNode[Index 📊]:::configurableMulti
                IndexTypes[Index Types]:::multioption
                IndexConstruction{Index Construction 🏗️}:::configurable
                DocManagement{Document Management 📄}:::process
            end
        end

        %% Storage
        subgraph StorageSystem[Storage]
            style StorageSystem fill:#ffe6e680,stroke:#ff6666,color:#000000,stroke-width:4px
            DocStore[(Document Store 📄)]:::storage
            IndexStore[(Index Store 🗄️)]:::storage
            VectorStore[(Vector Store 🧮)]:::storage
            GraphStore[(Graph Store 🌐)]:::storage
            ChatStore[(Chat Store 💬)]:::storage
            StorageContext{Storage Context 🧰}:::process
        end

        %% Querying System
        subgraph QueryingSystem[Querying]
            style QueryingSystem fill:#fff0e680,stroke:#ffa64d,color:#000000,stroke-width:4px
            QueryEngine[Query Engine ⚙️]:::configurableMulti
            ChatEngine[Chat Engine 🗨️]:::configurableMulti
            Retriever{Retriever 🎣}:::configurable
            NodePostprocessor{Node Postprocessor 🔧}:::configurable
            ResponseSynthesizer{Response Synthesizer 🎭}:::configurable
            Router{Router 🔀}:::process
            Streaming((Streaming 🌊)):::tool
            PromptHelper[Prompt Helper 💬]:::configurable
        end

        %% Agents System
        subgraph AgentsSystem[Agents]
            style AgentsSystem fill:#e6e6ff80,stroke:#6666ff,color:#000000,stroke-width:4px
            DataAgent[Data Agent 🕵️]:::agent
            ReasoningLoop{Reasoning Loop 🔄}:::process
            ToolAbstractions[Tool Abstractions 🛠️]:::tool
            AgentTypes[Agent Types 🤖]:::configurableMulti
            Tools[Tools 🔧]:::configurableMulti

            subgraph LowerLevelAPI[Lower-Level API]
                AgentRunner[Agent Runner 🏃]:::process
                AgentWorker[Agent Worker 👷]:::process
                Task[Task 📋]:::process
                TaskStep[Task Step 👣]:::process
                TaskStepOutput[Task Step Output 📤]:::process
            end
        end

        %% Workflow System
        subgraph WorkflowSystem[Workflow]
            style WorkflowSystem fill:#ffccff80,stroke:#ff66ff,color:#000000,stroke-width:4px
            WorkflowSteps[Workflow Steps 🚶]:::configurable
            EventHandling{Event Handling 🎭}:::process
            RetryPolicy{Retry Policy 🔁}:::configurableMulti
            GlobalContext{Global Context 🌍}:::process

            subgraph WorkflowComponents[Workflow Components]
                WorkflowEvents[Events]:::process
                WorkflowContext[Context]:::process
                StepDecorator[Step Decorator]:::process
                StreamingEvents[Streaming Events]:::process
            end

            subgraph WorkflowTypes[Workflow Types]
                SimpleWorkflow[Simple Workflow]:::process
                NestedWorkflow[Nested Workflow]:::process
            end

            subgraph WorkflowExecution[Workflow Execution]
                StepwiseExecution[Stepwise Execution]:::process
                AsyncExecution[Async Execution]:::process
            end
        end

        %% Workflow Deployment
        subgraph WorkflowDeployment[Workflow Deployment]
            style WorkflowDeployment fill:#f0e68c80,stroke:#daa520,color:#000000,stroke-width:4px
            LlamaDeploy[llama_deploy 🚀]:::process
            ControlPlane[Control Plane 🎛️]:::process
            MessageQueue[Message Queue 📬]:::process
            Orchestrator[Orchestrator 🎭]:::process

            subgraph DeploymentTypes[Deployment Types]
                LocalDeployment[Local Deployment]:::process
                KubernetesDeployment[Kubernetes Deployment]:::process
            end

            subgraph DeploymentComponents[Deployment Components]
                WorkflowService[Workflow Service]:::process
                LlamaDeployClient[LlamaDeploy Client]:::tool
            end
        end

        %% Observability System
        subgraph ObservabilitySystem[Observability]
            style ObservabilitySystem fill:#98fb9880,stroke:#3cb371,color:#000000,stroke-width:4px
            InstrumentationModule[Instrumentation Module 🔬]:::process
            EventSystem[Event System 📡]:::process
            SpanSystem[Span System 🕰️]:::process
            Dispatcher[Dispatcher 📣]:::process
            ObservabilityTools[Observability Tools 🛠️]:::configurableMulti
        end

        %% LlamaCloud
        subgraph LlamaCloudSystem[LlamaCloud]
            style LlamaCloudSystem fill:#ffdab980,stroke:#ff8c00,color:#000000,stroke-width:4px
            LlamaParse[LlamaParse 📄]:::tool
            IngestionAPI[Ingestion API 📥]:::tool
            RetrievalAPI[Retrieval API 📤]:::tool
            EvaluationsObservability[Evaluations & Observability 📊]:::tool
        end

        %% Input/Output
        InputDocs[Documents 📄]:::io
        InputQueries[Queries ❓]:::io
        OutputResponses[Responses 💬]:::io
        OutputSummaries[Summaries 📊]:::io

        %% Connections with enhanced labels
        User <====>|Interact and provide input| UI
        UI <====>|Send queries and receive responses| MainAgent
        MainAgent -.-o|Generate text based on context| LLM
        MainAgent -.-o|Create vector representations| EmbeddingModel
        MainAgent -->|Process and route queries| QueryEngine
        Readers ==>|Extract and parse raw data| NodeParser
        NodeParser ==>|Divide text into manageable chunks| TextSplitter
        TextSplitter ==>|Create structured node objects| Transformations
        Transformations ==>|Apply data transformations and enhancements| IngestionPipeline
        IngestionPipeline <==>|Store and retrieve processed data| Caching
        IndexConstruction ==>|Create searchable index structures| IndexNode
        IndexNode ---|Organize data in various index types| IndexTypes
        DocManagement -.-o|Update and maintain index| IndexConstruction
        StorageContext -.-o|Manage document storage and retrieval| DocStore
        StorageContext -.-o|Handle index data persistence| IndexStore
        StorageContext -.-o|Manage vector representations| VectorStore
        StorageContext -.-o|Handle graph-based data structures| GraphStore
        StorageContext -.-o|Manage conversation history| ChatStore
        Router ==>|Direct queries to appropriate engine| QueryEngine
        Router ==>|Handle conversational queries| ChatEngine
        QueryEngine <==>|Retrieve relevant information| Retriever
        QueryEngine <==>|Refine and filter retrieved nodes| NodePostprocessor
        QueryEngine <==>|Generate coherent responses| ResponseSynthesizer
        ChatEngine <==>|Process multi-turn conversations| QueryEngine
        ResponseSynthesizer ==>|Provide real-time response updates| Streaming
        QueryEngine <--->|Fetch and store data| StorageSystem
        PromptHelper -->|Optimize prompts for| QueryEngine
        PromptHelper -->|Enhance conversation flow in| ChatEngine
        DataAgent -->|Implement reasoning strategies| ReasoningLoop
        DataAgent -->|Utilize various tools and APIs| ToolAbstractions
        ReasoningLoop -->|Define agent behaviors and capabilities| AgentTypes
        AgentRunner -->|Coordinate and execute| Task
        Task -->|Break down into smaller units| TaskStep
        AgentWorker -->|Process individual steps| TaskStep
        TaskStep -->|Generate intermediate outputs| TaskStepOutput
        ToolAbstractions -->|Provide access to| Tools
        WorkflowSteps <==>|Handle workflow events| EventHandling
        WorkflowSteps <==>|Implement error handling and retries| RetryPolicy
        WorkflowSteps <==>|Share data across workflow| GlobalContext
        WorkflowSteps -->|Define step logic and structure| StepDecorator
        WorkflowSteps -->|Emit workflow events| WorkflowEvents
        WorkflowSteps -->|Access shared workflow data| WorkflowContext
        WorkflowSteps -->|Enable real-time updates| StreamingEvents
        WorkflowTypes -->|Define execution patterns for| WorkflowExecution
        LlamaDeploy -->|Manage deployment resources| ControlPlane
        LlamaDeploy -->|Handle inter-service communication| MessageQueue
        LlamaDeploy -->|Coordinate workflow execution| Orchestrator
        LlamaDeploy -->|Enable different deployment scenarios| DeploymentTypes
        LlamaDeploy -->|Manage workflow service instances| WorkflowService
        LlamaDeploy -->|Provide programmatic access| LlamaDeployClient
        InstrumentationModule -->|Track and manage events| EventSystem
        InstrumentationModule -->|Monitor execution spans| SpanSystem
        InstrumentationModule -->|Route monitoring data| Dispatcher
        Dispatcher -->|Send data to various monitoring tools| ObservabilityTools
        LlamaParse -->|Provide structured data from documents| IngestionAPI
        IngestionAPI -->|Store and index parsed data| RetrievalAPI
        RetrievalAPI -->|Provide data for analysis| EvaluationsObservability

        %% Main Data Flow
        InputDocs ==>|Provide raw document input| Readers
        DataLoadingSystem ==>|Supply processed and parsed data| IndexConstruction
        IndexingSystem ==>|Provide indexed data for storage| StorageContext
        InputQueries ==>|Submit user queries| Router
        StorageContext ==>|Fetch relevant data for queries| Retriever
        ResponseSynthesizer ==>|Generate final response| OutputResponses
        ResponseSynthesizer ==>|Produce summarized output| OutputSummaries

        %% Connections between systems
        MainAgent -->|Coordinate data processing and querying| DataAgent
        DataAgent -->|Execute complex queries and tasks| QueryEngine
        DataAgent -->|Access and manipulate stored data| StorageContext
        DataAgent -->|Produce agent-assisted responses| OutputResponses
        MainAgent -->|Initiate and manage workflows| WorkflowSteps
        WorkflowSteps -->|Utilize agent capabilities| DataAgent
        WorkflowSteps -->|Execute queries within workflow| QueryEngine
        WorkflowSteps -->|Manage data throughout workflow| StorageContext
        WorkflowSteps -->|Deploy and execute via| LlamaDeploy
        LlamaDeploy -->|Orchestrate and monitor| WorkflowService
        InstrumentationModule -->|Monitor data loading and processing| DataLoadingSystem
        InstrumentationModule -->|Track indexing operations| IndexingSystem
        InstrumentationModule -->|Observe query execution| QueryingSystem
        InstrumentationModule -->|Monitor agent activities| AgentsSystem
        InstrumentationModule -->|Track workflow execution| WorkflowSystem
        InstrumentationModule -->|Monitor deployment status| WorkflowDeployment
        LlamaCloudSystem -->|Provide advanced data processing| DataLoadingSystem
        LlamaCloudSystem -->|Offer cloud-based indexing| IndexingSystem
        LlamaCloudSystem -->|Enable cloud-powered querying| QueryingSystem
        LlamaCloudSystem -->|Integrate monitoring and evaluation| ObservabilitySystem
        LlamaParse -->|Enhance document preprocessing| InputDocs
        IngestionAPI -->|Streamline data ingestion process| DataLoadingSystem
        RetrievalAPI -->|Improve query capabilities| QueryEngine
        EvaluationsObservability -->|Provide performance insights| ObservabilityTools

        %% Data flow labels
        RawData[Raw Data]:::dataflow
        ProcessedData[Processed Data]:::dataflow
        Nodes[Nodes]:::dataflow
        IndexStructures[Index Structures]:::dataflow
        IndexedData[Indexed Data]:::dataflow
        StoredData[Stored Data]:::dataflow
        RetrievedData[Retrieved Data]:::dataflow
        ProcessedResults[Processed Query Results]:::dataflow
    end

    %% Enhanced Legend
    subgraph Legend[Legend]
        direction LR
        User2((User)):::user
        UI2[UI/Agent]:::ui
        Agent2[Agent]:::agent
        Tool2((Tool)):::tool
        Storage2[(Storage)]:::storage
        Process2{Process}:::process
        Resource2{{Resource}}:::resource
        Security2{Security}:::security
        MultiOption[Multiple Options]:::multioption
        Configurable[Configurable]:::configurable
        ConfigurableMulti[Configurable & Multi-Option]:::configurableMulti
        IO[Input/Output]:::io
        DataFlow[Data Flow Label]:::dataflow

        %% Connection type examples
        UserInteraction[User Interaction]
        SystemInteraction[System Interaction]
        DataProcessing[Data Processing]
        StorageOperation[Storage Operation]
        QueryExecution[Query Execution]
        AgentAction[Agent Action]
        WorkflowOperation[Workflow Operation]
        DeploymentAction[Deployment Action]
        ObservabilityFlow[Observability Flow]
        CloudIntegration[Cloud Integration]
        MainDataFlow[Main Data Flow]
        InterSystemConnection[Inter-System Connection]

        UserInteraction ====> SystemInteraction
        SystemInteraction ---> DataProcessing
        DataProcessing ==> StorageOperation
        StorageOperation <===> QueryExecution
        QueryExecution -.-> AgentAction
        AgentAction --> WorkflowOperation
        WorkflowOperation ==> DeploymentAction
        ObservabilityFlow -->|Monitor| DataProcessing
        CloudIntegration -->|Enhance| QueryExecution
        MainDataFlow ==>|Flow| InterSystemConnection

        linkStyle 87 stroke:#ff9900,stroke-width:4px
        linkStyle 88 stroke:#3333ff,stroke-width:4px
        linkStyle 89 stroke:#00cc66,stroke-width:4px
        linkStyle 90 stroke:#ff6666,stroke-width:4px
        linkStyle 91 stroke:#ffa64d,stroke-width:4px
        linkStyle 92 stroke:#6666ff,stroke-width:4px
        linkStyle 93 stroke:#ff66ff,stroke-width:4px
        linkStyle 94 stroke:#daa520,stroke-width:4px
        linkStyle 95 stroke:#3cb371,stroke-width:4px
        linkStyle 96 stroke:#ff8c00,stroke-width:4px
        linkStyle 97 stroke:#1e90ff,stroke-width:4px
    end

    %% Define connection styles
    linkStyle default stroke-width:4px
    linkStyle 0,1 stroke:#ff9900,stroke-width:4px
    linkStyle 2,3,4 stroke:#3333ff,stroke-width:4px
    linkStyle 5,6,7,8,9,10,11,12,13,14,15 stroke:#00cc66,stroke-width:4px
    linkStyle 16,17,18,19,20,21,22 stroke:#ff6666,stroke-width:4px
    linkStyle 23,24,25,26,27,28,29,30,31,32 stroke:#ffa64d,stroke-width:4px
    linkStyle 33,34,35,36,37,38,39,40 stroke:#6666ff,stroke-width:4px
    linkStyle 41,42,43,44,45,46,47,48,49 stroke:#ff66ff,stroke-width:4px
    linkStyle 50,51,52,53,54,55 stroke:#daa520,stroke-width:4px
    linkStyle 56,57,58,59 stroke:#3cb371,stroke-width:4px
    linkStyle 60,61,62 stroke:#ff8c00,stroke-width:4px
    linkStyle 63,64,65,66,67,68,69 stroke:#1e90ff,stroke-width:4px
    linkStyle 70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86 stroke:#800080,stroke-width:4px

    %% Define subgraph styles
    style LlamaIndexFramework fill:#ffffff,stroke:#333333,stroke-width:4px
    style Legend fill:#f5f5f5,stroke:#666666,stroke-width:2px
    style DataProcessingAndIndexing fill:#e6ffed80,stroke:#00cc66,color:#000000,stroke-width:4px
    style StorageSystem fill:#ffe6e680,stroke:#ff6666,color:#000000,stroke-width:4px
    style QueryingSystem fill:#fff0e680,stroke:#ffa64d,color:#000000,stroke-width:4px
    style AgentsSystem fill:#e6e6ff80,stroke:#6666ff,color:#000000,stroke-width:4px
    style WorkflowSystem fill:#ffccff80,stroke:#ff66ff,color:#000000,stroke-width:4px
    style WorkflowDeployment fill:#f0e68c80,stroke:#daa520,color:#000000,stroke-width:4px
    style ObservabilitySystem fill:#98fb9880,stroke:#3cb371,color:#000000,stroke-width:4px
    style LlamaCloudSystem fill:#ffdab980,stroke:#ff8c00,color:#000000,stroke-width:4px
```

## Workflow & Deployment

```mermaid

```