# Camera Stream Application

This project consists of a FastAPI backend server and a Nuxt.js frontend application for camera stream functionality.

## Project Structure

```
/apps/services/dev/stream/
├── server.py         # FastAPI backend server with loguru logging

/front_end/dev/stream/Camera/
├── components/       # Vue components
│   ├── NavigationBar.vue
│   ├── ServerHealth.vue
│   ├── WebSocketStats.vue
│   └── WebSocketConnection.vue
├── composables/      # Vue composables for state and logic
│   ├── types.ts     # Shared TypeScript interfaces and types
│   ├── server/      # Server-related composables
│   │   ├── index.ts
│   │   ├── serverUrl.ts
│   │   ├── serverConfig.ts
│   │   ├── healthCheck.ts
│   │   └── websocketStats.ts
│   └── chat/        # Chat-related composables
│       ├── index.ts
│       ├── chat.ts
│       ├── websocket.ts
│       └── connectionPreferences.ts
├── layouts/         # Nuxt layouts
│   └── default.vue
└── pages/          # Application pages
    ├── index.vue
    ├── server-setup.vue
    └── camera-stream.vue
```

## Current Implementation Status

### Backend (FastAPI)

#### Implemented Features:

1. **Health Check Endpoint**

   - Route: `/health`
   - Returns service health status
   - Includes CORS headers and ngrok support

2. **WebSocket Support**

   - Route: `/ws`
   - Handles multiple client connections with unique IDs
   - Supports custom client names
   - Broadcasts messages to all connected clients
   - Connection management with error handling
   - Real-time client tracking

3. **WebSocket Statistics Endpoint**

   - Route: `/ws/stats`
   - Provides real-time connection statistics
   - Tracks client connect/disconnect events
   - Monitors message counts per client
   - Tracks connection duration

4. **Enhanced Logging System**

   - Using loguru with emoji indicators
   - Colorized console output
   - Structured event logging
   - Connection lifecycle tracking
   - Message monitoring

5. **Server Configuration**
   - Configurable server host and port
   - CORS middleware with full configuration
   - Support for secure connections (HTTP/HTTPS, WS/WSS)
   - Ngrok tunneling support

### Frontend (Nuxt.js)

#### Implemented Features:

1. **Navigation System**

   - Navigation bar with routing
   - Current route highlighting
   - Responsive design

2. **Server Configuration**

   - Server host selection/input with validation
   - Predefined server hosts list
   - HTTP/HTTPS protocol toggle
   - Configuration state management
   - Visual feedback for applied settings

3. **WebSocket Functionality**

   - Real-time connection management
   - Client name customization options:
     - Server-generated names
     - Predefined name selection
     - Custom name input
   - Message handling with history
   - Connection status monitoring
   - Auto-refreshing statistics view

4. **Type-Safe Implementation**

   - Centralized TypeScript types
   - Proper type definitions for all features
   - Enhanced error handling
   - Improved null/undefined handling

5. **Composable-Based Architecture**
   - Modular state management
   - Logical grouping of related functionality
   - Clear separation of concerns
   - Reusable code patterns

#### Pending Features:

1. Camera Stream Implementation

## Development Setup

### Backend

```bash
# From /apps/services/dev/stream/
conda deactivate && conda activate dev
python server.py
```

### Frontend

```bash
# From /front_end/dev/stream/Camera/
npm run dev
```

### Ngrok Tunnel (Optional)

```bash
ngrok http --url=positive-viper-presently.ngrok-free.app 8000
```

## Technologies Used

### Backend

- FastAPI
- WebSocket
- Loguru with emoji logging
- CORS middleware
- Uvicorn
- Python Faker for name generation

### Frontend

- Nuxt.js 3
- Vue.js 3 Composition API
- TypeScript
- TailwindCSS
- WebSocket API

## Current Limitations and Notes

1. Server configuration must be explicitly applied before use
2. Health check requires proper server configuration
3. WebSocket connections require proper server configuration
4. Camera stream functionality is not yet implemented
5. WebSocket reconnection not yet implemented
6. No persistent storage for messages
