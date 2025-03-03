<template>
  <BaseWebSocketConnection
    connection-type="ML Server"
    :is-connected="mlStore.isConnected"
    :display-name="mlStore.clientName"
    :error="mlStore.error"
    :is-loading="isConnecting"
    @connect="handleConnect"
    @disconnect="handleDisconnect"
    @reset-error="mlStore.resetError"
    ref="baseConnection"
  >
    <!-- Connected Content -->
    <template #connected-content>
      <div class="space-y-4">
        <!-- Server Connection Test -->
        <button
          @click="testServerConnection"
          :disabled="mlStore.isServerConnected"
          class="w-full min-h-[44px] px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm font-medium transition-colors disabled:opacity-50"
        >
          {{ mlStore.isServerConnected ? 'Server Connected' : 'Test Server Connection' }}
        </button>

        <!-- Server Connection Status -->
        <div 
          v-if="mlStore.isServerConnected"
          class="p-3 bg-purple-50 border border-purple-100 rounded-lg"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-purple-500"></div>
              <span class="text-purple-700">Server Connected</span>
            </div>
            <button
              @click="disconnectServer"
              class="px-2 py-1 text-sm text-purple-600 hover:text-purple-800"
            >
              Disconnect
            </button>
          </div>
        </div>
      </div>
    </template>
  </BaseWebSocketConnection>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMLStore } from '@/stores/ml'
import BaseWebSocketConnection from '@/components/base/BaseWebSocketConnection.vue'

const mlStore = useMLStore()
const isConnecting = ref(false)
const baseConnection = ref()

const handleConnect = async (nameToUse?: string) => {
  isConnecting.value = true
  try {
    await mlStore.connect(nameToUse)
  } finally {
    isConnecting.value = false
  }
}

const handleDisconnect = () => {
  mlStore.disconnect()
}

const testServerConnection = async () => {
  if (!mlStore.isServerConnected) {
    await mlStore.connectServer()
  }
}

const disconnectServer = () => {
  mlStore.disconnectServer()
}

// Method to programmatically connect both client and server
const connect = async () => {
  let success = false
  try {
    // Connect client first
    if (!mlStore.isConnected) {
      await handleConnect()
    }
    // Then connect server
    if (!mlStore.isServerConnected) {
      await mlStore.connectServer()
    }
    success = mlStore.isConnected && mlStore.isServerConnected
  } catch (error) {
    console.error('Error connecting ML WebSocket:', error)
  }
  return success
}

// Expose methods for parent components
defineExpose({
  connect,
  disconnect: handleDisconnect,
  isConnected: () => mlStore.isConnected && mlStore.isServerConnected
})
</script>