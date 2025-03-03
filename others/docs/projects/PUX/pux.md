```mermaid
flowchart TD
    subgraph PP[Pre-Processing]
        NF[Apply Noise Filtering]
        VAD[Apply VAD - Voice Activity Detection]
        FE[Extract Features - MFCC or Mel-Spectrogram]
        NF --> VAD
        VAD --> FE
    end

    subgraph POST[Post-Processing]
        TH[Thresholding]
        SM[Smoothing - Majority Voting]
        DB[Debouncing]
        TH --> SM
        SM --> DB
    end

    subgraph INF[Run KWS Inference]
        LA[Load KWS Algorithm]
        RI[Run Inference with Selected Algorithm]
        NOTE[Note: KWSアルゴリズムは入れ替え可能]
        LA --> RI
        LA -.-> NOTE
    end

    START[Start]
    AM[Get Audio Data from Microphone]
    DM[Display Matched Keywords]
    SW[Sliding Window Continues]

    START --> AM
    SW --> AM
    AM --> PP
    PP --> INF
    INF --> POST
    POST --> DM
    DM --> SW
```

| Group | Item | Content |
|-------|------|----------|
| Demo Program Requirements | Demo Program Specifications | 1. Display recognized audio commands in real-time.<br><br>2. Show inference time for the following steps:<br>- Audio capture from microphone<br>- Preprocessing<br>- Model inference<br><br>3. Ensure no response to noise, silence, or unrelated speech. |
| Language Support in Demo | Language Support in Demo | Support for multiple languages, including Japanese and English. |
| Overview | Output Format | Recognized commands (text or label). |
| | Project Objective | Execute a keyword spotting model on Jetson Orin AGX to recognize specific commands (words, 2-3 phrases). |
| | Model Base | Use one of CLAP-JPA, MM-KWS, PhonMatchNet, LAION-CLAP, or BC-ResNet. Consider switching if issues arise. |
| | Dataset | Use datasets that allow commercial use. Non-commercial datasets can be used if they significantly affect accuracy, but a comparison is required. |

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '18px', 'fontFamily': 'arial' }}}%%
flowchart TD
    START[Start] --> AM[Get Audio Data from Microphone]

    subgraph Flow[Main Processing Pipeline]
        direction LR
        subgraph PP["`
            <b>Pre-Processing</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Apply Noise Filtering
            • Voice Activity Detection
            • Feature Extraction - MFCC/Mel-Spectrogram
            • Noise/Silence Rejection
            </div>
        `"]
        end

        subgraph INF["`
            <b>KWS Inference</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Load KWS Algorithm
            • Run Inference
            • Note: KWSアルゴリズムは入れ替え可能
            </div>
        `"]
        end

        subgraph POST["`
            <b>Post-Processing</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Thresholding
            • Smoothing - Majority Voting
            • Debouncing
            </div>
        `"]
        end

        PP --- INF
        INF --- POST
    end

    subgraph Config[Configuration]
        direction TB
        subgraph Models["`
            <b>Supported Models</b>
            <div style='text-align:left; white-space:nowrap;'>
            • CLAP-JPA
            • MM-KWS
            • PhonMatchNet
            • LAION-CLAP
            • BC-ResNet
            </div>
        `"]
        end

        subgraph LANG["`
            <b>Language Support</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Japanese
            • English
            </div>
        `"]
        end
    end

    subgraph Monitor[System Monitoring]
        direction LR
        subgraph PERF["`
            <b>Performance Timing</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Audio Capture Time
            • Preprocessing Time
            • Model Inference Time
            </div>
        `"]
        end

        subgraph REQ["`
            <b>Requirements</b>
            <div style='text-align:left; white-space:nowrap;'>
            • Real-time Command Display
            • No Response to Noise/Silence
            • No Response to Unrelated Speech
            </div>
        `"]
        end
    end

    %% Main Flow Connections
    AM --> PP
    POST --> DM[Display Matched Keywords]
    DM --> SW[Sliding Window Continues]
    SW --> AM

    %% Cross-connections
    Models -.-> INF
    AM -.-> PERF
    PP -.-> PERF
    INF -.-> PERF
    DM -.-> LANG

    %% Styling
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef primary fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef config fill:#fff3e0,stroke:#ff9800,stroke-width:2px;
    classDef monitor fill:#f1f8e9,stroke:#689f38,stroke-width:2px;

    class Flow,PP,INF,POST primary;
    class Config,Models,LANG config;
    class Monitor,PERF,REQ monitor;
```