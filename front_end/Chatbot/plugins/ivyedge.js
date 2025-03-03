export default defineNuxtPlugin((nuxtApp) => {
	const config = useRuntimeConfig();
	const PORT = parseInt(config.public.PORT_FAST_API) || 8765;
	const BASE_URL = `http://localhost:${PORT}`;
	const BASE_URL_RIVA = `http://localhost:${8771}`;

	const getEndpointUrl = (endpoint, query) => {
		switch (endpoint) {
			case "query":
				return `${BASE_URL}/query/?query=${encodeURIComponent(query)}`;
			case "control":
				return `${BASE_URL}/control/?query=${encodeURIComponent(query)}`;
			case "general":
				return `${BASE_URL}/general/?query=${encodeURIComponent(query)}`;
			case "workflow":
				return `${BASE_URL}/run_workflow/?query=${encodeURIComponent(query)}`;
			default:
				return `${BASE_URL}/query/?query=${encodeURIComponent(query)}`;
		}
	};

	return {
		provide: {
			ivyedge: {
				async *generateText(prompt, options = {}) {
					try {
						const endpoint = options.endpoint || "query";
						const url = getEndpointUrl(endpoint, prompt);

						let response;
						if (endpoint === "workflow") {
							// Handle workflow endpoint differently as it's not streaming
							response = await fetch(url, {
								method: "POST",
								headers: {
									"Content-Type": "application/json",
								},
								body: JSON.stringify({ user_query: prompt }),
							});

							if (!response.ok) {
								throw new Error(`HTTP error! status: ${response.status}`);
							}

							const data = await response.json();
							yield data.result;
							return;
						}

						// Handle streaming endpoints
						response = await fetch(url, {
							method: endpoint === "workflow" ? "POST" : "GET",
						});

						if (!response.ok) {
							throw new Error(`HTTP error! status: ${response.status}`);
						}

						const reader = response.body.getReader();
						const decoder = new TextDecoder("utf-8");

						while (true) {
							const { done, value } = await reader.read();
							if (done) break;

							const chunk = decoder.decode(value);
							yield chunk;
						}
					} catch (error) {
						console.error("Error generating text:", error);
						throw error;
					}
				},

				async transcribeAudio(audioFile) {
					try {
						const formData = new FormData();
						formData.append("file", audioFile);

						const response = await fetch(`${BASE_URL_RIVA}/transcribe/`, {
							// BASE_URL_RIVA | BASE_URL
							method: "POST",
							body: formData,
						});

						if (!response.ok) {
							throw new Error(`HTTP error! status: ${response.status}`);
						}

						const data = await response.json();
						return data.transcribed_text;
					} catch (error) {
						console.error("Error transcribing audio:", error);
						throw error;
					}
				},

				async textToSpeech(text) {
					try {
						const formData = new FormData();
						formData.append("text", text);

						const response = await fetch(`${BASE_URL}/text_to_speech/`, {
							method: "POST",
							body: formData,
						});

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
							URL.createObjectURL(new Blob([audioData], { type: "audio/wav" }))
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
