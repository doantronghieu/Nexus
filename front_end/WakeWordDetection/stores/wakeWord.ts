import { defineStore } from "pinia";
import { useRuntimeConfig } from "#app";

export const useWakeWordStore = defineStore("wakeWord", {
	state: () => ({
		isRecording: false,
		isWakeWordDetected: false,
		isConnected: false,
		audioContext: null as AudioContext | null,
		mediaStream: null as MediaStream | null,
		ws: null as WebSocket | null,
		connectionAttempts: 0,
		maxRetries: 5,
		events: [] as Array<{
			timestamp: string;
			event: string;
			confidence: number;
		}>,
		systemStatus: {
			wsClients: 0,
			status: "initializing",
		},
	}),

	getters: {
		apiBaseUrl(): string {
			const config = useRuntimeConfig().public;
			return `${config.httpProtocol}://${config.apiHost}:${config.apiPort}`;
		},
		wsBaseUrl(): string {
			const config = useRuntimeConfig().public;
			return `${config.wsProtocol}://${config.apiHost}:${config.apiPort}`;
		},
	},

	actions: {
		async testConnection() {
			try {
				const response = await fetch(`${this.apiBaseUrl}/health`, {
					method: "GET",
					headers: {
						Accept: "application/json",
					},
					credentials: "include", // Add this line
				});
				return response.ok;
			} catch (error) {
				console.error("Connection test failed:", error);
				return false;
			}
		},

		async connectWebSocket() {
			if (this.connectionAttempts >= this.maxRetries) {
				console.error("Max reconnection attempts reached");
				return;
			}

			// Test connection first
			const isConnectable = await this.testConnection();
			if (!isConnectable) {
				console.error("Server not available");
				this.connectionAttempts++;
				const delay = Math.min(
					1000 * Math.pow(2, this.connectionAttempts),
					10000
				);
				setTimeout(() => this.connectWebSocket(), delay);
				return;
			}

			const wsUrl = `${this.wsBaseUrl}/ws`;
			console.log("Connecting to WebSocket:", wsUrl);

			try {
				if (this.ws?.readyState === WebSocket.OPEN) {
					console.log("WebSocket already connected");
					return;
				}

				if (this.ws) {
					this.ws.close();
				}

				this.ws = new WebSocket(wsUrl);

				this.ws.onopen = () => {
					console.log("WebSocket connected successfully");
					this.isConnected = true;
					this.connectionAttempts = 0;
				};

				this.ws.onclose = (event) => {
					console.log("WebSocket closed:", event);
					this.isConnected = false;
					this.connectionAttempts++;

					// Exponential backoff
					const delay = Math.min(
						1000 * Math.pow(2, this.connectionAttempts),
						10000
					);
					setTimeout(() => this.connectWebSocket(), delay);
				};

				this.ws.onerror = (error) => {
					console.error("WebSocket error:", error);
					this.isConnected = false;
				};

				this.ws.onmessage = (event) => {
					try {
						const data = JSON.parse(event.data);
						if (data.event === "wake_word") {
							this.handleWakeWordDetection(data);
						}
					} catch (error) {
						console.error("Error processing message:", error);
					}
				};
			} catch (error) {
				console.error("WebSocket connection error:", error);
				this.isConnected = false;
				this.connectionAttempts++;
			}
		},

		async updateSystemStatus() {
			try {
				const response = await fetch(`${this.apiBaseUrl}/health`, {
					method: "GET",
					headers: {
						Accept: "application/json",
						Origin: "http://localhost:3000",
					},
					mode: "cors", // Explicitly set CORS mode
				});

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				const data = await response.json();
				this.systemStatus = {
					wsClients: data.websocket_clients || 0,
					status: data.status || "error",
				};
			} catch (error) {
				console.error("Error updating system status:", error);
				this.systemStatus.status = "error";
			}
		},

		handleWakeWordDetection(data: any) {
			this.isWakeWordDetected = true;
			this.events.unshift({
				timestamp: new Date().toISOString(),
				event: "wake_word_detected",
				confidence: data.confidence,
			});

			setTimeout(() => {
				this.isWakeWordDetected = false;
			}, 2000);
		},

		async startRecording() {
			try {
				if (!this.audioContext) {
					this.audioContext = new AudioContext({
						sampleRate: 16000,
						latencyHint: "interactive",
					});
				}

				const stream = await navigator.mediaDevices.getUserMedia({
					audio: {
						echoCancellation: true,
						noiseSuppression: true,
						channelCount: 1,
						sampleRate: 16000,
					},
				});

				this.mediaStream = stream;
				const source = this.audioContext.createMediaStreamSource(stream);
				const processor = this.audioContext.createScriptProcessor(1024, 1, 1);

				source.connect(processor);
				processor.connect(this.audioContext.destination);

				processor.onaudioprocess = (e) => {
					if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
						const inputData = e.inputBuffer.getChannelData(0);
						// Convert to 16-bit PCM
						const pcmData = new Int16Array(inputData.length);
						for (let i = 0; i < inputData.length; i++) {
							pcmData[i] = inputData[i] * 32767;
						}
						this.ws.send(pcmData.buffer);
					}
				};

				this.isRecording = true;
			} catch (error) {
				console.error("Failed to start recording:", error);
				throw error;
			}
		},

		stopRecording() {
			if (this.mediaStream) {
				this.mediaStream.getTracks().forEach((track) => track.stop());
				this.mediaStream = null;
			}
			if (this.audioContext) {
				this.audioContext.close();
				this.audioContext = null;
			}
			this.isRecording = false;
		},
	},
});
