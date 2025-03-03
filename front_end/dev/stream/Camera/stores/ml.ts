import { defineStore } from 'pinia'
import { useServerStore } from './server'
import type { WebSocketMessage } from '@/composables/types'

interface MLStats {
  active_connections: number
  server_connected: boolean
  uptime_seconds: number
  clients: Array<{
    id: string
    info: {
      name: string
      connected_at: string
      processed_frames: number
      is_streaming?: boolean
    }
  }>
}

interface ProcessedFrame {
  id: string
  content: string
  timestamp: string
  client_id: string
}

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

interface HealthCheckResult {
  ok: boolean
  message: string
  connections?: MLStats
}

interface MLState {
  socket: WebSocket | null
  serverSocket: WebSocket | null
  isConnected: boolean
  isServerConnected: boolean
  isConfigured: boolean
  stats: MLStats | null
  error: string | null
  reconnectAttempts: number
  maxReconnectAttempts: number
  reconnectInterval: number
  isReconnecting: boolean
  clientId: string
  clientName: string
  lastMLPingTime: number
  healthStatus: HealthCheckResult | null
  isLoading: boolean
  activeClients: Map<string, StreamClient>
  selectedClientId: string | null
  lastStreamUpdate: Record<string, number>
  processedFrames: Map<string, ProcessedFrame[]>
  streamCheckInterval: number | null
  isProcessing: boolean
  isMLProcessingEnabled: boolean
  processingStats: {
    frameCount: number
    fps: number
  }
}

