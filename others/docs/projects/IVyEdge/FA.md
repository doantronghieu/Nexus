# Automotive In-car Agents System Documentation

## 1. System Overview

### 1.1 Core Requirements

```mermaid
graph TD
    subgraph Requirements ["Automotive Integration Requirements"]
        R1["`
            <b>Core Requirements</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Must leverage invested tech/car infra (H/W)
            • High level of integration with car (H/W, SW, data)
            • Automotive grade HPC: Qualcomm
            </div>
        `"]
    end
```

### 1.2 Application Categories
1. Navigation
2. Driving: ADAS/AD
3. Communication
4. Entertainment
5. Parking
6. Diagnostics/Maintenance/OTA
7. EV-specific
8. Mobility needs/Fleet management
9. Remote control
10. V2X
11. In-Cabin monitoring

## 2. System Architecture

### 2.1 Complete System Pipeline

```mermaid
graph TD
    subgraph Input ["Input Sources"]
        AI["`
            <b>Audio Input (Microphone)</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Raw audio capture
            • Signal preprocessing
            • Initial filtering
            </div>
        `"]
        VCB["`
            <b>Voice Command Button</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Physical trigger
            • Direct activation
            • Wake word bypass
            </div>
        `"]
        BS["`
            <b>Background Service</b>
            <div style='text-align:left; white-space:nowrap;'>
            • System monitoring
            • Context tracking
            • State management
            </div>
        `"]
        SENS["`
            <b>Vehicle Sensors</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Light/Current detection
            • Water/Weather sensors
            • Door/Lock status
            • Environment monitoring
            </div>
        `"]
    end
    
    subgraph Processing ["Core Processing & AI"]
        WWD["`
            <b>Wake Word Detection</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Toyota: No wake word required
            • Bypass when agent waiting
            • Continuous monitoring
            </div>
        `"]
        VAD["`
            <b>Voice Activity Detection</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Speech detection
            • Noise filtering
            • Signal validation
            </div>
        `"]
        ASR["`
            <b>Speech Recognition</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Multi-language (EN, JP)
            • Text conversion
            • Context processing
            </div>
        `"]
        LLM["`
            <b>Language Model</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Natural language processing
            • Command interpretation
            • Response generation
            </div>
        `"]
        TTS["`
            <b>Text-to-Speech</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Voice synthesis
            • Audio generation
            • Output formatting
            </div>
        `"]
        FUNC["`
            <b>Function Calls</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Vehicle system control
            • API integration
            • CAN communication
            </div>
        `"]
    end

    subgraph Platform ["Computing & Cloud Platform"]
        CDC["`
            <b>Android Automotive (CDC)</b>
            <div style='text-align:left; white-space:nowrap;'>
            • SpaceQ/FF integration
            • Qualcomm optimization
            • Core system services
            </div>
        `"]
        OAI["`
            <b>OpenAI Cloud</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Cloud processing
            • Model serving
            • API services
            </div>
        `"]
        EP["`
            <b>Edge Processing</b>
            <div style='text-align:left; white-space:nowrap;'>
            • NVIDIA Orin AGX
            • Qualcomm 8295
            • Telechips Dolphin 5
            </div>
        `"]
    end

    subgraph Systems ["Vehicle Control Systems"]
        SOVI["`
            <b>SOVI Voice Path</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Voice routing
            • Signal processing
            • Audio management
            </div>
        `"]
        HVAC["`
            <b>HVAC System</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Climate control
            • Temperature management
            • Air quality
            </div>
        `"]
    end

    %% Input connections
    AI --> WWD
    VCB --> VAD
    BS -.-> WWD
    SENS --> SOVI

    %% Core processing flow
    WWD --> VAD
    VAD --> ASR
    ASR --> LLM
    LLM --> TTS
    LLM --> FUNC

    %% Platform support
    Platform -.-> Processing
    OAI -.-> LLM

    %% System control
    FUNC --> SOVI
    FUNC --> HVAC
    SOVI --- Processing

    %% Vehicle systems integration
    HVAC --- Systems
    
    %% Communication paths
    FUNC -.-> |"CAN/API"| Systems
```

### 2.2 Hardware Integration

