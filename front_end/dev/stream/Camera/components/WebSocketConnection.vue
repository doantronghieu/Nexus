<template>
  <BaseWebSocketConnection
    connection-type="WebSocket"
    :is-connected="webSocketStore.isConnected"
    :display-name="webSocketStore.displayName"
    :error="webSocketStore.error"
    :predefined-names="predefinedNames"
    :is-loading="isConnecting"
    @connect="handleConnect"
    @disconnect="handleDisconnect"
    @reset-error="webSocketStore.resetError"
    ref="baseConnection"
  >
    <!-- Connected Content -->
    <template #connected-content>
      <!-- Message Input -->
      <div class="flex flex-col sm:flex-row gap-2">
        <input
          v-model="currentMessage"
          type="text"
          placeholder="Type a message..."
          class="flex-1 min-h-[44px] px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          @keyup.enter="handleSendMessage"
        />
        <button
          @click="handleSendMessage"
          class="w-full sm:w-auto min-h-[44px] px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!currentMessage.trim()"
        >
          Send
        </button>
      </div>

      <!-- Messages Section -->
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-700">Messages</h3>
          <button
            @click="clearMessages"
            class="px-3 py-1 text-sm text-gray-500 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-300 rounded"
          >
            Clear
          </button>
        </div>
        
        <div class="border rounded-lg h-48 overflow-y-auto bg-gray-50 p-4">
          <div v-if="messages.length > 0" class="space-y-2">
            <div 
              v-for="(msg, index) in messages" 
              :key="index" 
              class="text-sm text-gray-700 break-words"
            >
              {{ msg }}
            </div>
          </div>
          <div v-else class="h-full flex items-center justify-center text-gray-400 text-sm">
            No messages yet
          </div>
        </div>
      </div>
    </template>
  </BaseWebSocketConnection>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useWebSocketStore } from '@/stores/websocket'
import BaseWebSocketConnection from '@/components/base/BaseWebSocketConnection.vue'

const webSocketStore = useWebSocketStore()
const { messages } = storeToRefs(webSocketStore)

const currentMessage = ref('')
const isConnecting = ref(false)
const baseConnection = ref()

const predefinedNames = [
  'Observer_1',
  'Observer_2',
  'Guest_A',
  'Guest_B',
  'Viewer_X',
  'Viewer_Y',
  'User_Alpha',
  'User_Beta'
]

const handleConnect = async (nameToUse?: string) => {
  isConnecting.value = true
  try {
    await webSocketStore.connect(nameToUse)
  } finally {
    isConnecting.value = false
  }
}

const handleDisconnect = () => {
  webSocketStore.disconnect()
}

const handleSendMessage = () => {
  if (currentMessage.value.trim()) {
    webSocketStore.sendMessage(currentMessage.value)
    currentMessage.value = ''
  }
}

const clearMessages = () => {
  webSocketStore.clearMessages()
}

// Method to programmatically connect
const connect = async () => {
  if (!webSocketStore.isConnected) {
    await handleConnect()
  }
  return webSocketStore.isConnected
}

// Expose methods for parent components
defineExpose({
  connect,
  disconnect: handleDisconnect,
  isConnected: () => webSocketStore.isConnected
})
</script>

<style scoped>
/* Custom scrollbar for messages */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}
</style>