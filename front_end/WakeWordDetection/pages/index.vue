<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">
          Wake Word Detection System
        </h1>
        <div class="flex space-x-4">
          <StatusBadge
            :status="store.systemStatus.status"
            label="System Status"
            type="string"
          />
          <StatusBadge
            :status="store.isConnected"
            label="WebSocket"
            type="boolean"
          />
          <StatusBadge
            :status="store.isRecording"
            label="Recording"
            type="boolean"
          />
        </div>
      </div>


      <!-- Main Content -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Audio Controls -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">Audio Controls</h2>
          <div class="flex items-center justify-center space-x-4">
            <button
              @click="handleRecording"
              class="px-4 py-2 rounded-md"
              :class="store.isRecording ? 'bg-red-500 text-white' : 'bg-green-500 text-white'"
            >
              {{ store.isRecording ? 'Stop Recording' : 'Start Recording' }}
            </button>
          </div>
          <AudioVisualizer v-if="store.isRecording" />
        </div>

        <!-- Wake Word Status -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">Wake Word Status</h2>
          <div
            class="flex items-center justify-center h-32 rounded-lg"
            :class="store.isWakeWordDetected ? 'bg-green-100' : 'bg-gray-100'"
          >
            <span class="text-2xl">
              {{ store.isWakeWordDetected ? '👋 Xin chào!' : '😴 Waiting...' }}
            </span>
          </div>
        </div>

        <!-- Event History -->
        <div class="bg-white rounded-lg shadow p-6 col-span-full">
          <h2 class="text-xl font-semibold mb-4">Event History</h2>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Time
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Event
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Confidence
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="event in store.events" :key="event.timestamp">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ new Date(event.timestamp).toLocaleString() }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ event.event }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ (event.confidence * 100).toFixed(2) }}%
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useWakeWordStore } from '~/stores/wakeWord'

const store = useWakeWordStore()

// Initialize WebSocket connection
const initWebSocket = () => {
  const ws = new WebSocket(`${useRuntimeConfig().public.wsBaseUrl}/ws`)
  
  ws.onopen = () => {
    store.isConnected = true
  }
  
  ws.onclose = () => {
    store.isConnected = false
    setTimeout(initWebSocket, 1000) // Reconnect after 1 second
  }
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.event === 'wake_word') {
      store.handleWakeWordDetection(data)
    }
  }
}

// Handle recording toggle
const handleRecording = async () => {
  if (store.isRecording) {
    store.stopRecording()
  } else {
    try {
      await store.startRecording()
    } catch (error) {
      console.error('Failed to start recording:', error)
    }
  }
}

// Setup on page load
// Initialize WebSocket and status updates
onMounted(() => {
  store.connectWebSocket()
  
  // Update system status every 5 seconds
  const statusInterval = setInterval(() => {
    store.updateSystemStatus()
  }, 5000)

  // Cleanup on unmount
  onUnmounted(() => {
    clearInterval(statusInterval)
    store.stopRecording()
  })
})
</script>