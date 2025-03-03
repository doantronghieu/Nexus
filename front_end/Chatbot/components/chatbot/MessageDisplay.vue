<template>
	<div class="space-y-4">
		<div
			v-for="(message, index) in messages"
			:key="message.id || index"
			:class="[
				'p-3 rounded-lg max-w-3/4 animate-fade-in holographic',
				message.role === 'user'
					? 'ml-auto bg-gradient-to-r from-blue-600 to-indigo-600 text-white'
					: 'mr-auto bg-gradient-to-r from-gray-700 to-gray-800 text-white',
			]"
		>
			<div v-if="message.role === 'assistant'" class="flex items-center mb-2">
				<AIAvatar class="w-8 h-8 mr-2 animate-pulse" />
				<span class="font-semibold text-blue-300">IVyEdge</span>
			</div>
			<div v-else class="flex items-center mb-2 justify-end">
				<span class="font-semibold text-blue-300">You</span>
				<UserAvatar class="w-8 h-8 ml-2 animate-pulse" />
			</div>
			<div
				v-html="markdownToHtml(message.content)"
				class="text-sm leading-relaxed"
			></div>
			<FeedbackSystem
				v-if="message.role === 'assistant'"
				:message-id="index"
				class="mt-2"
			/>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";
import FeedbackSystem from "./FeedbackSystem.vue";
import AIAvatar from "./AIAvatar.vue";
import UserAvatar from "./UserAvatar.vue";

const props = defineProps({
	messages: {
		type: Array,
		required: true,
	},
});

const markdownToHtml = (content) => {
	const rawHtml = marked(content);
	return DOMPurify.sanitize(rawHtml);
};
</script>

<style scoped>
.holographic {
	position: relative;
	overflow: hidden;
	box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}
.holographic::before {
	content: "";
	position: absolute;
	top: -50%;
	left: -50%;
	width: 200%;
	height: 200%;
	background: linear-gradient(
		to bottom right,
		rgba(255, 255, 255, 0) 0%,
		rgba(255, 255, 255, 0.1) 50%,
		rgba(255, 255, 255, 0) 100%
	);
	transform: rotate(30deg);
	animation: holographic 3s linear infinite;
}
@keyframes holographic {
	0% {
		transform: rotate(30deg) translate(-50%, -50%);
	}
	100% {
		transform: rotate(30deg) translate(50%, 50%);
	}
}
.animate-fade-in {
	animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(10px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

.animate-pulse {
	animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
	0%,
	100% {
		opacity: 1;
	}
	50% {
		opacity: 0.5;
	}
}
</style>
