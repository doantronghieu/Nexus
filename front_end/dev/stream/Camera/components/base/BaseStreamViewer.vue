<template>
  <div class="h-[calc(100dvh-6rem)] flex flex-col bg-gray-100">
    <!-- Status header - fixed height -->
    <div v-if="showHeader" class="flex-none bg-white shadow-sm">
      <div class="max-w-7xl mx-auto w-full px-4 py-2">
        <div class="flex flex-col space-y-1">
          <!-- Server Status -->
          <div class="flex items-center gap-2">
            <span class="text-gray-600 min-w-[100px] text-sm">{{ connectionLabel }}:</span>
            <div class="flex items-center gap-2 text-sm">
              <div 
                class="w-2 h-2 rounded-full"
                :class="{
                  'bg-green-500': isConnected,
                  'bg-red-500': !isConnected
                }"
              ></div>
              <span 
                :class="{
                  'text-green-700': isConnected,
                  'text-red-700': !isConnected,
                }"
              >
                {{ connectionStatus }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Streams Grid -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <div class="container mx-auto px-0 sm:px-4 h-full">
        <div class="max-w-7xl mx-auto h-full">
          <!-- Header Section -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-0 p-4 sm:p-0 sm:mb-6 bg-white sm:bg-transparent border-b sm:border-0">
            <div class="flex items-center justify-between">
              <h1 class="text-xl sm:text-2xl font-bold text-gray-900">{{ title }}</h1>
              <div class="ml-3 text-sm font-medium text-gray-500">
                {{ streamingClientsCount }} active {{ streamingClientsCount === 1 ? 'stream' : 'streams' }}
              </div>
            </div>
            <button
              v-if="hasActiveStreams && !selectedStreamId"
              @click="toggleFullscreen"
              class="w-full sm:w-auto min-h-[44px] sm:min-h-0 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 active:bg-gray-300 transition-colors text-sm font-medium"
            >
              <span v-if="isFullscreen">Exit Grid Fullscreen</span>
              <span v-else>View Grid Fullscreen</span>
            </button>
          </div>

          <!-- Streams Grid -->
          <div 
            v-if="hasActiveStreams" 
            ref="streamGrid"
            class="grid gap-4 sm:gap-6 transition-all duration-300 sm:mt-0 h-full"
            :class="[gridClass, { 'pointer-events-none': isModalOpen }]"
          >
            <div 
              v-for="client in activeStreams"
              :key="client.id"
              class="stream-container bg-white sm:rounded-lg shadow-sm sm:shadow overflow-hidden transition-all duration-300"
              :class="{ 'cursor-pointer': !isFullscreen }"
              @click="openStreamModal(client)"
            >
              <!-- Stream Preview -->
              <div class="relative aspect-video bg-gray-900">
                <img 
                  v-if="client.lastFrame"
                  :src="client.lastFrame"
                  class="w-full h-full object-cover"
                  :class="{ 'selected-stream': selectedStreamId === client.id }"
                  alt="Stream preview"
                  @error="handleImageError(client.id)"
                />
                <div
                  v-else
                  class="absolute inset-0 flex items-center justify-center text-gray-500"
                >
                  <div class="text-center p-4">
                    <svg class="w-12 h-12 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    <span class="text-sm">Waiting for frames...</span>
                  </div>
                </div>
                
                <!-- Stream Info Overlay -->
                <div class="absolute bottom-0 left-0 right-0 bg-black/60 backdrop-blur-sm text-white p-3 sm:p-4">
                  <div class="flex justify-between items-start sm:items-center gap-2">
                    <div class="flex items-start sm:items-center gap-2 min-w-0">
                      <div 
                        class="w-2.5 h-2.5 rounded-full mt-1.5 sm:mt-0 flex-shrink-0"
                        :class="{
                          'bg-green-500 animate-pulse': client.isStreaming,
                          'bg-red-500': !client.isStreaming
                        }"
                      ></div>
                      <div class="min-w-0">
                        <div class="flex items-center gap-2 flex-wrap">
                          <span class="font-medium truncate">{{ client.displayName }}</span>
                          <span 
                            v-if="client.isLocal" 
                            class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-blue-500/90 text-white"
                          >
                            You
                          </span>
                        </div>
                        <div class="text-sm text-white/75 mt-0.5">
                          Streaming for {{ formatDuration(getStreamDuration(client)) }}
                        </div>
                      </div>
                    </div>
                    <div class="flex flex-col sm:flex-row items-end sm:items-center gap-1 sm:gap-3 text-sm text-white/90">
                      <span class="whitespace-nowrap">{{ client.metrics.fps }} FPS</span>
                      <span class="whitespace-nowrap">{{ client.metrics.frameCount }} frames</span>
                    </div>
                  </div>
                </div>

                <!-- Stream Error Overlay -->
                <div 
                  v-if="streamErrors[client.id]"
                  class="absolute inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center text-white"
                >
                  <div class="text-center px-4">
                    <svg class="w-8 h-8 mx-auto mb-2 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div class="text-sm mb-3">Failed to load stream</div>
                    <button 
                      @click.stop="retryStream(client.id)"
                      class="min-h-[36px] px-4 py-1.5 bg-red-500 text-white rounded-full text-sm font-medium hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 active:bg-red-700 transition-colors"
                    >
                      Retry
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- No Streams Message -->
          <div 
            v-else
            class="flex flex-col items-center justify-center min-h-[50vh] mx-4"
          >
            <div class="w-full max-w-sm bg-white rounded-lg shadow-sm p-6 text-center">
              <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                No active streams
              </h3>
              <p class="text-sm text-gray-500 mb-6">
                {{ noStreamsMessage }}
              </p>
              <NuxtLink
                :to="streamPageLink"
                class="inline-flex items-center justify-center min-h-[44px] px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-sm font-medium transition-colors active:bg-blue-700"
              >
                {{ streamPageText }}
              </NuxtLink>
            </div>
          </div>

          <!-- Stream Modal -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div
              v-if="selectedStreamId"
              class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
              @click="closeStreamModal"
            >
              <div 
                class="flex flex-col h-full"
                @click.stop
              >
                <!-- Modal Header -->
                <div class="flex items-center justify-between p-4 bg-black/40">
                  <div class="flex items-center gap-3">
                    <button
                      @click="closeStreamModal"
                      class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-white/10 hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/50 active:bg-white/30 transition-colors"
                      aria-label="Close stream view"
                    >
                      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                    <div class="text-white">
                      <h2 class="text-lg font-medium">
                        {{ selectedStream?.displayName }}
                      </h2>
                    </div>
                  </div>
                  <button
                    @click="toggleModalFullscreen"
                    class="inline-flex items-center justify-center h-10 px-4 rounded-lg bg-white/10 hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/50 active:bg-white/30 transition-colors text-white text-sm"
                  >
                    <span v-if="isModalFullscreen">Exit Fullscreen</span>
                    <span v-else>Fullscreen</span>
                  </button>
                </div>

                <!-- Modal Content -->
                <div class="flex-1 relative bg-black">
                  <img
                    v-if="selectedStream?.lastFrame"
                    :src="selectedStream.lastFrame"
                    class="absolute inset-0 w-full h-full object-contain"
                    alt="Stream preview"
                  />
                  <!-- Stream Info Overlay -->
                  <div class="absolute bottom-0 left-0 right-0 bg-black/60 backdrop-blur-sm text-white p-4">
                    <div class="flex justify-between items-center">
                      <div class="flex items-center gap-3">
                        <div 
                          class="w-2.5 h-2.5 rounded-full"
                          :class="{
                            'bg-green-500 animate-pulse': selectedStream?.isStreaming,
                            'bg-red-500': !selectedStream?.isStreaming
                          }"
                        ></div>
                        <div class="text-sm">
                          Streaming for {{ formatDuration(getStreamDuration(selectedStream)) }}
                        </div>
                      </div>
                      <div class="flex items-center gap-4 text-sm">
                        <span>{{ selectedStream?.metrics.fps }} FPS</span>
                        <span>{{ selectedStream?.metrics.frameCount }} frames</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface StreamMetrics {
  frameCount: number
  fps: number
  startTime: number | null
  lastUpdateTime: number
}

