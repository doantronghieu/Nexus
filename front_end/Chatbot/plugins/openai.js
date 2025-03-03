import { useUserPreferencesStore } from "~/stores/chatbot/userPreferences";

export default defineNuxtPlugin((nuxtApp) => {
	const config = useRuntimeConfig();
	const openaiApiKey = config.public.OPENAI_API_KEY;

	// Move store initialization inside the plugin setup
	const initializeStores = () => {
		const userPreferencesStore = useUserPreferencesStore();
		return { userPreferencesStore };
	};

	if (!openaiApiKey) {
		console.error(
			"OpenAI API key is not set. Please check your environment variables."
		);
	}

	return {
		provide: {
			openai: {
				async *generateText(prompt) {
					const { userPreferencesStore } = initializeStores();
					try {
						const textGenSettings =
							userPreferencesStore.getAISettings("textGeneration");
						const response = await fetch(
							"https://api.openai.com/v1/chat/completions",
							{
								method: "POST",
								headers: {
									Authorization: `Bearer ${openaiApiKey}`,
									"Content-Type": "application/json",
								},
								body: JSON.stringify({
									model: textGenSettings.options.model || "gpt-3.5-turbo",
									messages: [{ role: "user", content: prompt }],
									stream: true,
									temperature: textGenSettings.options.temperature || 0.7,
									max_tokens: textGenSettings.options.maxTokens || 2000,
									// Add stop sequences to ensure proper sentence completion
									stop: ["\n\n"],
								}),
							}
						);

						if (!response.ok) {
							throw new Error(`HTTP error! status: ${response.status}`);
						}

						const reader = response.body.getReader();
						const decoder = new TextDecoder("utf-8");
						let buffer = "";

						while (true) {
							const { done, value } = await reader.read();
							if (done) break;

							// Decode the chunk and add it to our buffer
							buffer += decoder.decode(value, { stream: true });

							// Process complete lines from the buffer
							let lineEnd;
							while ((lineEnd = buffer.indexOf("\n")) !== -1) {
								const line = buffer.slice(0, lineEnd);
								buffer = buffer.slice(lineEnd + 1);

								if (line.startsWith("data: ")) {
									const data = line.slice(6);

									if (data === "[DONE]") {
										break;
									}

									try {
										const parsed = JSON.parse(data);
										const content = parsed.choices[0]?.delta?.content;

										if (content) {
											yield content;
										}
									} catch (e) {
										console.warn("Partial or invalid JSON:", e);
										// Continue processing rather than throwing
										continue;
									}
								}
							}
						}

						// Process any remaining content in the buffer
						if (buffer.length > 0 && buffer.startsWith("data: ")) {
							try {
								const data = buffer.slice(6);
								if (data !== "[DONE]") {
									const parsed = JSON.parse(data);
									const content = parsed.choices[0]?.delta?.content;
									if (content) {
										yield content;
									}
								}
							} catch (e) {
								console.warn("Error processing final buffer:", e);
							}
						}
					} catch (error) {
						console.error("Error generating text:", error);
						throw error;
					}
				},

				async transcribeAudio(audioBlob) {
					const { userPreferencesStore } = initializeStores();
					try {
						const sttSettings = userPreferencesStore.getAISettings("speechToText");
						const formData = new FormData();
						
						// Create a proper file from the blob
						const audioFile = new File([audioBlob], 'audio.wav', {
							type: 'audio/wav',
							lastModified: new Date().getTime()
						});
						
						formData.append("file", audioFile);
						formData.append("model", "whisper-1");
						formData.append("language", "en"); // You can make this configurable
						formData.append("response_format", "json");
				
						const response = await fetch(
							"https://api.openai.com/v1/audio/transcriptions",
							{
								method: "POST",
								headers: {
									Authorization: `Bearer ${openaiApiKey}`,
								},
								body: formData,
							}
						);
				
						if (!response.ok) {
							const errorData = await response.json().catch(() => ({}));
							console.error('Transcription error details:', errorData);
							throw new Error(`HTTP error! status: ${response.status}`);
						}
				
						const data = await response.json();
						return data.text;
					} catch (error) {
						console.error("Error transcribing audio:", error);
						throw error;
					}
				},
				
				async textToSpeech(text) {
					const { userPreferencesStore } = initializeStores();
					try {
						const ttsSettings =
							userPreferencesStore.getAISettings("textToSpeech");
						const response = await fetch(
							"https://api.openai.com/v1/audio/speech",
							{
								method: "POST",
								headers: {
									Authorization: `Bearer ${openaiApiKey}`,
									"Content-Type": "application/json",
								},
								body: JSON.stringify({
									model: "tts-1",
									input: text,
									voice: ttsSettings.options.voice || "alloy",
								}),
							}
						);

						if (!response.ok) {
							throw new Error(`HTTP error! status: ${response.status}`);
						}

						const arrayBuffer = await response.arrayBuffer();
						return arrayBuffer;
					} catch (error) {
						console.error("Error converting text to speech:", error);
						throw error;
					}
				},
				async getAudioDuration(audioData) {
					return new Promise((resolve, reject) => {
						const audio = new Audio(
							URL.createObjectURL(new Blob([audioData], { type: "audio/mpeg" }))
						);
						audio.addEventListener("loadedmetadata", () => {
							const duration = audio.duration;
							URL.revokeObjectURL(audio.src);
							resolve(duration);
						});
						audio.addEventListener("error", reject);
					});
				},
			},
		},
	};
});
