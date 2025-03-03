<template>
  <ClientOnly>
    <!-- Main container with flexible height -->
    <div class="h-full flex flex-col">
      <!-- Camera Preview Area with Flex Grow -->
      <div class="relative flex-1 min-h-0 bg-gray-900">
        <!-- Video Element -->
        <video
          ref="localVideo"
          :class="[
            'absolute inset-0 w-full h-full object-cover',
            { 
              'hidden': !cameraStore.stream,
              'flip-horizontal': cameraStore.isFlipped 
            }
          ]"
          autoplay
          playsinline
          muted
        />

        <!-- Recording Status Overlay -->
        <div 
          v-if="cameraStore.isRecording" 
          class="absolute top-4 left-4 flex items-center gap-2 px-3 py-1.5 rounded-full bg-black/70 text-white text-sm"
        >
          <div class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
          <span>{{ cameraStore.recordingDuration }} | {{ cameraStore.captureCount }} frames ({{ cameraStore.selectedFps }} FPS)</span>
        </div>

        <!-- ML Processing Indicator -->
        <div
          v-if="mlStore.isProcessing"
          class="absolute top-4 right-4 flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-500/80 backdrop-blur-sm text-white text-sm animate-pulse"
        >
          <svg class="w-4 h-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>ML Processing</span>
        </div>

        <!-- Placeholder when no camera -->
        <div 
          v-if="!cameraStore.stream" 
          class="absolute inset-0 flex flex-col items-center justify-center text-gray-400"
        >
          <svg class="w-12 h-12 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
            <circle cx="12" cy="13" r="4" />
          </svg>
          <p class="text-base mb-1">No camera stream</p>
          <p class="text-sm opacity-75">Select a camera and click Start Camera</p>
        </div>
      </div>

      <!-- Fixed Controls Section -->
      <div class="flex-none bg-gray-800/90 backdrop-blur-sm text-white">
        <div class="p-3 space-y-2">
          <!-- Camera and FPS Selection -->
          <div class="flex items-center gap-2">
            <select 
              v-model="currentDevice"
              @change="handleDeviceChange"
              :disabled="!devices.length || cameraStore.stream"
              class="flex-1 h-10 px-3 bg-white/10 rounded border border-white/20 appearance-none text-white text-sm"
            >
              <option value="">Select camera</option>
              <option 
                v-for="device in devices" 
                :key="device.deviceId" 
                :value="device.deviceId"
              >
                {{ device.label || `Camera ${device.deviceId.slice(0, 5)}...` }}
              </option>
            </select>

            <select 
              v-if="cameraStore.stream && props.showFpsControl"
              v-model="cameraStore.selectedFps"
              :disabled="cameraStore.isRecording"
              class="w-24 h-10 px-3 bg-white/10 rounded border border-white/20 text-white text-sm"
            >
              <option 
                v-for="fps in availableFpsOptions" 
                :key="fps" 
                :value="fps"
              >
                {{ fps }} FPS
              </option>
            </select>
          </div>

          <!-- Control Buttons -->
          <div class="grid grid-cols-2 gap-2">
            <!-- Start/Stop Camera -->
            <button 
              v-if="!cameraStore.stream"
              @click="startCamera"
              :disabled="!currentDevice || !webSocketStore.isConnected"
              class="col-span-2 flex items-center justify-center gap-2 h-10 bg-green-500 text-white rounded font-medium text-sm disabled:opacity-50"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Start Camera
            </button>

            <template v-else>
              <!-- Stop Camera -->
              <button 
                @click="stopCamera"
                class="flex items-center justify-center gap-2 h-10 bg-red-500 text-white rounded font-medium text-sm"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Stop Camera
              </button>

              <!-- Flip Camera -->
              <button 
                @click="cameraStore.toggleFlip"
                :class="[
                  'flex items-center justify-center gap-2 h-10 rounded font-medium text-sm transition-colors',
                  cameraStore.isFlipped ? 'bg-blue-600 text-white' : 'bg-white/10 text-white'
                ]"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
                {{ cameraStore.isFlipped ? 'Unflip' : 'Flip' }}
              </button>

              <!-- Streaming Controls Grid -->
              <div class="col-span-2 grid grid-cols-2 gap-2">
                <!-- Toggle ML Processing -->
                <button 
                  @click="toggleMLProcessing"
                  :disabled="!webSocketStore.isConnected || !mlStore.isConnected"
                  :class="[
                    'flex items-center justify-center gap-2 h-10 rounded font-medium text-sm transition-colors',
                    mlStore.isMLProcessingEnabled ? 'bg-purple-500 hover:bg-purple-600' : 'bg-white/10 hover:bg-white/20',
                    'text-white disabled:opacity-50'
                  ]"
                >
                  <template v-if="mlStore.error">
                    <svg class="w-4 h-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span class="truncate">ML Error</span>
                  </template>
                  <template v-else-if="mlStore.isProcessing">
                    <svg class="w-4 h-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Processing...</span>
                  </template>
                  <template v-else>
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
                      />
                    </svg>
                    <span>{{ mlStore.isMLProcessingEnabled ? 'Processing Enabled' : 'Enable Processing' }}</span>
                  </template>
                </button>

                <!-- Capture Frame -->
                <button 
                  @click="handleSingleCapture"
                  :disabled="!webSocketStore.isConnected || cameraStore.isRecording || isCapturing"
                  class="flex items-center justify-center gap-2 h-10 bg-purple-500 text-white rounded font-medium text-sm disabled:opacity-50"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {{ isCapturing ? 'Capturing...' : 'Capture' }}
                </button>

                <!-- Record Button -->
                <button 
                  @click="toggleRecording"
                  :disabled="!webSocketStore.isConnected"
                  class="col-span-2 flex items-center justify-center gap-2 h-10 rounded font-medium text-sm disabled:opacity-50"
                  :class="[
                    cameraStore.isRecording ? 'bg-red-500' : 'bg-orange-500'
                  ]"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path 
                      v-if="!cameraStore.isRecording"
                      stroke-linecap="round" 
                      stroke-linejoin="round" 
                      stroke-width="2" 
                      d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                    />
                    <path 
                      v-else 
                      stroke-linecap="round" 
                      stroke-linejoin="round" 
                      stroke-width="2" 
                      d="M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"
                    />
                  </svg>
                  {{ cameraStore.isRecording ? 'Stop' : 'Record' }}
                </button>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Flash Effect -->
      <div 
        v-if="showCaptureEffect" 
        class="fixed inset-0 bg-white pointer-events-none animate-flash"
      />

      <!-- Capture Success Toast -->
      <div 
        v-if="showNotification"
        class="fixed top-safe left-1/2 transform -translate-x-1/2 flex items-center gap-2 px-4 py-2 bg-black/90 text-white rounded-full text-sm animate-slideDown"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        Frame captured!
      </div>

      <!-- Error Display -->
      <div 
        v-if="cameraStore.error"
        class="fixed bottom-safe left-4 right-4 p-4 bg-red-500 text-white rounded-lg shadow-lg animate-slideUp"
      >
        {{ cameraStore.error }}
      </div>
    </div>
  </ClientOnly>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useWebSocketStore } from '@/stores/websocket'
