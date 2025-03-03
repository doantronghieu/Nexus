// Base configuration for AI providers and their available options
export const AI_PROVIDERS = {
	speechToText: {
		providers: [
			{
				id: "openai-whisper",
				name: "OpenAI Whisper",
				options: {}, // Currently no configurable options for Whisper
			},
			{
				id: "ivyedge-stt",
				name: "IvyEdge STT",
				options: {},
			},
			// Add more STT providers here
		],
	},
	textToSpeech: {
		providers: [
			{
				id: "openai-tts",
				name: "OpenAI TTS",
				options: {
					voice: {
						type: "select",
						label: "Voice",
						default: "alloy",
						choices: [
							{ value: "alloy", label: "Alloy" },
							{ value: "echo", label: "Echo" },
							{ value: "fable", label: "Fable" },
							{ value: "onyx", label: "Onyx" },
							{ value: "nova", label: "Nova" },
							{ value: "shimmer", label: "Shimmer" },
						],
					},
				},
			},
			{
				id: "ivyedge-tts",
				name: "IvyEdge TTS",
				options: {},
			},
			// Add more TTS providers here
		],
	},
	textGeneration: {
		providers: [
			{
				id: "openai-gpt",
				name: "OpenAI GPT",
				options: {
					model: {
						type: "select",
						label: "Model",
						default: "gpt-3.5-turbo",
						choices: [
							{ value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
							{ value: "gpt-4", label: "GPT-4" },
						],
					},
					temperature: {
						type: "range",
						label: "Temperature",
						default: 0.7,
						min: 0,
						max: 2,
						step: 0.1,
					},
					maxTokens: {
						type: "number",
						label: "Max Tokens",
						default: 2000,
						min: 1,
						max: 4000,
					},
				},
			},
			{
				id: "ivyedge-llm",
				name: "IvyEdge LLM",
				options: {
					endpoint: {
						type: "select",
						label: "Endpoint",
						default: "query",
						choices: [
							{ value: "query", label: "General Query" },
							{ value: "control", label: "Car Control" },
							{ value: "general", label: "Car General" },
							{ value: "workflow", label: "Workflow" },
						],
					},
				},
			},
			// Add more text generation providers here
		],
	},
};

// Helper functions for providers
export const getProviderConfig = (serviceType, providerId) => {
	const service = AI_PROVIDERS[serviceType];
	if (!service) return null;

	return service.providers.find((provider) => provider.id === providerId);
};

export const getDefaultProviderOptions = (serviceType, providerId) => {
	const provider = getProviderConfig(serviceType, providerId);
	if (!provider) return {};

	const defaultOptions = {};
	Object.entries(provider.options).forEach(([key, config]) => {
		defaultOptions[key] = config.default;
	});
	return defaultOptions;
};
