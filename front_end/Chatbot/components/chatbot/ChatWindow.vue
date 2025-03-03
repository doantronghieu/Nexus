<template>
	<div
		class="fixed bg-gradient-to-br from-gray-900 to-blue-900 rounded-lg shadow-2xl flex flex-col overflow-hidden transition-all duration-300 ease-in-out backdrop-blur-lg border border-opacity-30 border-blue-400"
		:class="[
			isFullScreen
				? 'top-0 left-0 w-full h-full m-0'
				: 'bottom-4 right-4 w-[480px] h-[600px]',
		]"
	>
		<!-- Header -->
		<div
			class="bg-opacity-30 bg-blue-800 text-white p-4 flex justify-between items-center backdrop-blur-md"
		>
			<h2 class="text-xl font-semibold text-blue-300 cyber-text">IVyEdge</h2>
			<div class="flex items-center space-x-2">
				<Toolbar
					@clear="clearChat"
					@export="exportChat"
					@toggle-theme="toggleDarkMode"
					@open-settings="openSettings"
				/>
				<button
					@click="closeChat"
					class="text-gray-300 hover:text-white transition-colors duration-200"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-6 w-6"
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
				</button>
			</div>
		</div>

		<!-- Chat Area -->
		<div
			class="flex-grow overflow-y-auto p-4 bg-opacity-10 bg-gray-800 backdrop-blur-sm"
			ref="chatContainer"
		>
			<MessageDisplay :messages="messages" />
			<TypingIndicator v-if="isTyping" />
		</div>

		<!-- Input Area -->
		<div
			class="p-4 border-t border-opacity-30 border-blue-400 bg-opacity-30 bg-gray-800 backdrop-blur-md"
		>
			<TextInput @send-message="sendMessage" :disabled="isTyping" />
			<div class="flex justify-between mt-2">
				<div class="flex space-x-2">
					<WakeWordInput @send-message="sendMessage" :disabled="isTyping" />
					<VoiceInput @send-message="sendMessage" :disabled="isTyping" />
				</div>
				<VoiceOutput :text="lastBotMessage" />
			</div>
		</div>

		<!-- Settings Modal -->
		<SettingsDashboard
			:is-open="isSettingsOpen"
			:is-full-screen="isFullScreen"
			@close="closeSettings"
			@toggle-fullscreen="handleFullscreenToggle"
		/>

		<AnimatedBackground />
	</div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from "vue";
import { useMessagesStore } from "~/stores/chatbot/messages";
import { useTokensStore } from "~/stores/chatbot/tokens";
import { useUserPreferencesStore } from "~/stores/chatbot/userPreferences";
import { useAIService } from "~/services/aiHandler";
import MessageDisplay from "./MessageDisplay.vue";
import TextInput from "./TextInput.vue";
import VoiceInput from "./VoiceInput.vue";
import WakeWordInput from "./WakeWordInput.vue";
import VoiceOutput from "./VoiceOutput.vue";
import TypingIndicator from "./TypingIndicator.vue";
import Toolbar from "./Toolbar.vue";
import SettingsDashboard from "./SettingsDashboard.vue";
import AnimatedBackground from "./AnimatedBackground.vue";

const props = defineProps({
	isFullScreen: {
		type: Boolean,
		default: true,
	},
});

const emit = defineEmits([
	"toggle-fullscreen",
	"close-fullscreen",
	"close-chat",
]);

// Store initialization
const messagesStore = useMessagesStore();
const tokensStore = useTokensStore();
const userPreferencesStore = useUserPreferencesStore();

const aiService = useAIService();

// Computed properties for AI settings
const textGenSettings = computed(() =>
	userPreferencesStore.getAISettings("textGeneration")
);
const sttSettings = computed(() =>
	userPreferencesStore.getAISettings("speechToText")
);
const ttsSettings = computed(() =>
	userPreferencesStore.getAISettings("textToSpeech")
);

// Info displays
const aiModelInfo = computed(() => {
	const model = textGenSettings.value.options.model;
	return `Model: ${model}`;
});

const sttInfo = computed(() => {
	return `STT: ${sttSettings.value.provider}`;
});

const ttsInfo = computed(() => {
	return `TTS: ${ttsSettings.value.provider} (${ttsSettings.value.options.voice})`;
});

