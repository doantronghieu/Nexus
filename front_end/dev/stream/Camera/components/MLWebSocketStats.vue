<template>
  <BaseWebSocketStats
    title="ML Server Statistics"
    :stats="mlStore.stats"
    :error="mlStore.error"
    :is-loading="isLoading"
    :is-polling="isPolling"
    :is-configured="serverStore.isConfigured"
    :primary-stat-label="'ML Connections'"
    :client-table-headers="clientTableHeaders"
    v-model:is-polling="isPolling"
    :start-polling="startPolling"
    :stop-polling="stopPolling"
  >
    <!-- Server Status Stats -->
    <template #custom-stats="{ stats, formatDuration }">
      <div v-if="stats" class="grid grid-cols-1 gap-4">
        <!-- Status Cards -->
        <div class="p-4 bg-indigo-50 rounded-lg border border-indigo-100">
          <div class="flex flex-col space-y-2">
            <!-- Server Processing Status -->
            <div class="flex items-center justify-between">
              <span class="text-sm text-indigo-600 font-medium">ML Server Status</span>
              <div class="flex items-center gap-2">
                <div 
                  class="w-2 h-2 rounded-full"
                  :class="stats.server_connected ? 'bg-green-500' : 'bg-red-500'"
                ></div>
                <span class="text-sm" :class="stats.server_connected ? 'text-green-600' : 'text-red-600'">
                  {{ stats.server_connected ? 'Connected' : 'Disconnected' }}
                </span>
              </div>
            </div>

            <!-- Processing Statistics -->
            <div class="grid grid-cols-2 gap-4 mt-2">
              <div class="space-y-1">
                <div class="text-xs text-indigo-500">Total ML Clients</div>
                <div class="text-lg font-semibold text-indigo-700">
                  {{ stats.clients.length }}
                </div>
              </div>
              <div class="space-y-1">
                <div class="text-xs text-indigo-500">Total Frames Processed</div>
                <div class="text-lg font-semibold text-indigo-700">
                  {{ calculateTotalProcessedFrames(stats) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="p-4 bg-gray-50 rounded-lg border border-gray-100">
            <div class="text-sm text-gray-600 font-medium mb-1">Average Processing Rate</div>
            <div class="text-lg font-semibold text-gray-700">
              {{ calculateAverageProcessingRate(stats) }} frames/min
            </div>
          </div>
          <div class="p-4 bg-gray-50 rounded-lg border border-gray-100">
            <div class="text-sm text-gray-600 font-medium mb-1">Peak Performance</div>
            <div class="text-lg font-semibold text-gray-700">
              {{ findPeakProcessingRate(stats) }} frames/min
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Client Table Cell Templates -->
    <template #client-id="{ client }">
      <div class="flex items-center gap-2">
        <div class="font-medium text-gray-900 truncate max-w-[120px] sm:max-w-none">
          {{ client.info.name }}
        </div>
        <span 
          v-if="client.info.is_server" 
          class="px-1.5 py-0.5 text-xs font-medium bg-purple-100 text-purple-700 rounded-full"
        >
          Server
        </span>
      </div>
    </template>

    <template #client-connected_for="{ client, formatDuration }">
      <div class="flex flex-col text-sm">
        <span class="text-gray-900">{{ formatTimestamp(client.info.connected_at) }}</span>
        <span class="text-gray-500 text-xs">
          {{ getTimeSinceConnection(client.info.connected_at) }} ago
        </span>
      </div>
    </template>

    <template #client-stats="{ client }">
      <div class="flex items-center gap-4 text-sm">
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span class="text-gray-600">{{ client.info.processed_frames }}</span>
        </div>
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span class="text-gray-600">{{ calculateProcessingRate(client) }}/min</span>
        </div>
      </div>
    </template>
  </BaseWebSocketStats>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useServerStore } from '@/stores/server'
import { useMLStore } from '@/stores/ml'
import BaseWebSocketStats from '@/components/base/BaseWebSocketStats.vue'

const serverStore = useServerStore()
const mlStore = useMLStore()

const isLoading = ref(false)
const isPolling = ref(false)
let pollInterval: number | null = null

const clientTableHeaders = [
  {
    key: 'id',
    label: 'Client Name',
    class: 'whitespace-nowrap'
  },
  {
    key: 'connected_for',
    label: 'Connected Since',
    class: 'whitespace-nowrap'
  },
  {
    key: 'stats',
    label: 'Processing Stats',
    class: 'whitespace-nowrap'
  }
]

// Helper functions
const calculateTotalProcessedFrames = (stats: any) => {
  if (!stats?.clients) return 0
  return stats.clients.reduce((total: number, client: any) => 
    total + (client.info.processed_frames || 0), 0
  )
}

const calculateProcessingRate = (client: any) => {
  if (!client?.info) return 0
  
  const connectedTime = Date.now() - new Date(client.info.connected_at).getTime()
  const minutesConnected = connectedTime / (1000 * 60)
  
  if (minutesConnected < 1) return client.info.processed_frames
  return Math.round(client.info.processed_frames / minutesConnected)
}

const calculateAverageProcessingRate = (stats: any) => {
  if (!stats?.clients || stats.clients.length === 0) return 0
  
  const rates = stats.clients.map(calculateProcessingRate)
  const total = rates.reduce((sum: number, rate: number) => sum + rate, 0)
  return Math.round(total / rates.length)
}

const findPeakProcessingRate = (stats: any) => {
  if (!stats?.clients || stats.clients.length === 0) return 0
  
  const rates = stats.clients.map(calculateProcessingRate)
  return Math.max(...rates)
}

const formatTimestamp = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTimeSinceConnection = (timestamp: string) => {
  const connectionTime = new Date(timestamp).getTime()
  const now = Date.now()
  const diffMinutes = Math.floor((now - connectionTime) / (1000 * 60))
  
  if (diffMinutes < 1) return 'just now'
  if (diffMinutes < 60) return `${diffMinutes}m`
  
  const hours = Math.floor(diffMinutes / 60)
  const minutes = diffMinutes % 60
  return `${hours}h ${minutes}m`
}

// Auto-refresh methods
const startAutoRefresh = async () => {
  try {
    if (!isPolling.value && serverStore.isConfigured) {
      await fetchStats()
      startPolling()
      return true
    }
  } catch (error) {
    console.error('Failed to start auto-refresh:', error)
  }
  return false
}

const stopAutoRefresh = () => {
  stopPolling()
}

// Polling functions
const fetchStats = async () => {
  isLoading.value = true
  try {
    await mlStore.checkHealth()
  } finally {
    isLoading.value = false
  }
}

const startPolling = (interval = 5000) => {
  stopPolling()
  isPolling.value = true
  pollInterval = window.setInterval(fetchStats, interval)
}

const stopPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
  isPolling.value = false
}

// Clean up on unmount
onUnmounted(() => {
  stopPolling()
})

// Expose methods for parent component
defineExpose({
  startAutoRefresh,
  stopAutoRefresh,
  isPolling: computed(() => isPolling.value)
})
</script>