<template>
	<div class="min-h-screen bg-gray-50 p-4 sm:p-6 md:p-8">
		<div class="max-w-4xl mx-auto space-y-6">
			<!-- Header -->
			<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
				<h1 class="text-2xl font-bold text-gray-900 mb-4 sm:mb-0">
					Server Configuration
				</h1>
			</div>

			<!-- Server Configuration Card -->
			<div
				class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden"
			>
				<div class="p-4 sm:p-6">
					<h2 class="text-lg font-semibold text-gray-900 mb-4">
						Connection Settings
					</h2>
					<div class="space-y-4">
						<form @submit.prevent="handleConfigApply" class="space-y-4">
							<!-- Server Input Section -->
							<div
								class="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4"
							>
								<div class="flex-1">
									<div class="relative">
										<!-- Combobox with input -->
										<input
											v-model="localServerHost"
											type="text"
											placeholder="Select or enter server host"
											class="w-full h-12 sm:h-10 px-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-base"
											:class="{
												'border-red-500':
													showValidation && !localServerHost.trim(),
											}"
											@focus="showOptions = true"
										/>
										<!-- Dropdown arrow -->
										<button
											type="button"
											@click="toggleOptions"
											class="absolute inset-y-0 right-0 px-3 flex items-center"
											aria-label="Toggle server options"
										>
											<svg
												class="h-5 w-5 text-gray-400"
												fill="none"
												stroke="currentColor"
												viewBox="0 0 24 24"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M19 9l-7 7-7-7"
												/>
											</svg>
										</button>

										<!-- Options dropdown -->
										<div
											v-if="showOptions"
											class="absolute z-10 w-full mt-1 bg-white border rounded-lg shadow-lg max-h-48 overflow-y-auto"
										>
											<ul class="py-1">
												<li
													v-for="host in predefinedHosts"
													:key="host"
													@click="selectHost(host)"
													class="px-4 py-3 hover:bg-gray-50 cursor-pointer text-base active:bg-gray-100"
													:class="{ 'bg-gray-50': localServerHost === host }"
												>
													{{ host }}
												</li>
											</ul>
										</div>
									</div>

									<p
										v-if="showValidation && !localServerHost.trim()"
										class="mt-2 text-sm text-red-500"
									>
										Please enter a server host
									</p>
								</div>

								<!-- HTTPS Toggle -->
								<div class="flex items-center">
									<label
										class="flex items-center space-x-3 cursor-pointer select-none"
									>
										<input
											type="checkbox"
											v-model="localIsSecure"
											class="w-5 h-5 rounded text-blue-500 focus:ring-2 focus:ring-blue-500 cursor-pointer"
										/>
										<span class="text-gray-700 text-base whitespace-nowrap"
											>HTTPS/WSS</span
										>
									</label>
								</div>
							</div>

							<!-- Apply Button -->
							<div class="flex justify-end">
								<button
									type="submit"
									class="w-full sm:w-auto px-6 py-3 sm:py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-base font-medium transition-colors disabled:opacity-50"
									:disabled="isConfiguring"
								>
									<template v-if="isConfiguring">
										<div class="flex items-center justify-center gap-2">
											<svg
												class="animate-spin h-5 w-5 text-white"
												xmlns="http://www.w3.org/2000/svg"
												fill="none"
												viewBox="0 0 24 24"
											>
												<circle
													class="opacity-25"
													cx="12"
													cy="12"
													r="10"
													stroke="currentColor"
													stroke-width="4"
												></circle>
												<path
													class="opacity-75"
													fill="currentColor"
													d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
												></path>
											</svg>
											<span>Configuring...</span>
										</div>
									</template>
									<template v-else> Apply Configuration </template>
								</button>
							</div>
						</form>

						<!-- Status Display -->
						<div class="mt-4 space-y-3">
							<div
								class="p-4 bg-gray-50 rounded-lg space-y-2 text-sm sm:text-base"
							>
								<div class="flex flex-col sm:flex-row sm:justify-between">
									<span class="font-medium">HTTP URL:</span>
									<span class="font-mono">{{
										serverStore.getHttpUrl || "Not configured"
									}}</span>
								</div>
								<div class="flex flex-col sm:flex-row sm:justify-between">
									<span class="font-medium">WebSocket URL:</span>
									<span class="font-mono">{{
										serverStore.getWsUrl || "Not configured"
									}}</span>
								</div>
								<div class="flex flex-col sm:flex-row sm:justify-between">
									<span class="font-medium">ML HTTP URL:</span>
									<span class="font-mono">{{
										mlStore.getMLHttpUrl || "Not configured"
									}}</span>
								</div>
								<div class="flex flex-col sm:flex-row sm:justify-between">
									<span class="font-medium">ML WebSocket URL:</span>
									<span class="font-mono">{{
										mlStore.getMLWsUrl || "Not configured"
									}}</span>
								</div>
							</div>
							<div
								v-if="serverStore.isConfigured"
								class="flex items-center text-green-600 font-medium"
							>
								<svg
									class="w-5 h-5 mr-2"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M5 13l4 4L19 7"
									/>
								</svg>
								Server configuration applied
							</div>
						</div>

						<!-- Configuration Progress -->
						<div
							v-if="isConfiguring"
							class="mt-6 border rounded-lg overflow-hidden bg-white"
						>
							<div class="px-4 py-3 bg-blue-50 border-b border-blue-100">
								<h3 class="text-sm font-medium text-blue-900">
									Configuration Progress
								</h3>
							</div>
							<div class="p-4 space-y-3">
								<div
									v-for="(step, index) in configSteps"
									:key="index"
									class="flex items-center gap-3"
								>
									<!-- Status Icon -->
									<div
										class="w-6 h-6 flex-shrink-0 rounded-full flex items-center justify-center"
										:class="{
											'bg-blue-500': step.completed,
											'bg-blue-100': step.inProgress,
											'bg-gray-200':
												!step.completed && !step.inProgress && !step.error,
											'bg-red-500': step.error,
										}"
									>
										<template v-if="step.completed">
											<svg
												class="w-4 h-4 text-white"
												fill="none"
												viewBox="0 0 24 24"
												stroke="currentColor"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M5 13l4 4L19 7"
												/>
											</svg>
										</template>
										<template v-else-if="step.inProgress">
											<svg
												class="w-4 h-4 text-blue-500 animate-spin"
												xmlns="http://www.w3.org/2000/svg"
												fill="none"
												viewBox="0 0 24 24"
											>
												<circle
													class="opacity-25"
													cx="12"
													cy="12"
													r="10"
													stroke="currentColor"
													stroke-width="4"
												></circle>
												<path
													class="opacity-75"
													fill="currentColor"
													d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
												></path>
											</svg>
										</template>
										<template v-else-if="step.error">
											<svg
												class="w-4 h-4 text-white"
												fill="none"
												viewBox="0 0 24 24"
												stroke="currentColor"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M6 18L18 6M6 6l12 12"
												/>
											</svg>
										</template>
										<template v-else>
											<span class="text-xs text-gray-500">{{ index + 1 }}</span>
										</template>
									</div>

									<!-- Step Label and Error -->
									<div class="flex-1">
										<div
											class="text-sm font-medium"
											:class="{
												'text-blue-600': step.completed || step.inProgress,
												'text-gray-900':
													!step.completed && !step.inProgress && !step.error,
												'text-red-600': step.error,
											}"
										>
											{{ step.label }}
										</div>
										<div
											v-if="step.error && step.errorMessage"
											class="text-sm text-red-500 mt-1"
										>
											{{ step.errorMessage }}
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Server Status Tabs -->
			<div
				class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden"
			>
				<div class="border-b border-gray-100">
					<nav class="flex -mb-px">
						<button
							v-for="tab in tabs"
							:key="tab.id"
							@click="currentTab = tab.id"
							class="flex-1 px-4 py-3 text-center border-b-2 font-medium text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
							:class="[
								currentTab === tab.id
									? 'border-blue-500 text-blue-600'
									: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
							]"
						>
							{{ tab.name }}
						</button>
					</nav>
				</div>

				<!-- Main Server Tab Content -->
				<div v-show="currentTab === 'main'" class="p-4 sm:p-6 space-y-6">
					<!-- Health Check Section -->
					<div>
						<h3 class="text-lg font-semibold text-gray-900 mb-4">
							Server Health
						</h3>
						<ServerHealth ref="serverHealthRef" />
					</div>

					<!-- WebSocket Stats Section -->
					<div>
						<WebSocketStats ref="webSocketStatsRef" />
					</div>

					<!-- WebSocket Connection Section -->
					<div>
						<h3 class="text-lg font-semibold text-gray-900 mb-4">
							WebSocket Test
						</h3>
						<WebSocketConnection ref="webSocketConnectionRef" />
					</div>
				</div>

				<!-- ML Server Tab Content -->
				<div v-show="currentTab === 'ml'" class="p-4 sm:p-6 space-y-6">
					<!-- ML Health Check Section -->
					<div>
						<h3 class="text-lg font-semibold text-gray-900 mb-4">
							ML Server Health
						</h3>
						<MLServerHealth ref="mlServerHealthRef" />
					</div>

					<!-- ML WebSocket Stats Section -->
					<div>
						<MLWebSocketStats ref="mlWebSocketStatsRef" />
					</div>

					<!-- ML WebSocket Connection Section -->
					<div>
						<h3 class="text-lg font-semibold text-gray-900 mb-4">
							ML WebSocket Test
						</h3>
						<MLWebSocketConnection ref="mlWebSocketConnectionRef" />
					</div>
				</div>
			</div>
		</div>

		<!-- Touch-friendly bottom spacing for mobile -->
		<div class="h-16 sm:h-0"></div>
	</div>