// State
const messages = computed(() => messagesStore.messages);
const isTyping = ref(false);
const chatContainer = ref(null);
const isSettingsOpen = ref(false);

const lastBotMessage = computed(() => {
	const botMessages = messages.value.filter((msg) => msg.role === "assistant");
	return botMessages.length > 0
		? botMessages[botMessages.length - 1].content
		: "";
});

// Message handling

const sendMessage = async (message) => {
	if (isTyping.value) return;

	try {
		// Add user message
		messagesStore.addMessage({
			role: "user",
			content: message,
		});

		isTyping.value = true;
		tokensStore.clearTokens();
		scrollToBottom();

		// Generate bot response and ensure it's properly streamed
		const stream = await aiService.generateText(message);
		let botResponse = "";

		// Create initial bot message
		const botMessageId = messagesStore.addBotMessage();

		// Process the stream and update message content
		for await (const chunk of stream) {
			// Add chunk to tokens store
			tokensStore.addToken(chunk);

			// Accumulate response
			botResponse += chunk;

			// Update bot message with current accumulated response
			messagesStore.updateMessage(botMessageId, botResponse);

			// Ensure UI updates
			await nextTick();
			scrollToBottom();
		}

		// Verify final message is set
		if (!botResponse) {
			console.warn("Empty bot response received");
			messagesStore.updateMessage(
				botMessageId,
				"I apologize, but I encountered an issue generating a response."
			);
		}

		// TODO: DEBUG
		// Add these in the sendMessage function
		console.log("User message:", message);
		console.log("Bot message ID:", botMessageId);
		console.log("Final bot response:", botResponse);
	} catch (error) {
		console.error("Error in message handling:", error);
		messagesStore.addMessage({
			role: "assistant",
			content: "I apologize, but I encountered an error. Please try again.",
		});
	} finally {
		isTyping.value = false;
		scrollToBottom();
	}
};

// UI handlers
const handleFullscreenToggle = (isFull) => {
	emit("toggle-fullscreen", isFull);
};

const toggleDarkMode = () => {
	userPreferencesStore.toggleDarkMode();
};

const scrollToBottom = () => {
	nextTick(() => {
		if (chatContainer.value) {
			chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
		}
	});
};

const clearChat = () => {
	messagesStore.clearMessages();
	tokensStore.clearTokens();
};

const closeChat = () => {
	emit("close-chat");
};

const exportChat = () => {
	const chatContent = messages.value
		.map((msg) => `${msg.role}: ${msg.content}`)
		.join("\n\n");
	const blob = new Blob([chatContent], { type: "text/plain" });
	const url = URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = url;
	a.download = "chat_export.txt";
	a.click();
	URL.revokeObjectURL(url);
};

const openSettings = () => {
	isSettingsOpen.value = true;
};

const closeSettings = () => {
	isSettingsOpen.value = false;
};

// Lifecycle
onMounted(() => {
	scrollToBottom();
});

watch(
	() => props.isFullScreen,
	(newValue) => {
		if (newValue) {
			document.body.style.overflow = "hidden";
		} else {
			document.body.style.overflow = "";
		}
	}
);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
	transition: all 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
	transform: translateY(20px);
}

@keyframes pulse {
	0%,
	100% {
		transform: scale(1);
	}
	50% {
		transform: scale(1.05);
	}
}

.pulse {
	animation: pulse 2s infinite;
}

.cyber-text {
	color: #dcf9ff;
	text-shadow: 0 0 5px #00fff2, 0 0 10px #00fff2, 0 0 20px #00fff2,
		0 0 40px #00fff2, 0 0 80px #00fff2;
}

.backdrop-blur-md {
	backdrop-filter: blur(12px);
}

.backdrop-blur-sm {
	backdrop-filter: blur(4px);
}

.overflow-y-auto {
	scrollbar-width: thin;
	scrollbar-color: rgba(74, 144, 226, 0.5) rgba(0, 0, 0, 0.1);
}

.overflow-y-auto::-webkit-scrollbar {
	width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
	background: rgba(0, 0, 0, 0.1);
}

.overflow-y-auto::-webkit-scrollbar-thumb {
	background-color: rgba(74, 144, 226, 0.5);
	border-radius: 3px;
}
</style>
