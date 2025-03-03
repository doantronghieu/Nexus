import { ref, onMounted, onUnmounted } from "vue";
import { v4 as uuidv4 } from "uuid";
import { useConfig } from "./useConfig";

/**
 * Handles WebRTC peer connections and signaling
 * @returns {Object} WebRTC controls and state
 */
export function useWebRTC() {
	const { getWSEndpoint } = useConfig();

	const peerConnection = ref(null);
	const localStream = ref(null);
	const remoteStream = ref(null);
	const isConnected = ref(false);
	const error = ref(null);
	const ws = ref(null);
	const clientId = ref(uuidv4());
	const remoteClientId = ref(null);
	let reconnectTimeout = null;

	// WebRTC configuration
	const configuration = {
		iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
	};

	/**
	 * Safely sends a message through WebSocket
	 * @param {Object} message - Message to send
	 */
	function sendWebSocketMessage(message) {
		if (ws.value?.readyState === WebSocket.OPEN) {
			ws.value.send(JSON.stringify(message));
		} else {
			throw new Error("WebSocket is not connected");
		}
	}

	/**
	 * Creates and configures a new RTCPeerConnection
	 */
	function createPeerConnection() {
		if (peerConnection.value) {
			peerConnection.value.close();
		}

		peerConnection.value = new RTCPeerConnection(configuration);

		peerConnection.value.onicecandidate = ({ candidate }) => {
			if (candidate && remoteClientId.value) {
				try {
					sendWebSocketMessage({
						type: "ice-candidate",
						candidate,
						targetId: remoteClientId.value,
					});
				} catch (err) {
					console.error("Failed to send ICE candidate:", err);
				}
			}
		};

		peerConnection.value.ontrack = (event) => {
			remoteStream.value = event.streams[0];
		};

		peerConnection.value.onconnectionstatechange = () => {
			const state = peerConnection.value?.connectionState;
			isConnected.value = state === "connected";

			if (state === "failed" || state === "closed") {
				handleConnectionFailure();
			}
		};

		// Monitor ICE connection state
		peerConnection.value.oniceconnectionstatechange = () => {
			if (peerConnection.value?.iceConnectionState === "failed") {
				handleIceFailure();
			}
		};
	}

	/**
	 * Handles WebRTC connection failures
	 */
	async function handleConnectionFailure() {
		console.log("Connection failed, attempting recovery...");
		if (peerConnection.value && isConnected.value) {
			await restartConnection();
		}
	}

	/**
	 * Handles ICE connection failures
	 */
	async function handleIceFailure() {
		console.log("ICE connection failed, restarting...");
		try {
			if (peerConnection.value) {
				const offer = await peerConnection.value.createOffer({
					iceRestart: true,
				});
				await peerConnection.value.setLocalDescription(offer);
				sendWebSocketMessage({ type: "offer", offer });
			}
		} catch (err) {
			console.error("ICE restart failed:", err);
			await restartConnection();
		}
	}

	/**
	 * Restarts the entire WebRTC connection
	 */
	async function restartConnection() {
		cleanup();
		await new Promise((resolve) => setTimeout(resolve, 1000));
		connectWebSocket();
	}

	/**
	 * Handles incoming signaling messages
	 */
	async function handleSignalingMessage(data) {
		try {
			if (!peerConnection.value) {
				createPeerConnection();
			}

			switch (data.type) {
				case "offer": {
					remoteClientId.value = data.clientId || null;
					await peerConnection.value.setRemoteDescription(
						new RTCSessionDescription(data.offer)
					);
					const answer = await peerConnection.value.createAnswer();
					await peerConnection.value.setLocalDescription(answer);

					if (remoteClientId.value) {
						sendWebSocketMessage({
							type: "answer",
							answer,
							targetId: remoteClientId.value,
						});
					}
					break;
				}

				case "answer":
					await peerConnection.value.setRemoteDescription(
						new RTCSessionDescription(data.answer)
					);
					break;

				case "ice-candidate":
					if (data.candidate) {
						await peerConnection.value.addIceCandidate(
							new RTCIceCandidate(data.candidate)
						);
					}
					break;

				case "client-disconnected":
					if (data.clientId === remoteClientId.value) {
						cleanup();
					}
					break;
			}
		} catch (err) {
			error.value = "Failed to handle signaling message";
			console.error("Signaling error:", err);
		}
	}

	/**
	 * Establishes WebSocket connection for signaling
	 */
	function connectWebSocket() {
		try {
			const wsUrl = getWSEndpoint(clientId.value);
			ws.value = new WebSocket(wsUrl);

			ws.value.onopen = () => {
				console.log("WebSocket connected");
				error.value = null;
				if (reconnectTimeout) {
					clearTimeout(reconnectTimeout);
					reconnectTimeout = null;
				}
			};

			ws.value.onmessage = async (event) => {
				try {
					const data = JSON.parse(event.data);
					await handleSignalingMessage(data);
				} catch (err) {
					console.error("Failed to parse WebSocket message:", err);
				}
			};

			ws.value.onerror = (err) => {
				console.error("WebSocket Error:", err);
				error.value = "WebSocket connection error";
			};

			ws.value.onclose = () => {
				console.log("WebSocket connection closed");
				isConnected.value = false;

				// Implement exponential backoff for reconnection
				if (!reconnectTimeout) {
					const backoffDelay = Math.min(
						1000 * Math.pow(2, reconnectAttempts),
						30000
					);
					reconnectTimeout = setTimeout(() => {
						reconnectTimeout = null;
						connectWebSocket();
					}, backoffDelay);
				}
			};
		} catch (err) {
			error.value = "Failed to connect to signaling server";
			console.error("WebSocket connection error:", err);
		}
	}

	/**
	 * Starts streaming media through WebRTC
	 * @param {MediaStream} stream - Media stream to send
	 */
	async function startStream(stream) {
		try {
			localStream.value = stream;
			createPeerConnection();

			// Optimize media quality based on connection
			const videoTrack = stream.getVideoTracks()[0];
			if (videoTrack) {
				const capabilities = videoTrack.getCapabilities();
				const settings = {
					width: Math.min(capabilities.width.max, 1280),
					height: Math.min(capabilities.height.max, 720),
					frameRate: Math.min(capabilities.frameRate.max, 30),
				};
				await videoTrack.applyConstraints(settings);
			}

			stream.getTracks().forEach((track) => {
				peerConnection.value?.addTrack(track, stream);
			});

			const offer = await peerConnection.value.createOffer();
			await peerConnection.value.setLocalDescription(offer);

			sendWebSocketMessage({ type: "offer", offer });
		} catch (err) {
			error.value = "Failed to start stream";
			console.error("Stream error:", err);
		}
	}

	/**
	 * Cleans up resources and connections
	 */
	function cleanup() {
		if (peerConnection.value) {
			peerConnection.value.close();
			peerConnection.value = null;
		}

		if (ws.value) {
			ws.value.close();
			ws.value = null;
		}

		if (reconnectTimeout) {
			clearTimeout(reconnectTimeout);
			reconnectTimeout = null;
		}

		if (localStream.value) {
			localStream.value.getTracks().forEach((track) => track.stop());
			localStream.value = null;
		}

		remoteStream.value = null;
		remoteClientId.value = null;
		isConnected.value = false;
		error.value = null;
	}

	onMounted(() => {
		connectWebSocket();
	});

	onUnmounted(() => {
		cleanup();
	});

	return {
		localStream,
		remoteStream,
		isConnected,
		error,
		clientId: clientId.value,
		startStream,
		cleanup,
	};
}
