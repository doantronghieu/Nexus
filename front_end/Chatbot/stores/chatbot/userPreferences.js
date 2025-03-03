import { defineStore } from "pinia";
import { AI_PROVIDERS, getDefaultProviderOptions } from "~/configs/aiProviders";

export const useUserPreferencesStore = defineStore("userPreferences", {
	state: () => ({
		theme: "dark",
		voiceEnabled: false,
		selectedVoice: "default",
		aiSettings: {
			speechToText: {
				provider: AI_PROVIDERS.speechToText.providers[0].id,
				options: getDefaultProviderOptions(
					"speechToText",
					AI_PROVIDERS.speechToText.providers[0].id
				),
			},
			textToSpeech: {
				provider: AI_PROVIDERS.textToSpeech.providers[0].id,
				options: getDefaultProviderOptions(
					"textToSpeech",
					AI_PROVIDERS.textToSpeech.providers[0].id
				),
			},
			textGeneration: {
				provider: AI_PROVIDERS.textGeneration.providers[0].id,
				options: getDefaultProviderOptions(
					"textGeneration",
					AI_PROVIDERS.textGeneration.providers[0].id
				),
			},
		},
	}),
	actions: {
		toggleDarkMode() {
			this.theme = this.theme === "dark" ? "light" : "dark";
		},
		toggleVoice() {
			this.voiceEnabled = !this.voiceEnabled;
		},
		setSelectedVoice(voice) {
			this.selectedVoice = voice;
		},
		updateAIProvider(service, providerId) {
			if (this.aiSettings[service]) {
				this.aiSettings[service].provider = providerId;
				// Reset options to default when changing provider
				this.aiSettings[service].options = getDefaultProviderOptions(
					service,
					providerId
				);
			}
		},
		updateAIOptions(service, options) {
			if (this.aiSettings[service]) {
				this.aiSettings[service].options = {
					...this.aiSettings[service].options,
					...options,
				};
			}
		},
	},
	getters: {
		isDarkMode: (state) => state.theme === "dark",
		getAISettings: (state) => (service) => state.aiSettings[service],
		getAllAISettings: (state) => state.aiSettings,
	},
});
