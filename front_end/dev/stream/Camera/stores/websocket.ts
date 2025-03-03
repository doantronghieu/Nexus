import { defineStore } from "pinia"
import { useServerStore } from "./server"
import { useStreamsStore } from "./streams"
import type { WebSocketMessage } from "@/composables/types"

interface ConnectionState {
  lastConnectAttempt: number
  consecutiveFailures: number
}

export const useWebSocketStore = defineStore("websocket", {
  state: () => ({
    socket: null as WebSocket | null,
    isConnected: false,
    messages: [] as string[],
    clientId: "",
    displayName: "",
    reconnectAttempts: 0,
    maxReconnectAttempts: 5,
    reconnectInterval: 3000,
    isReconnecting: false,
    connectionState: {
      lastConnectAttempt: 0,
      consecutiveFailures: 0,
    } as ConnectionState,
    lastMessageTime: 0,
    pingInterval: null as number | null,
    lastPingTime: 0,
    error: null as string | null
  }),

  getters: {
    storedClientInfo: (state) => {
      try {
        const stored = localStorage.getItem("clientInfo")
        return stored ? JSON.parse(stored) : null
      } catch {
        return null
      }
    },

    shouldAttemptReconnect: (state) => {
      const minReconnectInterval = Math.min(
        1000 * Math.pow(2, state.connectionState.consecutiveFailures),
        30000 // Max 30 seconds between attempts
      )
      const timeSinceLastAttempt =
        Date.now() - state.connectionState.lastConnectAttempt
      return timeSinceLastAttempt >= minReconnectInterval
    }
  },

  actions: {
    async autoConnect(): Promise<boolean> {
      try {
        const serverStore = useServerStore()
        
        if (!serverStore.isConfigured) {
          this.error = 'Server not configured for auto-connect'
          return false
        }

        // Use stored client info if available
        const storedInfo = this.storedClientInfo
        const userName = storedInfo?.displayName

        return await this.connect(userName)
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Auto-connect failed'
        return false
      }
    },

    setupPingInterval() {
      if (this.pingInterval) {
        clearInterval(this.pingInterval)
      }

      this.pingInterval = window.setInterval(() => {
        if (this.socket?.readyState === WebSocket.OPEN) {
          this.socket.send(
            JSON.stringify({
              type: "ping",
              timestamp: Date.now(),
            })
          )
          this.lastPingTime = Date.now()
        }
      }, 30000) // Ping every 30 seconds
    },

    clearPingInterval() {
      if (this.pingInterval) {
        clearInterval(this.pingInterval)
        this.pingInterval = null
      }
    },

    storeClientInfo() {
      if (this.clientId && this.displayName) {
        localStorage.setItem(
          "clientInfo",
          JSON.stringify({
            clientId: this.clientId,
            displayName: this.displayName,
          })
        )
      }
    },

    async connect(userName?: string): Promise<boolean> {
      try {
        const serverStore = useServerStore()
        if (!serverStore.isConfigured) {
          throw new Error("Please apply server configuration first")
        }

        // Don't attempt reconnect too quickly
        if (!this.shouldAttemptReconnect) {
          return false
        }

        if (this.socket) {
          this.socket.close()
        }

        let wsUrl = serverStore.getWsUrl
        if (userName) {
          wsUrl += `?client_name=${encodeURIComponent(userName)}`
        }

        this.connectionState.lastConnectAttempt = Date.now()
        
        return new Promise((resolve) => {
          this.socket = new WebSocket(wsUrl)
          const streamsStore = useStreamsStore()

          this.socket.onopen = () => {
            this.isConnected = true
            this.reconnectAttempts = 0
            this.isReconnecting = false
            this.connectionState.consecutiveFailures = 0
            this.error = null
            this.setupPingInterval()
            resolve(true)
          }

          this.socket.onmessage = async (event) => {
						try {
							const data = JSON.parse(event.data);
							this.lastMessageTime = Date.now();

							if (data.type === "client_info") {
								this.clientId = data.client_id || "";
								this.displayName = data.display_name || "";
								this.messages.push(`Connected as ${data.display_name}`);

								// Store client info for reconnections
								this.storeClientInfo();

								// Initialize local client in streams store
								streamsStore.initializeClient(
									data.client_id,
									data.display_name,
									true
								);
							} else if (data.type === "pong") {
								this.lastPingTime = Date.now();
							} else if (data.type === "message") {
								this.messages.push(`${data.sender}: ${data.content}`);
							} else if (data.type === "frame") {
								// Handle frame messages
								const streamsStore = useStreamsStore();
								streamsStore.updateClientFrame(data.sender_id, data.content);
							}
						} catch (error) {
							console.error("Error processing message:", error);
						}
					};

          this.socket.onclose = () => {
            this.isConnected = false
            this.clearPingInterval()

            // Don't show disconnect message during intentional reconnection
            if (!this.isReconnecting) {
              this.messages.push("Disconnected from server")
            }

            if (!event.wasClean) {
              this.connectionState.consecutiveFailures++
            }

            // Attempt reconnection if appropriate
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
              this.isReconnecting = true
              this.reconnectAttempts++

              // Use exponential backoff for reconnection timing
              const backoffDelay = Math.min(
                1000 * Math.pow(2, this.connectionState.consecutiveFailures),
                30000
              )

              setTimeout(() => {
                this.connect(this.displayName || userName)
              }, backoffDelay)
            }
            
            resolve(false)
          }

          this.socket.onerror = () => {
            this.error = 'WebSocket connection error'
            this.isConnected = false
            this.clearPingInterval()
            resolve(false)
          }

          // Add connection timeout
          setTimeout(() => resolve(false), 5000)
        })

      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Connection failed'
        this.connectionState.consecutiveFailures++
        return false
      }
    },

    disconnect() {
      this.clearPingInterval()
      if (this.socket) {
        this.socket.close()
        this.socket = null
      }
      this.isConnected = false
      this.clientId = ""
      this.displayName = ""
      this.reconnectAttempts = 0
      this.isReconnecting = false
      this.connectionState = {
        lastConnectAttempt: 0,
        consecutiveFailures: 0,
      }
      this.error = null

      // Clear stored client info
      localStorage.removeItem("clientInfo")

      // Clear streams when disconnecting
      const streamsStore = useStreamsStore()
      streamsStore.clearStreams()
    },

    sendMessage(message: string | object) {
      if (this.socket?.readyState === WebSocket.OPEN) {
        const messageString =
          typeof message === "string" ? message : JSON.stringify(message)
        this.socket.send(messageString)
        return true
      }
      return false
    },

    clearMessages() {
      this.messages = []
    },

    resetError() {
      this.error = null
    }
  },

  persist: {
    paths: ["messages"],
  },
})
