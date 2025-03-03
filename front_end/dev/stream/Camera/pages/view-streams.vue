<template>
  <BaseStreamViewer
    title="Active Streams"
    :showHeader="false"
    :activeStreams="streamsStore.clientsList"
    :streamingClientsCount="streamsStore.streamingClientsCount"
    :isConnected="webSocketStore.isConnected"
    :connectionStatus="connectionStatus"
    :getStreamDuration="streamsStore.getStreamDuration"
    noStreamsMessage="Start streaming from the Camera Stream page to see streams here"
    streamPageLink="/camera-stream"
    streamPageText="Go to Camera Stream"
    @retryStream="handleRetryStream"
    @streamError="handleStreamError"
    ref="streamViewer"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { useStreamsStore } from '@/stores/streams'
import { useWebSocketStore } from '@/stores/websocket'
import BaseStreamViewer from '@/components/base/BaseStreamViewer.vue'

// Store instantiation
const streamsStore = useStreamsStore()
const webSocketStore = useWebSocketStore()

// Refs
const streamViewer = ref()

// Computed
const connectionStatus = computed(() => {
  if (webSocketStore.isConnected) {
    return `Connected as ${webSocketStore.displayName}`
  }
  return webSocketStore.isReconnecting ? 'Reconnecting...' : 'Disconnected'
})

// Methods
const handleRetryStream = (clientId: string) => {
  // Request updated metrics for the client
  if (webSocketStore.isConnected) {
    webSocketStore.sendMessage({
      type: 'metrics_request',
      client_id: clientId
    })
  }
}

const handleStreamError = (clientId: string) => {
  console.error(`Stream error for client ${clientId}`)
}

// If page is loaded without server configuration, redirect to setup
onMounted(() => {
  const serverStore = useServerStore()
  if (!serverStore.isConfigured) {
    const router = useRouter()
    router.push('/server-setup')
  }
})

// Watch for route changes to handle cleanup
const router = useRouter()
const route = useRoute()

watch(
  () => route.path,
  (newPath) => {
    if (newPath !== '/view-streams' && streamViewer.value) {
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