interface StreamClient {
  id: string
  displayName: string
  lastFrame: string | null
  isStreaming: boolean
  metrics: StreamMetrics
  isLocal: boolean
}

interface Props {
  title: string
  showHeader?: boolean
  connectionLabel?: string
  isConnected?: boolean
  connectionStatus?: string
  activeStreams: StreamClient[]
  streamingClientsCount: number
  noStreamsMessage?: string
  streamPageLink?: string
  streamPageText?: string
  getStreamDuration: (client: StreamClient | undefined) => number
}

const props = withDefaults(defineProps<Props>(), {
  showHeader: true,
  connectionLabel: 'Server',
  isConnected: false,
  connectionStatus: 'Not Connected',
  noStreamsMessage: 'Start streaming from the Camera Stream page to see streams here',
  streamPageLink: '/camera-stream',
  streamPageText: 'Go to Camera Stream'
})

const emit = defineEmits<{
  (e: 'retryStream', clientId: string): void
  (e: 'streamError', clientId: string): void
}>()

const streamGrid = ref<HTMLElement | null>(null)
const isFullscreen = ref(false)
const isModalFullscreen = ref(false)
const selectedStreamId = ref<string | null>(null)
const streamErrors = ref<Record<string, boolean>>({})

// Computed
const hasActiveStreams = computed(() => props.activeStreams.length > 0)
const isModalOpen = computed(() => !!selectedStreamId.value)

const selectedStream = computed(() => 
  props.activeStreams.find(client => client.id === selectedStreamId.value)
)

const gridClass = computed(() => {
  const count = props.activeStreams.length
  if (count === 1) return 'grid-cols-1'
  if (count === 2) return 'grid-cols-1 md:grid-cols-2'
  if (count === 3) return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
  return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
})

