import { defineStore } from "pinia";

export const useTokensStore = defineStore("tokens", {
	state: () => ({
		currentTokens: "",
		audioQueue: [],
		isProcessing: false,
		textAccumulator: "",
		nextChunkId: 0,
		currentAudioId: 0,
	}),
	actions: {
		addToken(token) {
			this.currentTokens += token;
			this.textAccumulator += token;
		},
		clearTokens() {
			this.currentTokens = "";
			this.textAccumulator = "";
			this.audioQueue = [];
			this.isProcessing = false;
			this.nextChunkId = 0;
			this.currentAudioId = 0;
		},
		async addToAudioQueue(text) {
			const chunkId = this.nextChunkId++;
			this.audioQueue.push({
				id: chunkId,
				text,
				status: "pending",
				audio: null,
				duration: 0,
			});
			return chunkId;
		},
		updateAudioChunk(id, audio, duration) {
			const chunk = this.audioQueue.find((chunk) => chunk.id === id);
			if (chunk) {
				chunk.audio = audio;
				chunk.duration = duration;
				chunk.status = "ready";
			}
		},
		removeFromQueue(id) {
			const index = this.audioQueue.findIndex((chunk) => chunk.id === id);
			if (index !== -1) {
				// Clean up audio resources before removing
				const chunk = this.audioQueue[index];
				if (chunk.audio) {
					URL.revokeObjectURL(chunk.audio.src);
				}
				this.audioQueue.splice(index, 1);
			}
		},
		setProcessing(status) {
			this.isProcessing = status;
		},
		clearTextAccumulator() {
			this.textAccumulator = "";
		},
	},
	getters: {
		nextAudioChunk: (state) => {
			return state.audioQueue.find(
				(chunk) => chunk.status === "ready" && chunk.id === state.currentAudioId
			);
		},
		hasNextChunk: (state) => {
			return state.audioQueue.some(
				(chunk) => chunk.status === "ready" && chunk.id === state.currentAudioId
			);
		},
	},
});