</template>

// File:
/Users/thung/Documents/Me/Coding/Embedded-AI/front_end/dev/stream/Camera/pages/server-setup.vue
// Script section continued

<script setup lang="ts">
import { ref } from "vue";
import { useServerStore, predefinedHosts } from "@/stores/server";
import { useMLStore } from "@/stores/ml";
import { useWebSocketStore } from "@/stores/websocket";
import { useWebSocketStatsStore } from "@/stores/websocketStats";

// Components
import ServerHealth from "@/components/ServerHealth.vue";
import MLServerHealth from "@/components/MLServerHealth.vue";
import WebSocketStats from "@/components/WebSocketStats.vue";
import MLWebSocketStats from "@/components/MLWebSocketStats.vue";
import WebSocketConnection from "@/components/WebSocketConnection.vue";
import MLWebSocketConnection from "@/components/MLWebSocketConnection.vue";

// Store instantiation
const serverStore = useServerStore();
const mlStore = useMLStore();
const webSocketStore = useWebSocketStore();
const webSocketStatsStore = useWebSocketStatsStore();

// Component refs
const serverHealthRef = ref();
const mlServerHealthRef = ref();
const webSocketStatsRef = ref();
const mlWebSocketStatsRef = ref();
const webSocketConnectionRef = ref();
const mlWebSocketConnectionRef = ref();

