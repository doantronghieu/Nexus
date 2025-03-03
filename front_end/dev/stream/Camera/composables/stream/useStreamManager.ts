import { ref, computed } from "vue";
import { useWebSocketStore } from "@/stores/websocket";
import { useMLStore } from "@/stores/ml";

export interface StreamingTarget {
	id: string;
	name: string;
	enabled: boolean;
	isConnected: boolean;
	isProcessing: boolean;
	error: string | null;
}

export interface StreamStats {
	streamCount: number;
	frameCount: number;
	avgFps: number;
}

export function useStreamManager() {
	// Store instances
	const webSocketStore = useWebSocketStore();
	const mlStore = useMLStore();

	// State
	const targets = ref<StreamingTarget[]>([
		{
			id: "main",
			name: "Main Server",
			enabled: true,
			isConnected: false,
			isProcessing: false,
			error: null,
		},
		{
			id: "ml",
			name: "ML Processing",
			enabled: false,
			isConnected: false,
			isProcessing: false,
			error: null,
		},
	]);

	const stats = ref<Record<string, StreamStats>>({
		main: { streamCount: 0, frameCount: 0, avgFps: 0 },
		ml: { streamCount: 0, frameCount: 0, avgFps: 0 },
	});

	// Computed
	const activeTargets = computed(() =>
		targets.value.filter((target) => target.enabled)
	);

	const isStreamingEnabled = computed(
		() =>
			activeTargets.value.length > 0 &&
			activeTargets.value.some((target) => target.isConnected)
	);

	const hasStreamingErrors = computed(() =>
		activeTargets.value.some((target) => target.error !== null)
	);

	// Methods
	const toggleTarget = (targetId: string, enabled?: boolean) => {
		const target = targets.value.find((t) => t.id === targetId);
		if (target) {
			target.enabled = enabled ?? !target.enabled;
		}
	};

	const updateConnectionStatus = () => {
		// Update main server status
		const mainTarget = targets.value.find((t) => t.id === "main");
		if (mainTarget) {
			mainTarget.isConnected = webSocketStore.isConnected;
			mainTarget.error = webSocketStore.error;
		}

		// Update ML server status
		const mlTarget = targets.value.find((t) => t.id === "ml");
		if (mlTarget) {
			mlTarget.isConnected = mlStore.isConnected && mlStore.isServerConnected;
			mlTarget.error = mlStore.error;
		}
	};

	const updateStreamStats = (targetId: string, stats: Partial<StreamStats>) => {
		if (targetId in stats.value) {
			stats.value[targetId] = {
				...stats.value[targetId],
				...stats,
			};
		}
	};

	const sendFrame = async (frameData: string, timestamp?: string) => {
		const frameMessage = {
			type: "frame",
			content: frameData,
			timestamp: timestamp || new Date().toISOString(),
		};

		const sendPromises: Promise<boolean>[] = [];

		// Send to enabled and connected targets
		for (const target of activeTargets.value) {
			try {
				target.isProcessing = true;
				target.error = null;

				if (target.id === "main" && target.isConnected) {
					sendPromises.push(
						Promise.resolve(
							webSocketStore.sendMessage(JSON.stringify(frameMessage))
						)
					);
				} else if (target.id === "ml" && target.isConnected) {
					sendPromises.push(
						Promise.resolve(
							mlStore.socket?.send(JSON.stringify(frameMessage)) ?? false
						)
					);
				}
			} catch (error) {
				target.error =
					error instanceof Error ? error.message : "Frame sending failed";
				target.isProcessing = false;
			}
		}

		try {
			// Wait for all sends to complete
			const results = await Promise.allSettled(sendPromises);

			// Update processing status
			activeTargets.value.forEach((target) => {
				target.isProcessing = false;
			});

			// Return true if all sends were successful
			return results.every(
				(result) => result.status === "fulfilled" && result.value
			);
		} catch (error) {
			console.error("Error sending frames:", error);
			return false;
		}
	};

	const connect = async () => {
		const connectPromises: Promise<boolean>[] = [];

		for (const target of activeTargets.value) {
			target.error = null;

			if (target.id === "main" && !target.isConnected) {
				connectPromises.push(webSocketStore.autoConnect());
			} else if (target.id === "ml" && !target.isConnected) {
				connectPromises.push(mlStore.autoConnect());
			}
		}

		try {
			await Promise.all(connectPromises);
			updateConnectionStatus();
			return true;
		} catch (error) {
			console.error("Error connecting to servers:", error);
			return false;
		}
	};

	const disconnect = () => {
		for (const target of activeTargets.value) {
			if (target.id === "main") {
				webSocketStore.disconnect();
			} else if (target.id === "ml") {
				mlStore.disconnect();
			}
			target.isConnected = false;
			target.isProcessing = false;
			target.error = null;
		}
	};

	const resetErrors = () => {
		for (const target of targets.value) {
			target.error = null;
		}
		webSocketStore.resetError();
		mlStore.resetError();
	};

	// Watch for connection status changes
	watch(
		() => [
			webSocketStore.isConnected,
			mlStore.isConnected,
			mlStore.isServerConnected,
		],
		() => {
			updateConnectionStatus();
		}
	);

	return {
		// State
		targets,
		stats,

		// Computed
		activeTargets,
		isStreamingEnabled,
		hasStreamingErrors,

		// Methods
		toggleTarget,
		updateConnectionStatus,
		updateStreamStats,
		sendFrame,
		connect,
		disconnect,
		resetErrors,
	};
}
