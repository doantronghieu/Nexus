# Car Voice Assistant UI System PRD
Version: 1.3
Date: February 10, 2025

## 1. Project Overview

### 1.1 Purpose
The Car Voice Assistant UI System is a Nuxt.js-based user interface designed to visualize and interact with the car voice assistant backend services. The system provides a main interface for monitoring agent activity and specialized modal interfaces for different agent functionalities.

### 1.2 System Scope
- Frontend UI implementation only
- Integration with existing backend services
- Real-time status visualization
- WebSocket-based communication
- Error and state management
- Agent-specific modal interfaces

## 2. User Experience Requirements

### 2.1 Core User Flows
1. Main Page Interface
   - Active agent status display
   - Current processing indication
   - System status visualization
   - Agent switching visualization

2. Voice Interaction
   - Voice-to-text transcription display (after 1s of silence)
   - Visual feedback during processing
   - Main agent response visualization
   - Dynamic modal activation based on agent context
   - WebSocket connection for real-time agent status updates

3. System Response
   - Natural text-to-speech output display
   - Processing status indication
   - Agent-specific interface display

### 2.2 Interface Requirements
1. Status Indicators
   - System status (active/inactive)
   - Microphone status
   - Processing status
   - Main agent status
   - Network connectivity

2. Visual Feedback
   - Voice activity visualization
   - Error state indicators
   - Processing state indicators

3. User Controls
   - Settings access
   - Mute button
   - Modal close/minimize controls

### 2.3 Agent Modal Interfaces

1. Car Manual Modal
   - Text stream display from LLM backend
   - Auto-scrolling conversation view
   - Response formatting

2. Car Control Modal
   - Interactive dashboard interface
   - Climate control interface
   - Audio system controls
   - Light control panel
   - Vehicle settings display
   - System status indicators

3. Navigation Modal
   - Map display
   - Route information
   - Traffic updates
   - POI display

4. Weather Modal
   - Current conditions dashboard
   - Forecast display
   - Weather alerts
   - Location-based weather information

5. News Modal
   - Text stream display from LLM backend
   - Auto-scrolling conversation view
   - Response formatting

6. Music Modal
   - Search interface
   - Player controls
   - Now playing display
   - Queue management

7. Search Modal
   - Text stream display from LLM backend
   - Auto-scrolling conversation view
   - Response formatting

## 3. Technical Requirements

### 3.1 Frontend Architecture
1. Core Technologies
   - Nuxt.js 3.x
   - Vue 3 Composition API
   - TypeScript
   - WebSocket integration
   - Web Audio API

2. State Management
   - Pinia for global state
   - Real-time state synchronization
   - Persistent settings storage
   - Error state handling
   - Modal state management

3. Real-time Communication
   - WebSocket connection management
   - Reconnection handling
   - Message queuing
   - Event broadcasting

## 4. Project Structure

### 4.1 Folder Structure
```
├── app/
├── components/
│   ├── common/
│   │   ├── ErrorDisplay.vue
│   │   ├── LoadingSpinner.vue
│   │   └── StatusIndicator.vue
│   ├── voice/
│   │   ├── ActivityIndicator.vue
│   │   ├── ConversationDisplay.vue
│   │   └── ProcessingStatus.vue
│   ├── settings/
│   │   ├── SettingsPanel.vue
│   │   └── AudioSettings.vue
│   ├── modals/
│   │   ├── BaseModal.vue
│   │   ├── TextStreamModal.vue
│   │   ├── CarControlModal.vue
│   │   ├── NavigationModal.vue
│   │   ├── WeatherModal.vue
│   │   └── MusicModal.vue
│   └── dashboards/
│       ├── CarControl/
│       │   ├── ClimateControl.vue
│       │   ├── AudioControl.vue
│       │   ├── LightControl.vue
│       │   └── Settings.vue
│       ├── Navigation/
│       │   ├── MapView.vue
│       │   └── RouteInfo.vue
│       ├── Weather/
│       │   ├── CurrentConditions.vue
│       │   └── Forecast.vue
│       └── Music/
│           ├── SearchView.vue
│           └── PlayerControls.vue
├── composables/
│   ├── useWebSocket.ts
│   ├── useVoiceProcessing.ts
│   ├── useSystemStatus.ts
│   ├── useModal.ts
│   └── useTextStream.ts
├── layouts/
│   └── default.vue
├── pages/
│   └── index.vue
├── stores/
│   ├── system.ts
│   ├── conversation.ts
│   ├── settings.ts
│   └── modal.ts
├── types/
│   ├── system.d.ts
│   ├── websocket.d.ts
│   ├── voice.d.ts
│   └── agents.d.ts
├── utils/
│   ├── websocket.ts
│   ├── audioProcessing.ts
│   ├── errorHandling.ts
│   └── modalManager.ts
└── public/
    └── assets/
```

### 4.2 Key Components

1. Modal Components
   - TextStreamModal: Base modal for LLM text stream display
   - Specialized dashboard modals for specific agents
   - Modal state management
   - WebSocket integration

2. Dashboard Components
   - Interactive control interfaces
   - Real-time data display
   - Status indicators
   - Control panels

3. Common Components
   - ErrorDisplay: Handles error message display
   - LoadingSpinner: Shows loading states
   - StatusIndicator: Shows system status

### 4.3 State Management

1. System Store
   ```typescript
   interface SystemState {
     isActive: boolean
     connectionStatus: ConnectionStatus
     currentError: Error | null
     processingStatus: ProcessingStatus
     currentAgent: AgentType | null
   }
   ```

2. Conversation Store
   ```typescript
   interface ConversationState {
     messages: Message[]
     isProcessing: boolean
     currentTranscript: string
     agentResponse: string
     textStream: string
   }
   ```

3. Modal Store
   ```typescript
   interface ModalState {
     activeModal: AgentType | null
     modalState: {
       isVisible: boolean
       position: Position
     }
   }
   ```

### 4.4 WebSocket Integration

1. Agent Status Connection
   ```typescript
   interface AgentStatusSocket {
     connect(): Promise<void>
     getCurrentAgent(): AgentType
     onAgentChange(callback: (agent: AgentType) => void): void
     disconnect(): void
   }
   ```

2. Text Stream Handler
   ```typescript
   interface TextStreamHandler {
     connect(): Promise<void>
     processStream(data: string): void
     disconnect(): void
   }
   ```

## 5. Development Guidelines

### 5.1 Code Organization
- Use TypeScript for all new code
- Implement composables for reusable logic
- Keep components small and focused
- Use Pinia for state management
- Implement proper error boundaries

### 5.2 Component Guidelines
- Use Composition API with `<script setup>`
- Implement proper prop validation
- Use typed emits for events
- Maintain clear component documentation
- Follow Vue 3 best practices

### 5.3 Modal Guidelines
- Implement consistent modal behavior
- Handle text stream display efficiently
- Maintain modal state
- Handle modal interactions
- Support keyboard navigation

### 5.4 State Management Guidelines
- Use Pinia stores for global state
- Implement proper type definitions
- Use composables for complex logic
- Maintain atomic state updates
- Implement proper error handling

### 5.5 WebSocket Guidelines
- Implement automatic reconnection
- Handle connection timeouts
- Implement message queuing
- Proper error handling
- Maintain connection status