export const useMLStore = defineStore("ml", {
	state: (): MLState => ({
		socket: null,
		serverSocket: null,
		isConnected: false,
		isServerConnected: false,
		isConfigured: false,
		stats: null,
		error: null,
		reconnectAttempts: 0,
		maxReconnectAttempts: 5,
		reconnectInterval: 3000,
		isReconnecting: false,
		clientId: "",
		clientName: "",
		lastMLPingTime: 0,
		healthStatus: null,
		isLoading: false,
		activeClients: new Map(),
		selectedClientId: null,
		lastStreamUpdate: {},
		processedFrames: new Map(),
		streamCheckInterval: null,
		isProcessing: false,
		isMLProcessingEnabled: false,
		processingStats: {
			frameCount: 0,
			fps: 0,
		},
	}),

	getters: {
		getMLHttpUrl: (state): string => {
			const serverStore = useServerStore();
			return serverStore.isConfigured ? `${serverStore.getHttpUrl}/ml` : "";
		},

		getMLWsUrl: (state): string => {
			const serverStore = useServerStore();
			return serverStore.isConfigured
				? `${serverStore.getWsUrl.replace("/ws", "/ml/ws")}`
				: "";
		},

		getMLStats: (state) => state.stats,

		isMLHealthy: (state): boolean => state.isConnected && !state.error,

		clientsList: (state): StreamClient[] =>
			Array.from(state.activeClients.values()),

		hasActiveStreams: (state): boolean =>
			Array.from(state.activeClients.values()).some(
				(client) => client.isStreaming
			),

		streamingClientsCount: (state): number =>
			Array.from(state.activeClients.values()).filter(
				(client) => client.isStreaming
			).length,

		getClientById:
			(state) =>
			(clientId: string): StreamClient | undefined =>
				state.activeClients.get(clientId),

		getClientFrames:
			(state) =>
			(clientId: string): ProcessedFrame[] =>
				state.processedFrames.get(clientId) || [],

		getStreamDuration:
			(state) =>
			(clientId: string): number => {
				const client = state.activeClients.get(clientId);
				if (client?.metrics.startTime && client.isStreaming) {
					return Date.now() - client.metrics.startTime;
				}
				return 0;
			},
	},

	actions: {
		async checkHealth(): Promise<HealthCheckResult> {
			if (!this.getMLHttpUrl) {
				return {
					ok: false,
					message: "ML server not configured",
				};
			}

			this.isLoading = true;
			this.error = null;

			try {
				const response = await fetch(`${this.getMLHttpUrl}/health`, {
					headers: {
						Accept: "application/json",
						"ngrok-skip-browser-warning": "true",
					},
				});

				if (!response.ok) {
					throw new Error("ML server health check failed");
				}

				const data = await response.json();
				this.stats = data.connections;
				this.isConfigured = true;

				const result = {
					ok: true,
					message: "ML server is healthy",
					connections: data.connections,
				};

				this.healthStatus = result;
				this.error = null;
				return result;
			} catch (error) {
				const message =
					error instanceof Error ? error.message : "Unknown error";
				this.error = message;
				this.isConfigured = false;

				const result = {
					ok: false,
					message: `ML server health check failed: ${message}`,
				};

				this.healthStatus = result;
				return result;
			} finally {
				this.isLoading = false;
			}
		},

		async autoConnect(): Promise<boolean> {
			try {
				if (!this.isConnected) {
					await this.connect();
				}
				if (!this.isServerConnected) {
					await this.connectServer();
				}
				return this.isConnected && this.isServerConnected;
			} catch (error) {
				console.error("ML auto-connect error:", error);
				return false;
			}
		},

		async connect(clientName?: string): Promise<boolean> {
			try {
				if (this.socket) {
					this.socket.close();
				}

				let wsUrl = this.getMLWsUrl;
				if (clientName) {
					wsUrl += `?client_name=${encodeURIComponent(clientName)}`;
				}

				return new Promise((resolve) => {
					this.socket = new WebSocket(wsUrl);

					this.socket.onopen = () => {
						this.isConnected = true;
						this.reconnectAttempts = 0;
						this.isReconnecting = false;
						this.error = null;
						resolve(true);
					};

					this.socket.onmessage = this.handleWebSocketMessage.bind(this);

					this.socket.onerror = () => {
						this.error = "WebSocket error occurred";
						this.isConnected = false;
						resolve(false);
					};

					setTimeout(() => resolve(false), 5000);
				});
			} catch (error) {
				this.error =
					error instanceof Error
						? error.message
						: "Failed to connect to ML server";
				return false;
			}
		},

		async connectServer(): Promise<boolean> {
			try {
				if (this.serverSocket) {
					this.serverSocket.close();
				}

				const wsUrl = `${this.getMLWsUrl}/server`;

				return new Promise((resolve) => {
					this.serverSocket = new WebSocket(wsUrl);

					this.serverSocket.onopen = () => {
						this.isServerConnected = true;
						this.error = null;
						resolve(true);
					};

					this.serverSocket.onmessage =
						this.handleServerWebSocketMessage.bind(this);

					this.serverSocket.onerror = () => {
						this.error = "Server WebSocket error occurred";
						this.isServerConnected = false;
						resolve(false);
					};

					setTimeout(() => resolve(false), 5000);
				});
			} catch (error) {
				this.error =
					error instanceof Error
						? error.message
						: "Failed to connect server to ML server";
				return false;
			}
		},

		disconnect() {
			if (this.socket) {
				this.socket.close();
				this.socket = null;
			}
			this.isConnected = false;
			this.clientId = "";
			this.clientName = "";
			this.reconnectAttempts = 0;
			this.isReconnecting = false;
			this.clearProcessedStreams();
		},

		disconnectServer() {
			if (this.serverSocket) {
				this.serverSocket.close();
				this.serverSocket = null;
			}
			this.isServerConnected = false;
		},

		resetError() {
			this.error = null;
		},

		handleWebSocketMessage(event: MessageEvent) {
			try {
				const data = JSON.parse(event.data);

				switch (data.type) {
					case "connection_info":
						this.clientId = data.client_id;
						this.clientName = data.name;
						this.initializeClient(this.clientId, this.clientName, true);
						break;

					case "processed_frame":
						this.handleProcessedFrame(data);
						break;

					case "streaming_status":
						this.handleStreamingStatusUpdate(data.client_id, data.is_streaming);
						break;

					case "metrics_update":
						this.handleMetricsUpdate(data);
						break;
				}
			} catch (error) {
				console.error("Error processing WebSocket message:", error);
			}
		},

		handleServerWebSocketMessage(event: MessageEvent) {
			try {
				const data = JSON.parse(event.data);

				if (data.type === "error") {
					this.error = data.message;
				}
			} catch (error) {
				console.error("Error processing server WebSocket message:", error);
			}
		},

		async sendFrame(frameData: string, timestamp?: string): Promise<boolean> {
			if (!this.isMLProcessingEnabled || !this.isConnected) {
				return false;
			}

			try {
				const frameMessage = {
					type: "frame",
					content: frameData, // This should already include the data:image/jpeg;base64 prefix
					timestamp: timestamp || new Date().toISOString(),
				};

				if (this.socket?.readyState === WebSocket.OPEN) {
					this.socket.send(JSON.stringify(frameMessage));
					this.isProcessing = true;
					this.processingStats.frameCount++;
					return true;
				}
			} catch (error) {
				console.error("Error sending frame to ML server:", error);
				this.error =
					error instanceof Error ? error.message : "Failed to send frame";
			}

			return false;
		},

		clearProcessedStreams() {
			this.activeClients.clear();
			this.processedFrames.clear();
			this.lastStreamUpdate = {};
			this.selectedClientId = null;
			this.isProcessing = false;
			this.processingStats = {
				frameCount: 0,
				fps: 0,
			};
		},

		initializeClient(
			clientId: string,
			displayName: string,
			isLocal: boolean = false
		) {
			if (!this.activeClients.has(clientId)) {
				const now = Date.now();
				this.activeClients.set(clientId, {
					id: clientId,
					displayName: isLocal ? `${displayName} (You)` : displayName,
					lastFrame: null,
					isStreaming: false,
					metrics: {
						frameCount: 0,
						fps: 0,
						startTime: null,
						lastUpdateTime: now,
					},
					isLocal,
				});
				this.lastStreamUpdate[clientId] = now;
			}
		},

		handleProcessedFrame(data: any) {
			const clientId = data.client_id;
			const frame: ProcessedFrame = {
				id: Math.random().toString(36).substr(2, 9),
				content: data.content,
				timestamp: data.timestamp,
				client_id: clientId,
			};

			if (!this.processedFrames.has(clientId)) {
				this.processedFrames.set(clientId, []);
			}
			this.processedFrames.get(clientId)?.push(frame);

			const client = this.activeClients.get(clientId);
			if (client) {
				const now = Date.now();
				this.activeClients.set(clientId, {
					...client,
					lastFrame: data.content,
					isStreaming: true,
					metrics: {
						...client.metrics,
						frameCount: client.metrics.frameCount + 1,
						startTime: client.metrics.startTime || now,
						lastUpdateTime: now,
					},
				});
				this.lastStreamUpdate[clientId] = now;
			}

			// Update processing status
			this.isProcessing = false;
			const duration =
				(Date.now() - (client?.metrics.startTime || Date.now())) / 1000;
			if (duration > 0) {
				this.processingStats.fps = Math.round(
					this.processingStats.frameCount / duration
				);
			}
		},
	},

	persist: {
		paths: ["isConfigured", "selectedClientId", "isMLProcessingEnabled"],
	},
});