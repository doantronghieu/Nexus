<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">AI Chatbot</h1>
      </div>
    </header>
    <main class="flex-grow relative">
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <p class="mb-4">Welcome to the AI Chatbot. Click the chat icon to start a conversation!</p>
        </div>
      </div>
      <ChatWindow 
        :is-full-screen="isFullScreen"
        @toggle-fullscreen="toggleFullScreen"
        @close-fullscreen="closeFullScreen"
        @close-chat="closeChat"
        v-if="isChatOpen"
      />
      <ChatbotIcon v-else @toggle-chat="openChat" />
    </main>
    <footer class="bg-white">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-gray-500 text-sm">© 2023 AI Chatbot. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChatbotIcon from '~/components/chatbot/ChatbotIcon.vue'
import ChatWindow from '~/components/chatbot/ChatWindow.vue'

const isChatOpen = ref(true) // Changed to true by default
const isFullScreen = ref(true) // Changed to true by default

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value
}

const openChat = () => {
  isChatOpen.value = true
  isFullScreen.value = true // Set full screen when opening chat
}

const closeChat = () => {
  isChatOpen.value = false
  isFullScreen.value = false
}

const toggleFullScreen = () => {
  isFullScreen.value = !isFullScreen.value
}

const closeFullScreen = () => {
  isFullScreen.value = false
}

// Add onMounted to ensure the chat opens in full screen on page load
onMounted(() => {
  isChatOpen.value = true
  isFullScreen.value = true
})
</script>