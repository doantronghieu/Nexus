import { defineStore } from 'pinia'
import { useWebSocketStore } from './websocket'
import { useCameraStore } from './camera'

interface StreamMetrics {
  frameCount: number
  fps: number
  startTime: number | null
  lastUpdateTime: number
}

interface StreamClient {
  id: string
  displayName: string
  lastFrame: string | null
  isStreaming: boolean
  metrics: StreamMetrics
  isLocal: boolean
}

const STREAM_TIMEOUT = 5000 // 5 seconds without updates to consider stream inactive

export const useStreamsStore = defineStore('streams', {
  state: () => ({
    activeClients: new Map<string, StreamClient>(),
    selectedClientId: null as string | null,
    streamCheckInterval: null as number | null,
    metricsUpdateInterval: null as number | null,
    lastStreamUpdate: {} as Record<string, number>
  }),

  getters: {
    clientsList: (state) => Array.from(state.activeClients.values()),
    hasActiveStreams: (state) => Array.from(state.activeClients.values()).some(client => client.isStreaming),
    selectedClient: (state) => state.selectedClientId ? state.activeClients.get(state.selectedClientId) : null,
    streamingClientsCount: (state) => Array.from(state.activeClients.values()).filter(client => client.isStreaming).length,
    getClientById: (state) => (clientId: string) => state.activeClients.get(clientId),
    
    getClientMetrics: (state) => (clientId: string) => {
      const client = state.activeClients.get(clientId)
      return client?.metrics || null
    },

    getStreamDuration: (state) => (clientId: string) => {
      const client = state.activeClients.get(clientId)
      if (client?.metrics.startTime && client.isStreaming) {
        return Date.now() - client.metrics.startTime
      }
      return 0
    }
  },

  actions: {
    startStreamCheck() {
      this.stopStreamCheck()

      // Check for inactive streams every second
      this.streamCheckInterval = window.setInterval(() => {
        const now = Date.now()
        this.activeClients.forEach((client, clientId) => {
          if (!client.isLocal && client.isStreaming) {
            const timeSinceUpdate = now - (this.lastStreamUpdate[clientId] || 0)
            if (timeSinceUpdate > STREAM_TIMEOUT) {
              this.handleStreamingStatusUpdate(clientId, false)
            }
          }
        })
      }, 1000)
    },

    stopStreamCheck() {
      if (this.streamCheckInterval) {
        clearInterval(this.streamCheckInterval)
        this.streamCheckInterval = null
      }
    },

    startMetricsUpdate() {
      this.stopMetricsUpdate()

      // Update metrics for active streams every second
      this.metricsUpdateInterval = window.setInterval(() => {
        this.activeClients.forEach((client) => {
          if (client.isStreaming) {
            this.updateClientMetrics(client.id, {
              frameCount: client.metrics.frameCount,
              fps: this.calculateFPS(client),
              startTime: client.metrics.startTime,
              lastUpdateTime: Date.now()
            })
          }
        })
      }, 1000)
    },

    stopMetricsUpdate() {
      if (this.metricsUpdateInterval) {
        clearInterval(this.metricsUpdateInterval)
        this.metricsUpdateInterval = null
      }
    },

    calculateFPS(client: StreamClient): number {
      if (!client.metrics.startTime || !client.isStreaming) return 0
      const duration = (Date.now() - client.metrics.startTime) / 1000
      return duration > 0 ? Math.round((client.metrics.frameCount / duration) * 10) / 10 : 0
    },

    initializeClient(clientId: string, displayName: string, isLocal: boolean = false) {
      if (!this.activeClients.has(clientId)) {
        const now = Date.now()
        this.activeClients.set(clientId, {
          id: clientId,
          displayName: isLocal ? `${displayName} (You)` : displayName,
          lastFrame: null,
          isStreaming: false,
          metrics: {
            frameCount: 0,
            fps: 0,
            startTime: null,
            lastUpdateTime: now
          },
          isLocal
        })
        this.lastStreamUpdate[clientId] = now

        if (this.activeClients.size === 1) {
          this.startStreamCheck()
          this.startMetricsUpdate()
        }
      }
    },

    updateClientMetrics(clientId: string, metrics: Partial<StreamMetrics>) {
      const client = this.activeClients.get(clientId)
      if (client) {
        const now = Date.now()
        this.activeClients.set(clientId, {
          ...client,
          metrics: {
            ...client.metrics,
            ...metrics,
            lastUpdateTime: now
          }
        })
        this.lastStreamUpdate[clientId] = now
      }
    },

    updateLocalStream(isStreaming: boolean, frame: string | null = null) {
      const webSocketStore = useWebSocketStore()
      const cameraStore = useCameraStore()
      if (!webSocketStore.clientId) return

      const now = Date.now()
      const client = this.activeClients.get(webSocketStore.clientId)

      if (client) {
        const newFrameCount = isStreaming ? (frame ? client.metrics.frameCount + 1 : client.metrics.frameCount) : 0
        const newStartTime = isStreaming ? (client.metrics.startTime || now) : null

        const metrics = {
          frameCount: newFrameCount,
          fps: isStreaming ? Number(cameraStore.selectedFps) : 0,
          startTime: newStartTime,
          lastUpdateTime: now
        }

        this.activeClients.set(webSocketStore.clientId, {
          ...client,
          isStreaming,
          lastFrame: frame || client.lastFrame,
          metrics,
          isLocal: true
        })
        this.lastStreamUpdate[webSocketStore.clientId] = now

        // Broadcast metrics update via WebSocket
        if (isStreaming) {
          webSocketStore.sendMessage({
            type: 'metrics_update',
            client_id: webSocketStore.clientId,
            metrics: {
              frameCount: newFrameCount,
              fps: metrics.fps,
              startTime: newStartTime,
              isStreaming: true
            }
          })
        }
      } else {
        this.initializeClient(webSocketStore.clientId, webSocketStore.displayName, true)
        this.updateLocalStream(isStreaming, frame)
      }
    },

    updateClientStream(clientId: string, data: { displayName: string } & Partial<StreamClient>) {
      const webSocketStore = useWebSocketStore()
      if (clientId === webSocketStore.clientId) return

      const client = this.activeClients.get(clientId)
      const now = Date.now()

      if (client) {
        this.activeClients.set(clientId, {
          ...client,
          ...data,
          metrics: {
            ...client.metrics,
            lastUpdateTime: now
          },
          isLocal: false
        })
        this.lastStreamUpdate[clientId] = now
      } else {
        this.initializeClient(clientId, data.displayName)
        this.updateClientStream(clientId, data)
      }
    },

    handleStreamingStatusUpdate(clientId: string, isStreaming: boolean) {
      const client = this.activeClients.get(clientId)
      if (client && !client.isLocal) {
        const now = Date.now()
        const newMetrics = isStreaming ? {
          ...client.metrics,
          lastUpdateTime: now
        } : {
          frameCount: 0,
          fps: 0,
          startTime: null,
          lastUpdateTime: now
        }

        this.activeClients.set(clientId, {
          ...client,
          isStreaming,
          metrics: newMetrics
        })
        this.lastStreamUpdate[clientId] = now
      }
    },

    updateClientFrame(clientId: string, frame: string) {
      const webSocketStore = useWebSocketStore()
      if (clientId === webSocketStore.clientId) {
        this.updateLocalStream(true, frame)
        return
      }

      const client = this.activeClients.get(clientId)
      if (client) {
        const now = Date.now()
        const newFrameCount = client.metrics.frameCount + 1

        this.activeClients.set(clientId, {
          ...client,
          lastFrame: frame,
          isStreaming: true,
          metrics: {
            ...client.metrics,
            frameCount: newFrameCount,
            startTime: client.metrics.startTime || now,
            lastUpdateTime: now
          }
        })
        this.lastStreamUpdate[clientId] = now
      } else {
        this.initializeClient(clientId, `Client ${clientId.slice(0, 8)}`)
        this.updateClientFrame(clientId, frame)
      }
    },

    removeClient(clientId: string) {
      const client = this.activeClients.get(clientId)
      if (client?.isLocal) {
        this.updateLocalStream(false)
      } else {
        this.activeClients.delete(clientId)
        delete this.lastStreamUpdate[clientId]
      }
      
      if (this.selectedClientId === clientId) {
        this.selectedClientId = null
      }

      if (this.activeClients.size === 0) {
        this.stopStreamCheck()
        this.stopMetricsUpdate()
      }
    },

    clearStreams() {
      const localStreams = Array.from(this.activeClients.values())
        .filter(client => client.isLocal)
      this.activeClients.clear()
      this.lastStreamUpdate = {}
      
      localStreams.forEach(client => {
        this.activeClients.set(client.id, client)
        this.lastStreamUpdate[client.id] = Date.now()
      })
      
      this.selectedClientId = null
      this.stopStreamCheck()
      this.stopMetricsUpdate()
    }
  },

  persist: {
    paths: ['selectedClientId']
  }
})