```mermaid
graph TD
    subgraph Hardware ["Hardware Layer"]
        ORIN["`
            <b>Tom's NVIDIA ORIN</b>
            <div style='text-align:left; white-space:nowrap;'>
            • AI acceleration
            • Processing unit
            • System control
            </div>
        `"]
        BCM["`
            <b>Body Control Module</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Accessory control
            • Sensor integration
            • System coordination
            </div>
        `"]
        BMS["`
            <b>Battery Management</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Power management
            • Charging control
            • Energy monitoring
            </div>
        `"]
        PT["`
            <b>Powertrain Control</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Engine management
            • Performance control
            • System optimization
            </div>
        `"]
    end

    subgraph Sensors ["Sensor Layer"]
        SENS["`
            <b>Vehicle Sensors</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Light sensors
            • Current monitoring
            • Water/Weather
            • Door locks
            </div>
        `"]
    end

    subgraph Communication ["Protocol Stack"]
        PROT["`
            <b>Communication Protocols</b>
            <div style='text-align:left; white-space:nowrap;'>
            • CAN Bus
            • Ethernet
            • Safety protocols
            • Security measures
            </div>
        `"]
    end

    SENS --> Hardware
    Hardware --- PROT
```

### 2.3 Multi-Agent System

```mermaid
graph TD
    subgraph Core ["Core Services"]
        HAL["`
            <b>Hardware Abstract Layer</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Wrap hardware complexity
            • Common reusable APIs
            • Interface standardization
            </div>
        `"]
        CIS["`
            <b>Car Internal State Services</b>
            <div style='text-align:left; white-space:nowrap;'>
            • State synchronization (Daemon)
            • Data persistence
            • Real-time updates
            </div>
        `"]
        MAE["`
            <b>Multi-Agent Endpoint</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Handle user input
            • Delegate to agents
            • Coordination control
            </div>
        `"]
    end

    subgraph Agents ["Specialized Agents"]
        CCA["`
            <b>Car Control Agent</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Non-critical system control
            • Vehicle settings
            • Environment management
            </div>
        `"]
        CMA["`
            <b>Car Manual Agent</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Model-specific support
            • Documentation access
            • Feature guidance
            </div>
        `"]
        NA["`
            <b>Navigation Agent</b>
            <div style='text-align:left; white-space:nowrap;'>
            • User-based routing
            • Interest-based guidance
            • Location services
            </div>
        `"]
        IA["`
            <b>Infotainment Agent</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Media control
            • Entertainment
            • User preferences
            </div>
        `"]
        CA["`
            <b>Cloud Agent</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Offline handling
            • Cloud services
            • Remote functions
            </div>
        `"]
    end

    HAL --> CIS
    CIS --> MAE
    MAE --> CCA & CMA & NA & IA & CA
```

## 3. Implementation Details

### 3.1 Agent Candidates
1. Try Iy (AI-First)
   - Multi-command capability
   - LLM integration
   - CAN interface

2. Digital Mirror (Mazda Requirement)
   - Real-time monitoring
   - Visual feedback
   - State display

3. Predictive Fault Diagnostics (Drivers)
   - Early warning
   - Maintenance prediction
   - User alerts

4. Fault Diagnosis (Technicians)
   - Detailed diagnostics
   - Service tools
   - Professional support

5. In-cabin Monitoring
   - Providers: VinAI, Next, Xperi, LG, comma.ai
   - Environment monitoring
   - State detection

### 3.2 Example Scenarios

1. Weather Response:
   ```
   Scenario: "It is raining, do you want me to..."
   - Detect weather conditions
   - Suggest appropriate actions
   - Adjust vehicle systems
   ```

2. Mood Detection:
   ```
   Scenario: "I see you are in a bad mood due to traffic, 
             do you want me to play the newest playlist from Bruno Mars"
   - Monitor driver state
   - Detect traffic conditions
   - Provide entertainment suggestions
   ```

### 3.3 Key Features
1. Dynamic Agent Installation
   - App-like installation
   - Runtime configuration
   - Flexible deployment

2. Collaborative Operation
   - Independent or team-based
   - Task-specific cooperation
   - Seamless integration

3. Multi-language Support
   - English processing
   - Japanese processing
   - Natural language understanding

4. System Integration
   - High hardware integration
   - Software coordination
   - Data management