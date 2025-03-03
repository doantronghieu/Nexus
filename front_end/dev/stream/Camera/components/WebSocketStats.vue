<template>
  <BaseWebSocketStats
    title="WebSocket Statistics"
    :stats="statsStore.stats"
    :error="statsStore.error"
    :is-loading="statsStore.isLoading"
    :is-polling="statsStore.isPolling"
    :is-configured="serverStore.isConfigured"
    :client-table-headers="clientTableHeaders"
    v-model:is-polling="statsStore.isPolling"
    :start-polling="statsStore.startPolling"
    :stop-polling="statsStore.stopPolling"
  >
    <template #client-id="{ client }">
      <div class="font-medium text-gray-900 truncate max-w-[120px] sm:max-w-none">
        {{ client.id }}
      </div>
    </template>

    <template #client-connected_for="{ client, formatDuration }">
      <span class="whitespace-nowrap text-gray-500">
        {{ formatDuration(client.connected_for) }}
      </span>
    </template>

    <template #client-message_count="{ client }">
      <span class="whitespace-nowrap text-gray-500">
        {{ client.message_count }}
      </span>
    </template>
  </BaseWebSocketStats>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useServerStore } from '@/stores/server'
import { useWebSocketStatsStore } from '@/stores/websocketStats'
import BaseWebSocketStats from '@/components/base/BaseWebSocketStats.vue'

const serverStore = useServerStore()
const statsStore = useWebSocketStatsStore()

const clientTableHeaders = [
  {
    key: 'id',
    label: 'Client ID',
    class: 'whitespace-nowrap'
  },
  {
    key: 'connected_for',
    label: 'Connected For',
    class: 'whitespace-nowrap'
  },
  {
    key: 'message_count',
    label: 'Messages',
    class: 'whitespace-nowrap'
  }
]

// Method to programmatically start auto-refresh
const startAutoRefresh = async () => {
  try {
    if (!statsStore.isPolling && serverStore.isConfigured) {
      await statsStore.startPolling()
      return true
    }
  } catch (error) {
    console.error('Failed to start auto-refresh:', error)
  }
  return false
}

// Method to programmatically stop auto-refresh
const stopAutoRefresh = () => {
  if (statsStore.isPolling) {
    statsStore.stopPolling()
  }
}

// Clean up on unmount
onUnmounted(() => {
  // Only stop the actual polling interval, don't change the isPolling state
  if (statsStore.isPolling) {
    statsStore.stopPolling()
    statsStore.isPolling = true // Keep the state as polling
  }
})

// Expose control methods for parent component
defineExpose({
  startAutoRefresh,
  stopAutoRefresh,
  isPolling: computed(() => statsStore.isPolling)
})
</script>
