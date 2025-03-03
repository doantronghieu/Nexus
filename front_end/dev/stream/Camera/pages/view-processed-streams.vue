<template>
  <BaseStreamViewer
    title="Processed Streams"
    :showHeader="false"
    :activeStreams="mlStore.clientsList"
    :streamingClientsCount="mlStore.streamingClientsCount"
    :isConnected="mlStore.isConnected"
    :connectionStatus="connectionStatus"
    :getStreamDuration="mlStore.getStreamDuration"
    noStreamsMessage="Start streaming from the Camera Stream page and enable ML processing to see processed streams here"
    streamPageLink="/camera-stream"
    streamPageText="Go to Camera Stream"
    @retryStream="handleRetryStream"
    @streamError="handleStreamError"
    ref="streamViewer"
  >
    <!-- Extra ML Status Headers -->
    <template #header-extra>
      <div class="flex items-center gap-2 text-sm">
        <span class="text-gray-600 min-w-[100px]">ML Server:</span>
        <div class="flex items-center gap-2">
          <div 
            class="w-2 h-2 rounded-full"
            :class="{
              'bg-green-500': mlStore.isServerConnected,
              'bg-red-500': !mlStore.isServerConnected
            }"
          ></div>
          <span 
            :class="{
              'text-green-700': mlStore.isServerConnected,
              'text-red-700': !mlStore.isServerConnected
            }"
          >
            {{ mlStore.isServerConnected ? 'Connected' : 'Disconnected' }}
          </span>
        </div>
      </div>
    </template>

    <!-- Extra Stream Info -->
    <template #stream-info="{ client }">
      <div class="flex items-center gap-2 text-sm text-white/75">
        <span>Processing: {{ getProcessingRate(client) }} frames/sec</span>
      </div>
    </template>
  </BaseStreamViewer>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { useMLStore } from '@/stores/ml'
import { useServerStore } from '@/stores/server'
import BaseStreamViewer from '@/components/base/BaseStreamViewer.vue'

// Store instantiation
const mlStore = useMLStore()
const serverStore = useServerStore()

// Refs
const streamViewer = ref()

// Computed
const connectionStatus = computed(() => {
  if (mlStore.isConnected) {
    return `Connected as ${mlStore.clientName}`
  }
  return mlStore.isReconnecting ? 'Reconnecting...' : 'Disconnected'
})

// Methods
const getProcessingRate = (client: any) => {
  if (!client.metrics?.startTime) return 0
  const duration = (Date.now() - client.metrics.startTime) / 1000
  return duration > 0 ? (client.metrics.frameCount / duration).toFixed(1) : 0
}

const handleRetryStream = (clientId: string) => {
  // Request updated metrics for the client
  if (mlStore.isConnected) {
    mlStore.socket?.send(JSON.stringify({
      type: 'metrics_request',
      client_id: clientId
    }))
  }
}

const handleStreamError = (clientId: string) => {
  console.error(`Stream error for client ${clientId}`)
}

// Auto-connection
onMounted(async () => {
  if (!serverStore.isConfigured) {
    const router = useRouter()
    router.push('/server-setup')
    return
  }

  if (!mlStore.isConnected) {
    await mlStore.autoConnect()
  }
})

// Watch for route changes to handle cleanup
const router = useRouter()
const route = useRoute()

watch(
  () => route.path,
  (newPath) => {
    if (newPath !== '/view-processed-streams' && streamViewer.value) {
      streamViewer.value.closeStreamModal()
    }
  }
)

// Cleanup
onUnmounted(() => {
  if (streamViewer.value) {
    streamViewer.value.closeStreamModal()
  }
})
</script>

<style scoped>
/* ML-specific animations */
@keyframes processing-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.processing-indicator {
  animation: processing-pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>