// Local state
const localServerHost = ref("");
const localIsSecure = ref(false);
const showValidation = ref(false);
const showOptions = ref(false);
const isConfiguring = ref(false);

// Tab state
const currentTab = ref("main");
const tabs = [
	{ id: "main", name: "Main Server" },
	{ id: "ml", name: "ML Server" },
];

// Configuration step interface
interface ConfigStep {
	label: string;
	completed: boolean;
	error: boolean;
	errorMessage?: string;
	inProgress: boolean;
}

// Configuration steps state
const configSteps = ref<ConfigStep[]>([
	{
		label: "Applying server configuration",
		completed: false,
		error: false,
		inProgress: false,
	},
	{
		label: "Checking main server health",
		completed: false,
		error: false,
		inProgress: false,
	},
	{
		label: "Checking ML server health",
		completed: false,
		error: false,
		inProgress: false,
	},
	{
		label: "Starting statistics monitoring",
		completed: false,
		error: false,
		inProgress: false,
	},
	{
		label: "Establishing WebSocket connections",
		completed: false,
		error: false,
		inProgress: false,
	},
]);

// Step management methods
const updateConfigStep = (
	step: string,
	status: {
		completed?: boolean;
		error?: boolean;
		errorMessage?: string;
		inProgress?: boolean;
	} = {}
) => {
	const stepIndex = {
		config: 0,
		mainHealth: 1,
		mlHealth: 2,
		stats: 3,
		websocket: 4,
	}[step];

	if (stepIndex !== undefined && configSteps.value[stepIndex]) {
		const currentStep = configSteps.value[stepIndex];
		if (status.completed !== undefined) {
			currentStep.completed = status.completed;
			currentStep.inProgress = false;
		}
		if (status.error !== undefined) {
			currentStep.error = status.error;
			currentStep.inProgress = false;
			if (status.errorMessage) {
				currentStep.errorMessage = status.errorMessage;
			}
		}
		if (status.inProgress !== undefined) {
			currentStep.inProgress = status.inProgress;
		}
	}
};

