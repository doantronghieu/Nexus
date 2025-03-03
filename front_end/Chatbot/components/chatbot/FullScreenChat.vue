<template>
  <div class="fixed inset-0 bg-white z-50 flex flex-col">
    <div class="bg-blue-500 text-white p-4 flex justify-between items-center">
      <h2 class="text-xl font-semibold">AI Chatbot (Full Screen)</h2>
      <button @click="toggleFullScreen" class="text-white hover:text-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    <div class="flex-grow overflow-y-auto p-4" ref="chatContainer">
      <MessageDisplay :messages="messages" />
      <TypingIndicator v-if="isTyping" />
    </div>
    <UndoRedoControls @undo="undo" @redo="redo" />
    <div class="p-4 border-t flex items-center space-x-2">
      <TextInput @send-message="sendMessage" class="flex-grow" />
      <VoiceInput @send-message="sendMessage" />
      <VoiceOutput :text="lastBotMessage" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useMessagesStore } from '~/stores/chatbot/messages'
import { useUserPreferencesStore } from '~/stores/chatbot/userPreferences'
import MessageDisplay from './MessageDisplay.vue'
import TextInput from './TextInput.vue'
import VoiceInput from './VoiceInput.vue'
import VoiceOutput from './VoiceOutput.vue'
import TypingIndicator from './TypingIndicator.vue'
import UndoRedoControls from './UndoRedoControls.vue'

const messagesStore = useMessagesStore()
const userPreferencesStore = useUserPreferencesStore()
const messages = computed(() => messagesStore.messages)
const isTyping = ref(false)
const chatContainer = ref(null)

const { $openai } = useNuxtApp()

const emit = defineEmits(['toggle-fullscreen'])

const lastBotMessage = computed(() => {
  const botMessages = messages.value.filter(msg => msg.role === 'assistant')
  return botMessages.length > 0 ? botMessages[botMessages.length - 1].content : ''
})

const sendMessage = async (message) => {
  // Implementation same as in ChatWindow.vue
}

const toggleFullScreen = () => {
  emit('toggle-fullscreen')
}

const undo = () => {
  messagesStore.undo()
}

const redo = () => {
  messagesStore.redo()
}

const scrollToBottom = () => {
  nextTick(() => {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })
}

onMounted(() => {
  scrollToBottom()
})
</script>