<template>
  <!-- Main container with full viewport height minus navigation -->
  <div class="h-[calc(100dvh-6rem)] flex flex-col bg-gray-100">
    <!-- Status header - fixed height -->
    <div class="flex-none bg-white shadow-sm">
      <div class="max-w-7xl mx-auto w-full px-4 py-2">
        <div class="flex flex-col space-y-1">
          <!-- Server Status -->
          <div class="flex items-center gap-2">
            <span class="text-gray-600 min-w-[100px] text-sm">Server:</span>
            <div class="flex items-center gap-2 text-sm">
              <div 
                class="w-2 h-2 rounded-full"
                :class="{
                  'bg-green-500': serverStore.isConfigured,
                  'bg-red-500': !serverStore.isConfigured
                }"
              ></div>
              <span 
                :class="{
                  'text-green-700': serverStore.isConfigured,
                  'text-red-700': !serverStore.isConfigured,
                }"
              >
                {{ serverStore.isConfigured ? serverStore.getHttpUrl : 'Not Connected' }}
              </span>
            </div>
          </div>

          <!-- WebSocket Status -->
          <div class="flex items-center gap-2">
            <span class="text-gray-600 min-w-[100px] text-sm">WebSocket:</span>
            <div class="flex items-center gap-2 text-sm">
              <div 
                class="w-2 h-2 rounded-full"
                :class="{
                  'bg-green-500': webSocketStore.isConnected,
                  'bg-yellow-500': webSocketStore.isReconnecting,
                  'bg-red-500': !webSocketStore.isConnected && !webSocketStore.isReconnecting
                }"
              ></div>
              <span
                :class="{
                  'text-green-700': webSocketStore.isConnected,
                  'text-yellow-700': webSocketStore.isReconnecting,
                  'text-red-700': !webSocketStore.isConnected && !webSocketStore.isReconnecting
                }"
              >
                {{ 
                  webSocketStore.isConnected 
                    ? `Connected as ${webSocketStore.displayName}` 
                    : webSocketStore.isReconnecting 
                      ? 'Reconnecting...'
                      : 'Disconnected' 
                }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Camera Component - Takes remaining height with no overflow -->
    <div class="flex-1 min-h-0">
      <div class="h-full max-w-7xl mx-auto w-full">
        <CameraStream />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useServerStore } from '@/stores/server'
import { useWebSocketStore } from '@/stores/websocket'
import CameraStream from '@/components/CameraStream.vue'

const serverStore = useServerStore()
const webSocketStore = useWebSocketStore()

// If page is loaded without server configuration, redirect to setup
onMounted(() => {
  if (!serverStore.isConfigured) {
    const router = useRouter()
    router.push('/server-setup')
  }
})
</script>

<style scoped>
/* Status indicator animations */
.bg-green-500 {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* URL text truncation */
@media (max-width: 640px) {
  .text-sm {
    max-width: calc(100vw - 150px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

/* Prevent text selection on status items */
.text-sm {
  user-select: none;
  -webkit-user-select: none;
}
</style>
