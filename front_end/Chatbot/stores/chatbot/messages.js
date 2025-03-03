import { defineStore } from "pinia";

export const useMessagesStore = defineStore("messages", {
	state: () => ({
		messages: [],
		undoStack: [],
		redoStack: [],
		feedback: {},
	}),

	getters: {
		canUndo: (state) => state.undoStack.length > 0,
		canRedo: (state) => state.redoStack.length > 0,
	},

	actions: {
		addMessage(message) {
			const messageWithId = {
				...message,
				id: message.id || Date.now().toString(),
			};
			this.messages.push(messageWithId);
			return messageWithId.id;
		},

		addBotMessage(initialContent = "") {
			const botMessage = {
				id: Date.now().toString(),
				role: "assistant",
				content: initialContent,
			};
			this.messages.push(botMessage);
			return botMessage.id;
		},

		updateMessage(id, content) {
			const message = this.messages.find((msg) => msg.id === id);
			if (message) {
				message.content = content;
			}
		},

		removeMessage(id) {
			const index = this.messages.findIndex((msg) => msg.id === id);
			if (index !== -1) {
				this.messages.splice(index, 1);
			}
		},

		clearMessages() {
			this.messages = [];
		},

		addFeedback(messageId, isPositive) {
			this.feedback[messageId] = isPositive;
		},
	},
});
