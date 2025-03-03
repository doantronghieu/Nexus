import { useUserPreferencesStore } from "~/stores/chatbot/userPreferences";

export class AIServiceHandler {
	constructor(nuxtApp) {
		this.nuxtApp = nuxtApp;
		this.userPreferencesStore = useUserPreferencesStore();
	}

	async *generateText(message) {
		const settings = this.userPreferencesStore.getAISettings("textGeneration");

		try {
			let stream;
			switch (settings.provider) {
				case "openai-gpt":
					stream = this.nuxtApp.$openai.generateText(message);
					break;
				case "ivyedge-llm":
					stream = this.nuxtApp.$ivyedge.generateText(message, {
						endpoint: settings.options.endpoint || "query",
					});
					break;
				default:
					throw new Error(
						`Unsupported text generation provider: ${settings.provider}`
					);
			}

			// Process the stream and ensure chunks are properly yielded
			for await (const chunk of stream) {
				if (chunk && typeof chunk === "string" && chunk.trim()) {
					yield chunk;
				}
			}
		} catch (error) {
			console.error("Error in AI service text generation:", error);
			throw error;
		}
	}

	async textToSpeech(text) {
		const settings = this.userPreferencesStore.getAISettings("textToSpeech");

		switch (settings.provider) {
			case "openai-tts":
				return await this.nuxtApp.$openai.textToSpeech(text);
			case "ivyedge-tts":
				return await this.nuxtApp.$ivyedge.textToSpeech(text);
			// Add more providers here
			default:
				throw new Error(
					`Unsupported text-to-speech provider: ${settings.provider}`
				);
		}
	}

	async transcribeAudio(audioBlob) {
		const settings = this.userPreferencesStore.getAISettings("speechToText");

		switch (settings.provider) {
			case "openai-whisper":
				return await this.nuxtApp.$openai.transcribeAudio(audioBlob);
			case "ivyedge-stt":
				return await this.nuxtApp.$ivyedge.transcribeAudio(audioBlob);
			// Add more providers here
			default:
				throw new Error(
					`Unsupported speech-to-text provider: ${settings.provider}`
				);
		}
	}

	async getAudioDuration(audioData) {
		const settings = this.userPreferencesStore.getAISettings("textToSpeech");

		switch (settings.provider) {
			case "openai-tts":
				return await this.nuxtApp.$openai.getAudioDuration(audioData);
			case "ivyedge-tts":
				return await this.nuxtApp.$ivyedge.getAudioDuration(audioData);
			default:
				return await this.nuxtApp.$openai.getAudioDuration(audioData); // fallback
		}
	}
}

export function useAIService() {
	const nuxtApp = useNuxtApp();
	return new AIServiceHandler(nuxtApp);
}