const resetConfigSteps = () => {
	configSteps.value = configSteps.value.map((step) => ({
		...step,
		completed: false,
		error: false,
		errorMessage: undefined,
		inProgress: false,
	}));
};

// Main automation methods
const performHealthChecks = async (): Promise<boolean> => {
	updateConfigStep("mainHealth", { inProgress: true });
	updateConfigStep("mlHealth", { inProgress: true });

	try {
		// Call both health checks directly using component refs
		const [mainResult, mlResult] = await Promise.allSettled([
			serverHealthRef.value?.checkHealth(),
			mlServerHealthRef.value?.checkHealth(),
		]);

		// Handle main server health check result
		if (mainResult.status === "fulfilled") {
			const mainHealthOk = mainResult.value?.ok;
			updateConfigStep("mainHealth", {
				completed: true,
				error: !mainHealthOk,
				errorMessage: mainHealthOk
					? undefined
					: "Main server health check failed",
			});
		} else {
			updateConfigStep("mainHealth", {
				error: true,
				errorMessage: mainResult.reason?.message || "Health check failed",
			});
			return false;
		}

		// Handle ML server health check result
		if (mlResult.status === "fulfilled") {
			const mlHealthOk = mlResult.value?.ok;
			updateConfigStep("mlHealth", {
				completed: true,
				error: !mlHealthOk,
				errorMessage: mlHealthOk ? undefined : "ML server health check failed",
			});
		} else {
			updateConfigStep("mlHealth", {
				error: true,
				errorMessage: mlResult.reason?.message || "ML health check failed",
			});
			// Don't return false here as ML server is optional
		}

		// Return true if main server is healthy
		return mainResult.status === "fulfilled" && mainResult.value?.ok;
	} catch (error) {
		console.error("Health checks failed:", error);
		return false;
	}
};

const startStatsMonitoring = async (): Promise<boolean> => {
	updateConfigStep("stats", { inProgress: true });
	try {
		// Start both stats auto-refresh
		const startMainStats = webSocketStatsRef.value?.startAutoRefresh();
		const startMLStats = mlWebSocketStatsRef.value?.startAutoRefresh();

		const [mainResult, mlResult] = await Promise.allSettled([
			startMainStats,
			startMLStats,
		]);

		const success = mainResult.status === "fulfilled";
		const mlSuccess = mlResult.status === "fulfilled";

		updateConfigStep("stats", {
			completed: success,
			error: !success,
			errorMessage: !success ? "Failed to start stats monitoring" : undefined,
		});

		return success;
	} catch (error) {
		updateConfigStep("stats", {
			error: true,
			errorMessage:
				error instanceof Error ? error.message : "Failed to start monitoring",
		});
		return false;
	}
};

const establishConnections = async (): Promise<boolean> => {
	updateConfigStep("websocket", { inProgress: true });
	try {
		// Connect both WebSockets
		const mainConnected = await webSocketStore.autoConnect();
		const mlConnected = await mlStore.autoConnect();

		const success = mainConnected && mlConnected;
		updateConfigStep("websocket", {
			completed: success,
			error: !success,
			errorMessage: !success
				? "Failed to establish all connections"
				: undefined,
		});
		return success;
	} catch (error) {
		updateConfigStep("websocket", {
			error: true,
			errorMessage:
				error instanceof Error
					? error.message
					: "Failed to establish connections",
		});
		return false;
	}
};