// Methods
const formatDuration = (milliseconds: number): string => {
  if (!milliseconds) return '0s'
  
  const seconds = Math.floor(milliseconds / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  
  if (hours > 0) {
    return `${hours}h ${minutes % 60}m`
  }
  if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`
  }
  return `${seconds}s`
}

const openStreamModal = (client: StreamClient) => {
  if (!isFullscreen.value) {
    selectedStreamId.value = client.id
    document.body.style.overflow = 'hidden' // Prevent background scrolling
  }
}

const closeStreamModal = () => {
  selectedStreamId.value = null
  isModalFullscreen.value = false
  document.body.style.overflow = '' // Restore scrolling
  if (document.fullscreenElement) {
    document.exitFullscreen().catch(err => {
      console.error('Error exiting fullscreen:', err)
    })
  }
}

const handleImageError = (clientId: string) => {
  streamErrors.value[clientId] = true
  emit('streamError', clientId)
}

const retryStream = (clientId: string) => {
  streamErrors.value[clientId] = false
  emit('retryStream', clientId)
}

// Fullscreen handling for grid view
const toggleFullscreen = async () => {
  if (!document.fullscreenElement) {
    if (streamGrid.value?.requestFullscreen) {
      try {
        await streamGrid.value.requestFullscreen()
        isFullscreen.value = true
      } catch (err) {
        console.error('Grid fullscreen error:', err)
      }
    }
  } else {
    if (document.exitFullscreen) {
      try {
        await document.exitFullscreen()
        isFullscreen.value = false
      } catch (err) {
        console.error('Exit grid fullscreen error:', err)
      }
    }
  }
}

// Fullscreen handling for modal view
const toggleModalFullscreen = async () => {
  const modalElement = document.querySelector('[data-modal-content]')
  if (!modalElement) return

  if (!document.fullscreenElement) {
    try {
      await modalElement.requestFullscreen()
      isModalFullscreen.value = true
    } catch (err) {
      console.error('Modal fullscreen error:', err)
    }
  } else {
    try {
      await document.exitFullscreen()
      isModalFullscreen.value = false
    } catch (err) {
      console.error('Exit modal fullscreen error:', err)
    }
  }
}

// Fullscreen change event handler
const handleFullscreenChange = () => {
  if (!document.fullscreenElement) {
    isFullscreen.value = false
    isModalFullscreen.value = false
  }
}

// Handle escape key for modal
const handleEscapeKey = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && selectedStreamId.value) {
    closeStreamModal()
  }
}

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange)
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
  document.removeEventListener('keydown', handleEscapeKey)
  document.body.style.overflow = '' // Restore scrolling
})

// Expose methods for parent components
defineExpose({
  closeStreamModal,
  selectedStreamId
})
</script>

<style scoped>
.stream-container {
  transform-origin: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  -webkit-tap-highlight-color: transparent;
}

.stream-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
}

.selected-stream {
  border: 2px solid #3B82F6;
}

/* Grid responsiveness */
@media (min-width: 768px) {
  .grid {
    grid-auto-rows: 1fr;
  }
}

/* Fullscreen mode */
:fullscreen .stream-container {
  height: 100vh;
  margin: 0;
  border-radius: 0;
}

:fullscreen .grid {
  height: 100vh;
  gap: 0;
}

:fullscreen .stream-container:hover {
  transform: none;
  box-shadow: none;
}

/* Mobile optimizations */
@media (max-width: 640px) {
  .stream-container {
    border-radius: 0;
    margin: 0;
    border-bottom: 1px solid rgb(229 231 235);
  }

  .stream-container:last-child {
    border-bottom: none;
  }

  .grid {
    gap: 0;
  }

  /* Disable hover effects on mobile */
  .stream-container:hover {
    transform: none;
    box-shadow: none;
  }

  /* Improve touch targets */
  button {
    min-height: 44px;
  }

  /* Safe area insets for notched devices */
  @supports (padding: max(0px)) {
    .container {
      padding-left: max(0px, env(safe-area-inset-left));
      padding-right: max(0px, env(safe-area-inset-right));
      padding-bottom: max(0px, env(safe-area-inset-bottom));
    }

    /* Adjust modal padding for safe areas */
    [data-modal-content] {
      padding-top: max(16px, env(safe-area-inset-top));
      padding-bottom: max(16px, env(safe-area-inset-bottom));
    }
  }

  /* Smooth scrolling */
  .grid {
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
  }
}

/* iOS specific styles */
@supports (-webkit-touch-callout: none) {
  .stream-container {
    /* Disable gray highlight on tap */
    -webkit-tap-highlight-color: transparent;
  }

  /* Fix for iOS Safari sticky hover */
  @media (hover: hover) {
    .stream-container:hover {
      transform: translateY(-2px);
    }
  }
  
  /* Fix for iOS Safari viewport height */
  :fullscreen .stream-container {
    height: -webkit-fill-available;
  }

  /* Modal height fix for iOS */
  [data-modal-content] {
    min-height: -webkit-fill-available;
  }
}

/* Reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  .stream-container,
  .stream-enter-active,
  .stream-leave-active,
  .animate-pulse {
    transition: none;
    animation: none;
  }
  
  .stream-container:hover {
    transform: none;
  }
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Ensure modal content is above other elements */
[data-modal-content] {
  position: relative;
  z-index: 60;
}
</style>