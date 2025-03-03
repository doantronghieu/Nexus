import { ref, onMounted, onUnmounted } from "vue";
import { useRuntimeConfig } from "nuxt/app";

export const useWebSocket = () => {
	const config = useRuntimeConfig();
	const ws = ref<WebSocket | null>(null);
	const isConnected = ref(false);
	const reconnectAttempts = ref(0);
	const maxReconnectAttempts = 5;

	const connect = () => {
		if (ws.value?.readyState === WebSocket.OPEN) return;

		ws.value = new WebSocket(`${config.public.wsBaseUrl}/ws`);

		ws.value.onopen = () => {
			console.log("WebSocket connected");
			isConnected.value = true;
			reconnectAttempts.value = 0;
		};

		ws.value.onclose = () => {
			console.log("WebSocket disconnected");
			isConnected.value = false;

			// Attempt to reconnect
			if (reconnectAttempts.value < maxReconnectAttempts) {
				reconnectAttempts.value++;
				setTimeout(connect, 1000 * Math.pow(2, reconnectAttempts.value - 1));
			}
		};

		ws.value.onerror = (error) => {
			console.error("WebSocket error:", error);
		};
	};

	const disconnect = () => {
		if (ws.value) {
			ws.value.close();
			ws.value = null;
			isConnected.value = false;
		}
	};

	const sendMessage = (data: ArrayBuffer) => {
		if (ws.value?.readyState === WebSocket.OPEN) {
			ws.value.send(data);
		}
	};

	onMounted(() => {
		connect();
	});

	onUnmounted(() => {
		disconnect();
	});

	return {
		isConnected,
		sendMessage,
		connect,
		disconnect,
	};
};