const handleServerSetup = async () => {
	try {
		// Reset state and start configuration
		resetConfigSteps();
		isConfiguring.value = true;

		// 1. Apply server configuration
		updateConfigStep("config", { inProgress: true });
		serverStore.setServerInfo(localServerHost.value, localIsSecure.value);
		updateConfigStep("config", { completed: true });

		// Wait for configuration to be applied
		await nextTick();

		// 2. Check server health
		const healthOk = await performHealthChecks();
		if (!healthOk) {
			console.error("Health checks failed");
			return;
		}

		// 3. Start stats monitoring
		const monitoringStarted = await startStatsMonitoring();
		if (!monitoringStarted) {
			console.error("Failed to start monitoring");
			return;
		}

		// 4. Establish WebSocket connections
		const connectionsEstablished = await establishConnections();
		if (!connectionsEstablished) {
			console.error("Failed to establish connections");
			return;
		}
	} catch (error) {
		console.error("Server setup failed:", error);
	} finally {
		isConfiguring.value = false;
	}
};

const handleConfigApply = async () => {
	showValidation.value = true;
	showOptions.value = false;

	if (localServerHost.value.trim()) {
		await handleServerSetup();
	}
};

// UI interaction methods
const selectHost = (host: string) => {
	localServerHost.value = host;
	showOptions.value = false;
};

const toggleOptions = () => {
	showOptions.value = !showOptions.value;
};

const setupClickOutside = () => {
	const handleClickOutside = (event: MouseEvent) => {
		const form = document.querySelector("form");
		if (form && !form.contains(event.target as Node)) {
			showOptions.value = false;
		}
	};

	document.addEventListener("click", handleClickOutside);
	return () => document.removeEventListener("click", handleClickOutside);
};

// Setup and cleanup
onMounted(() => {
	const cleanup = setupClickOutside();

	// Initialize form with stored values if they exist
	if (serverStore.serverHost) {
		localServerHost.value = serverStore.serverHost;
		localIsSecure.value = serverStore.protocol === "https";
	}

	onUnmounted(cleanup);
});
</script>

<style scoped>
/* Custom scrollbar for dropdown */
.overflow-y-auto {
	scrollbar-width: thin;
	scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
	width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
	background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
	background-color: rgba(156, 163, 175, 0.5);
	border-radius: 3px;
}

/* Prevent text selection on buttons */
button {
	-webkit-tap-highlight-color: transparent;
	-webkit-touch-callout: none;
	user-select: none;
}

/* Font mono urls overflow handling */
.font-mono {
	overflow-wrap: break-word;
	word-break: break-all;
}

/* Configuration steps transition */
.config-step {
	transition: all 0.2s ease-in-out;
}

/* Progress indicator transitions */
.step-icon {
	transition: background-color 0.2s ease-in-out;
}

/* Status indicator transitions */
.status-indicator {
	transition: all 0.2s ease-in-out;
}

/* Improve touch targets on mobile */
@media (max-width: 640px) {
	input[type="checkbox"] {
		min-width: 20px;
		min-height: 20px;
	}

	.cursor-pointer {
		min-height: 44px;
	}

	/* Ensure form inputs have sufficient touch target size */
	input[type="text"],
	select,
	button {
		min-height: 44px;
	}

	/* Adjust spacing for mobile */
	.space-y-4 > :not([hidden]) ~ :not([hidden]) {
		margin-top: 1.5rem;
	}

	/* Improve dropdown usability on mobile */
	.absolute.z-10 {
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 90%;
		max-width: 400px;
		max-height: 80vh;
	}
}

/* Tab transitions */
.tab-content {
	transition: opacity 0.2s ease;
}

.tab-enter-active,
.tab-leave-active {
	transition: opacity 0.2s ease;
}

.tab-enter-from,
.tab-leave-to {
	opacity: 0;
}

/* Safe area insets for notched devices */
@supports (padding: max(0px)) {
	.min-h-screen {
		min-height: max(100vh, -webkit-fill-available);
		padding-top: max(1rem, env(safe-area-inset-top));
		padding-bottom: max(1rem, env(safe-area-inset-bottom));
	}
}
</style>
