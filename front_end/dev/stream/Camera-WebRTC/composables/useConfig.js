import { reactive, ref, computed, onMounted } from "vue";
import { v4 as uuidv4 } from "uuid";

// Singleton state for the WebSocket connection
let globalConnection = null;
let globalClientId = null;
let messageHandlers = new Set();

/**
 * Provides centralized configuration and connection management
 * @returns {Object} Configuration and connection utilities
 */
export function useConfig() {
	const config = reactive({
		fastAPI: {
			protocol: "https",
			host:
				typeof window !== "undefined" ? window.location.hostname : "localhost",
			port: 8000,
			wsProtocol: "wss",
		},
		nuxtAPI: {
			protocol: "https",
			host: "localhost",
			port: 3000,
			wsProtocol: "wss",
		},
		endpoints: {
			ws: "/ws",
			frames: "/frames",
		},
	});

	// Server info state
	const serverInfo = ref(null);
	const isLoading = ref(false);
	const error = ref(null);

	// Connection state
	const connection = reactive({
		status: ref({
			state: "disconnected",
			message: "Not connected",
		}),
		reconnectAttempts: 0,
		reconnectTimeout: null,
		heartbeatInterval: null,
	});

	// Connection settings
	const CONNECTION_SETTINGS = {
		MAX_RECONNECT_ATTEMPTS: 5,
		RECONNECT_INTERVAL: 3000,
		HEARTBEAT_INTERVAL: 30000,
	};

	const getFastAPIBaseUrl = () => {
		return `${config.fastAPI.protocol}://${config.fastAPI.host}:${config.fastAPI.port}`;
	};

	const getFastAPIWSBaseUrl = () => {
		return `${config.fastAPI.wsProtocol}://${config.fastAPI.host}:${config.fastAPI.port}`;
	};

	const getWSEndpoint = (clientId) => {
		return `${getFastAPIWSBaseUrl()}${config.endpoints.ws}/${clientId}`;
	};

	const getFramesEndpoint = (clientId) => {
		return `${getFastAPIBaseUrl()}${config.endpoints.frames}/${clientId}`;
	};

	const startHeartbeat = () => {
		if (connection.heartbeatInterval) {
			clearInterval(connection.heartbeatInterval);
		}

		connection.heartbeatInterval = setInterval(() => {
			if (globalConnection?.readyState === WebSocket.OPEN) {
				sendMessage({ type: "heartbeat" });
			}
		}, CONNECTION_SETTINGS.HEARTBEAT_INTERVAL);
	};

	const handleReconnect = () => {
		if (
			connection.reconnectAttempts < CONNECTION_SETTINGS.MAX_RECONNECT_ATTEMPTS
		) {
			connection.reconnectAttempts++;
			const delay =
				CONNECTION_SETTINGS.RECONNECT_INTERVAL *
				Math.pow(2, connection.reconnectAttempts - 1);

			console.log(
				`Attempting reconnect in ${delay}ms (attempt ${connection.reconnectAttempts})`
			);

			if (connection.reconnectTimeout) {
				clearTimeout(connection.reconnectTimeout);
			}

			connection.reconnectTimeout = setTimeout(() => {
				setupWebSocket();
			}, delay);
		} else {
			connection.status.value = {
				state: "error",
				message: "Connection Failed",
			};
		}
	};

	const setupWebSocket = () => {
		// If we already have a connection, just return
		if (globalConnection?.readyState === WebSocket.OPEN) {
			return;
		}

		// Generate clientId if not exists
		globalClientId = globalClientId || uuidv4();

		const wsUrl = getWSEndpoint(globalClientId);
		console.log("Setting up WebSocket connection:", wsUrl);

		try {
			globalConnection = new WebSocket(wsUrl);

			globalConnection.onopen = () => {
				console.log("WebSocket connected");
				connection.status.value = { state: "connected", message: "Connected" };
				connection.reconnectAttempts = 0;
				startHeartbeat();
			};

			globalConnection.onclose = () => {
				console.log("WebSocket closed");
				connection.status.value = {
					state: "disconnected",
					message: "Disconnected",
				};
				handleReconnect();
			};

			globalConnection.onerror = (err) => {
				console.error("WebSocket error:", err);
				connection.status.value = {
					state: "error",
					message: "Connection Error",
				};
			};

			globalConnection.onmessage = (event) => {
				try {
					const data = JSON.parse(event.data);
					messageHandlers.forEach((handler) => handler(data));
				} catch (err) {
					console.error("Failed to parse WebSocket message:", err);
				}
			};
		} catch (err) {
			console.error("Error setting up WebSocket:", err);
			handleReconnect();
		}
	};

	const sendMessage = (message) => {
		if (globalConnection?.readyState === WebSocket.OPEN) {
			globalConnection.send(
				JSON.stringify({
					...message,
					clientId: globalClientId,
				})
			);
			return true;
		}
		return false;
	};

	const addMessageHandler = (handler) => {
		messageHandlers.add(handler);
	};

	const removeMessageHandler = (handler) => {
		messageHandlers.delete(handler);
	};

	const cleanup = () => {
		if (connection.heartbeatInterval) {
			clearInterval(connection.heartbeatInterval);
		}
		if (connection.reconnectTimeout) {
			clearTimeout(connection.reconnectTimeout);
		}
		if (globalConnection) {
			globalConnection.close();
			globalConnection = null;
		}

		connection.status.value = {
			state: "disconnected",
			message: "Not connected",
		};
		connection.reconnectAttempts = 0;
		messageHandlers.clear();
	};

	const fetchServerInfo = async () => {
		try {
			isLoading.value = true;
			error.value = null;
			const response = await fetch(`${getFastAPIBaseUrl()}/server/info`);

			if (!response.ok) {
				throw new Error("Failed to fetch server info");
			}

			const data = await response.json();
			serverInfo.value = data;

			if (data.internal_ips?.length > 0) {
				config.fastAPI.host = data.internal_ips[0];
				localStorage.setItem("fastapi-host", data.internal_ips[0]);
			}
		} catch (err) {
			error.value = err.message;
			console.error("Error fetching server info:", err);
		} finally {
			isLoading.value = false;
		}
	};

  const getCurrentClientId = () => globalClientId

	const initConfig = () => {
		const storedHost = localStorage.getItem("fastapi-host");
		if (storedHost) {
			config.fastAPI.host = storedHost;
		}
		fetchServerInfo();
	};

	onMounted(() => {
		if (!globalConnection) {
			initConfig();
		}
	});

	return {
		config,
		serverInfo,
		isLoading,
		error,
		connectionStatus: computed(() => connection.status.value),
		getFastAPIBaseUrl,
		getFastAPIWSBaseUrl,
		getWSEndpoint,
		getFramesEndpoint,
		setupWebSocket,
		sendMessage,
		addMessageHandler,
		removeMessageHandler,
		cleanup,
		getCurrentClientId,
		globalClientId,
	};
}
