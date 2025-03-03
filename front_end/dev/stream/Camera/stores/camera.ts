import { defineStore } from 'pinia'
import { useWebSocketStore } from './websocket'
import { useStreamsStore } from './streams'
import { useMLStore } from "./ml";

interface CameraState {
  stream: MediaStream | null;
  currentDevice: string | null;
  isFlipped: boolean;
  isRecording: boolean;
  selectedFps: string;
  captureCount: number;
  recordingStartTime: number | null;
  recordingDuration: string;
  error: string | null;
  offscreenVideo: HTMLVideoElement | null;
}

export const useCameraStore = defineStore("camera", {
	state: (): CameraState => ({
		stream: null as MediaStream | null,
		currentDevice: null as string | null,
		isFlipped: true,
		isRecording: false,
		selectedFps: "5",
		captureCount: 0,
		recordingStartTime: null as number | null,
		recordingDuration: "00:00:00",
		error: null as string | null,
		offscreenVideo: null as HTMLVideoElement | null,
	}),

	actions: {
		createOffscreenVideo() {
			if (this.offscreenVideo) {
				this.offscreenVideo.srcObject = null;
			}

			// Create a new video element for offscreen processing
			const video = document.createElement("video");
			video.autoplay = true;
			video.muted = true;
			video.playsInline = true;

			if (this.stream) {
				video.srcObject = this.stream;
			}

			this.offscreenVideo = video;

			// Handle play promise to avoid uncaught rejection
			const playPromise = video.play();
			if (playPromise !== undefined) {
				playPromise.catch((error) => {
					console.error("Error playing offscreen video:", error);
				});
			}
		},

		async initializeCamera(deviceId?: string) {
			try {
				const constraints = {
					video: {
						deviceId: deviceId ? { exact: deviceId } : undefined,
						width: { ideal: 1280 },
						height: { ideal: 720 },
					},
				};

				const mediaStream = await navigator.mediaDevices.getUserMedia(
					constraints
				);
				this.stream = mediaStream;
				this.currentDevice = deviceId || null;
				this.error = null;

				// Initialize offscreen video element with the new stream
				this.createOffscreenVideo();
			} catch (err) {
				this.error = "Failed to start camera";
				console.error("Error starting camera:", err);
			}
		},

		async switchCamera(deviceId: string) {
			if (this.stream) {
				this.stream.getTracks().forEach((track) => track.stop());
			}
			await this.initializeCamera(deviceId);
		},

		stopCamera() {
			this.stopRecording();
			if (this.stream) {
				this.stream.getTracks().forEach((track) => track.stop());
				this.stream = null;
			}
			if (this.offscreenVideo) {
				this.offscreenVideo.srcObject = null;
				this.offscreenVideo = null;
			}
			this.captureCount = 0;

			// Update streams store
			const streamsStore = useStreamsStore();
			streamsStore.updateLocalStream(false);
		},

		toggleFlip() {
			this.isFlipped = !this.isFlipped;
		},

		async captureFrameFromVideo(): Promise<string> {
			if (!this.offscreenVideo || !this.stream) {
				throw new Error("No video source available");
			}

			// Create temporary canvas for frame capture
			const canvas = document.createElement("canvas");
			canvas.width = this.offscreenVideo.videoWidth;
			canvas.height = this.offscreenVideo.videoHeight;
			const ctx = canvas.getContext("2d");

			if (!ctx) {
				throw new Error("Could not get canvas context");
			}

			// Apply flip if needed
			if (this.isFlipped) {
				ctx.translate(canvas.width, 0);
				ctx.scale(-1, 1);
			}

			// Ensure video is ready
			if (
				this.offscreenVideo.readyState === this.offscreenVideo.HAVE_ENOUGH_DATA
			) {
				ctx.drawImage(this.offscreenVideo, 0, 0);
				// Ensure we include the proper data URL prefix for base64 image
				return canvas.toDataURL("image/jpeg", 0.8); // This includes 'data:image/jpeg;base64,' prefix
			} else {
				throw new Error("Video not ready");
			}
		},

		async captureFrame({ showEffects = true } = {}) {
			const webSocketStore = useWebSocketStore();
			const mlStore = useMLStore();
			const streamsStore = useStreamsStore();

			if (!this.stream || !webSocketStore.isConnected) {
				return;
			}

			try {
				// Capture frame using offscreen video element
				const frame = await this.captureFrameFromVideo();
				if (!frame) return;

				const timestamp = new Date().toISOString();
				const frameMessage = {
					type: "frame",
					content: frame, // This now includes the data:image/jpeg;base64 prefix
					timestamp: timestamp,
					isStream: !showEffects,
				};

				// Send to main server
				webSocketStore.sendMessage(frameMessage);

				// Send to ML server if enabled
				if (mlStore.isMLProcessingEnabled && mlStore.isConnected) {
					await mlStore.sendFrame(frame, timestamp);
				}

				// Update streams store with local frame
				if (this.isRecording) {
					streamsStore.updateLocalStream(true, frame);
				}

				this.captureCount++;
			} catch (err) {
				console.error("Error capturing frame:", err);
				this.error = "Failed to capture frame";
				if (this.isRecording) {
					this.stopRecording();
				}
			}
		},

		startRecording() {
			if (!this.stream || this.isRecording) return;

			this.isRecording = true;
			this.captureCount = 0;
			this.recordingStartTime = Date.now();
			this.recordingDuration = "00:00:00";

			// Update streams store
			const streamsStore = useStreamsStore();
			streamsStore.updateLocalStream(true);

			// Start duration timer and frame capture
			this.startDurationTimer();
			this.startFrameCapture();
		},

		stopRecording() {
			this.isRecording = false;
			this.recordingStartTime = null;
			this.captureCount = 0;
			this.recordingDuration = "00:00:00";

			// Update streams store
			const streamsStore = useStreamsStore();
			streamsStore.updateLocalStream(false);

			if (this.durationTimer) {
				clearInterval(this.durationTimer);
			}
			if (this.captureTimer) {
				cancelAnimationFrame(this.captureTimer);
			}
		},

		// Private fields for timers
		durationTimer: null as number | null,
		captureTimer: null as number | null,
		lastFrameTime: 0,

		startDurationTimer() {
			this.durationTimer = window.setInterval(() => {
				if (this.recordingStartTime) {
					const duration = Date.now() - this.recordingStartTime;
					this.recordingDuration = this.formatDuration(duration);
				}
			}, 1000);
		},

		async startFrameCapture() {
			const mlStore = useMLStore();
			const frameInterval = 1000 / parseInt(this.selectedFps);
			this.lastFrameTime = performance.now();

			const captureLoop = async () => {
				if (!this.isRecording) return;

				const now = performance.now();
				if (now - this.lastFrameTime >= frameInterval) {
					this.lastFrameTime = now;

					// Capture frame
					try {
						const frame = await this.captureFrame({ showEffects: false });
						if (frame) {
							this.captureCount++;
							const timestamp = new Date().toISOString();

							// Send to ML server if ML processing is enabled
							if (mlStore.isMLProcessingEnabled && mlStore.isConnected) {
								await mlStore.sendFrame(frame, timestamp);
							}
						}
					} catch (error) {
						console.error("Error capturing frame:", error);
						this.error =
							error instanceof Error ? error.message : "Frame capture failed";
						this.stopRecording();
						return;
					}
				}

				this.captureTimer = requestAnimationFrame(captureLoop);
			};

			this.captureTimer = requestAnimationFrame(captureLoop);
		},

		formatDuration(milliseconds: number): string {
			const seconds = Math.floor(milliseconds / 1000);
			const hours = Math.floor(seconds / 3600);
			const minutes = Math.floor((seconds % 3600) / 60);
			const remainingSeconds = seconds % 60;

			const pad = (num: number): string => num.toString().padStart(2, "0");
			return `${pad(hours)}:${pad(minutes)}:${pad(remainingSeconds)}`;
		},
	},

	persist: {
		paths: ["isFlipped", "selectedFps"],
	},
});