<template>
  <div class="camera-stream">
    <div class="stream-controls">
      <button 
        @click="toggleStream" 
        :class="{ 'bg-red-500': isStreaming, 'bg-green-500': !isStreaming }"
        class="px-4 py-2 text-white rounded">
        {{ isStreaming ? 'Stop Stream' : 'Start Stream' }}
      </button>
    </div>
    
    <div class="stream-preview">
      <video 
        ref="localVideo" 
        autoplay 
        playsinline 
        muted 
        class="w-full max-w-lg border rounded"
      ></video>
    </div>

    <div v-if="error" class="error-message mt-4 p-4 bg-red-100 text-red-700 rounded">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import WebRTCService from '~/services/WebRTCService'

const localVideo = ref(null)
const isStreaming = ref(false)
const error = ref(null)
const mediaStream = ref(null)

// Initialize room and connection on component mount
onMounted(async () => {
  try {
    // Create or join room
    const response = await fetch('/api/create-room', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ roomId: 'default-room' })
    })
    
    const { routerRtpCapabilities, transportOptions } = await response.json()
    
    // Initialize MediaSoup device
    await WebRTCService.initializeDevice(routerRtpCapabilities)
    await WebRTCService.createSendTransport(transportOptions)
  } catch (err) {
    error.value = 'Failed to initialize streaming: ' + err.message
    console.error('Initialization error:', err)
  }
})

// Clean up on component unmount
onUnmounted(() => {
  stopStream()
})

const startStream = async () => {
  try {
    error.value = null
    mediaStream.value = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 30 }
      },
      audio: true
    })

    if (localVideo.value) {
      localVideo.value.srcObject = mediaStream.value
    }

    await WebRTCService.startStreaming(mediaStream.value)
    isStreaming.value = true
  } catch (err) {
    error.value = 'Failed to start stream: ' + err.message
    console.error('Streaming error:', err)
  }
}

const stopStream = async () => {
  try {
    if (mediaStream.value) {
      mediaStream.value.getTracks().forEach(track => track.stop())
      mediaStream.value = null
    }

    if (localVideo.value) {
      localVideo.value.srcObject = null
    }

    await WebRTCService.stopStreaming()
    isStreaming.value = false
  } catch (err) {
    error.value = 'Failed to stop stream: ' + err.message
    console.error('Stop streaming error:', err)
  }
}

const toggleStream = () => {
  if (isStreaming.value) {
    stopStream()
  } else {
    startStream()
  }
}
</script>

<style scoped>
.camera-stream {
  @apply p-4 max-w-2xl mx-auto;
}

.stream-controls {
  @apply mb-4 flex justify-center;
}

.stream-preview {
  @apply flex justify-center;
}

.error-message {
  @apply text-center;
}
</style>