import { useMLStore } from '@/stores/ml'
import { useCameraStore } from '@/stores/camera'

// Props with validation
interface Props {
  maxFps?: number
  minFps?: number
  persistStream?: boolean
  showFpsControl?: boolean
  showFlipControl?: boolean
}

// Define emits
const emit = defineEmits<{
  'update:stream': [MediaStream | null]
  'camera-start': [string] // deviceId
  'camera-stop': [void]
  'recording-start': [void]
  'recording-stop': [number] // frameCount
  'error': [string]
}>()

const props = withDefaults(defineProps<Props>(), {
  maxFps: 30,
  minFps: 1,
  persistStream: true,
  showFpsControl: true,
  showFlipControl: true
})

// Store instantiation
const cameraStore = useCameraStore()
const webSocketStore = useWebSocketStore()
const mlStore = useMLStore()

// UI state
const localVideo = ref<HTMLVideoElement | null>(null)
const showCaptureEffect = ref(false)
const isCapturing = ref(false)
const showNotification = ref(false)
const isLoading = ref(false)

// Device management
const hasGetUserMedia = ref(false)
const devices = ref<MediaDeviceInfo[]>([])
const currentDevice = ref<string>('')

// Computed
const availableFpsOptions = computed(() => {
  const defaultOptions = [1, 2, 5, 10, 15, 30]
  return defaultOptions.filter(fps => 
    fps >= props.minFps && fps <= props.maxFps
  )
})

// Methods
const startCamera = async () => {
  if (!currentDevice.value || isLoading.value) return
  
  isLoading.value = true
  try {
    await cameraStore.initializeCamera(currentDevice.value)
    if (localVideo.value && cameraStore.stream) {
      localVideo.value.srcObject = cameraStore.stream
      emit('update:stream', cameraStore.stream)
      emit('camera-start', currentDevice.value)
    }

    // If ML processing is enabled, ensure connection
    if (mlStore.isMLProcessingEnabled && !mlStore.isConnected) {
      await mlStore.autoConnect()
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to start camera'
    cameraStore.error = errorMessage
    emit('error', errorMessage)
  } finally {
    isLoading.value = false
  }
}

const stopCamera = () => {
  const hadStream = !!cameraStore.stream
  cameraStore.stopCamera()
  if (localVideo.value) {
    localVideo.value.srcObject = null
  }
  if (hadStream) {
    emit('update:stream', null)
    emit('camera-stop')
    
    // Clear stream states
    webSocketStore.clearMessages()
    mlStore.clearProcessedStreams()
  }
}

const handleDeviceChange = async () => {
  if (!currentDevice.value || !cameraStore.stream || isLoading.value) return
  
  isLoading.value = true
  try {
    await cameraStore.switchCamera(currentDevice.value)
    if (localVideo.value && cameraStore.stream) {
      localVideo.value.srcObject = cameraStore.stream
      emit('update:stream', cameraStore.stream)
      emit('camera-start', currentDevice.value)
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to switch camera'
    cameraStore.error = errorMessage
    emit('error', errorMessage)
  } finally {
    isLoading.value = false
  }
}

const handleSingleCapture = async () => {
  if (isCapturing.value) return
  
  try {
    isCapturing.value = true
    showCaptureEffect.value = true

    const frame = await cameraStore.captureFrame({ showEffects: true })
    if (frame) {
      // Send to main WebSocket server
      webSocketStore.sendMessage({
      type: 'frame',
      content: frame,
      timestamp: new Date().toISOString()
    });

      // Send to ML server if enabled
      if (mlStore.isMLProcessingEnabled && mlStore.isConnected) {
        await mlStore.sendFrame(frame)
      }
    }

    showNotification.value = true
    setTimeout(() => {
      showNotification.value = false
    }, 2000)
  } finally {
    isCapturing.value = false
    setTimeout(() => {
      showCaptureEffect.value = false
    }, 200)
  }
}

const toggleRecording = async () => {
  if (cameraStore.isRecording) {
    cameraStore.stopRecording()
    emit('recording-stop', cameraStore.captureCount)
  } else {
    cameraStore.startRecording()
    emit('recording-start')
  }
}

const toggleMLProcessing = async () => {
  // Toggle ML processing state
  mlStore.isMLProcessingEnabled = !mlStore.isMLProcessingEnabled

  // If enabling ML processing, ensure connection
  if (mlStore.isMLProcessingEnabled && !mlStore.isConnected) {
    await mlStore.autoConnect()
  }
}

// Camera device enumeration
const getCameraDevices = async () => {
  try {
    // Check for permissions first
    const permissions = await navigator.permissions.query({ name: 'camera' as PermissionName })
    
    if (permissions.state === 'denied') {
      throw new Error('Camera permission denied. Please enable camera access.')
    }

    // Request camera access if not already granted
    if (permissions.state === 'prompt') {
      const tempStream = await navigator.mediaDevices.getUserMedia({ video: true })
      tempStream.getTracks().forEach(track => track.stop())
    }

    // Enumerate devices
    const deviceList = await navigator.mediaDevices.enumerateDevices()
    const videoDevices = deviceList.filter(device => device.kind === 'videoinput')

    if (videoDevices.length === 0) {
      throw new Error('No camera devices found')
    }

    devices.value = videoDevices
    
    // Only set default device if not already set
    if (!currentDevice.value && devices.value.length > 0) {
      currentDevice.value = devices.value[0].deviceId
    }
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : 'Failed to get camera devices'
    cameraStore.error = errorMessage
    console.error('Error getting camera devices:', err)
  }
}

// Watch for frame processing
watch(() => cameraStore.isRecording, async (isRecording) => {
  if (isRecording) {
    // Ensure WebSocket is connected
    if (!webSocketStore.isConnected) {
      await webSocketStore.autoConnect()
    }

    // Ensure ML server is connected if ML processing is enabled
    if (mlStore.isMLProcessingEnabled && !mlStore.isConnected) {
      await mlStore.autoConnect()
    }
  }
})

// Initialize
onMounted(async () => {
  hasGetUserMedia.value = !!(
    navigator.mediaDevices?.getUserMedia &&
    navigator.mediaDevices?.enumerateDevices
  )

  if (hasGetUserMedia.value) {
    await getCameraDevices()
    // Setup device change listener
    navigator.mediaDevices.addEventListener('devicechange', getCameraDevices)
    // Restore video stream if it was active
    if (cameraStore.stream && localVideo.value) {
      localVideo.value.srcObject = cameraStore.stream
    }
  }
})

// Clean up
onUnmounted(() => {
  // Don't stop camera on unmount if persistence is enabled
  if (!props.persistStream) {
    stopCamera()
  }
  
  if (localVideo.value) {
    localVideo.value.srcObject = null
  }
  
  if (hasGetUserMedia.value) {
    navigator.mediaDevices.removeEventListener('devicechange', getCameraDevices)
  }
})
</script>

<style scoped>
.flip-horizontal {
  transform: scaleX(-1);
}

/* Flash animation */
@keyframes flash {
  0% { opacity: 0; }
  50% { opacity: 0.8; }
  100% { opacity: 0; }
}

.animate-flash {
  animation: flash 200ms ease-out forwards;
}

/* Notification animation */
@keyframes slideDown {
  0% { 
    transform: translateX(-50%) translateY(-100%);
    opacity: 0;
  }
  100% { 
    transform: translateX(-50%) translateY(0);
    opacity: 1;
  }
}

.animate-slideDown {
  animation: slideDown 200ms ease-out forwards;
}

/* Error animation */
@keyframes slideUp {
  0% {
    transform: translateY(100%);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slideUp {
  animation: slideUp 200ms ease-out forwards;
}

/* Mobile optimizations */
@media (max-width: 640px) {
  select, button {
    -webkit-tap-highlight-color: transparent;
    -webkit-touch-callout: none;
    user-select: none;
  }

  /* Custom select styling */
  select {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
    background-position: right 0.75rem center;
    background-repeat: no-repeat;
    background-size: 1.25rem;
    padding-right: 2.5rem;
  }
}

/* Safe area positioning utils */
.top-safe {
  top: max(1rem, env(safe-area-inset-top));
}

.bottom-safe {
  bottom: max(1rem, env(safe-area-inset-bottom));
}

/* Edge-to-edge video for iOS */
@supports (-webkit-touch-callout: none) {
  video {
    width: 100%;
    height: 100%;
  }
}

/* Prevent text selection */
button {
  user-select: none;
  -webkit-user-select: none;
}

/* Chrome video background fix */
video {
  background-color: #000;
}

/* Processing state animations */
.animate-processing {
  animation: processing 2s ease-in-out infinite;
}

@keyframes processing {
  0%, 100% { 
    opacity: 1;
    transform: scale(1);
  }
  50% { 
    opacity: 0.7;
    transform: scale(0.98);
  }
}
</style>