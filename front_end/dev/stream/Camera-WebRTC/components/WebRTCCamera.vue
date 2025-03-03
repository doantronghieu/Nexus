<template>
  <div class="camera-container">
    <ClientOnly>
      <!-- Camera Container with placeholder -->
      <div class="video-wrapper" :class="{ 'no-camera': !stream }">
        <!-- Video element -->
        <video
          ref="localVideo"
          :class="{ 
            'camera-preview': true, 
            hidden: !stream,
            'flip-horizontal': isFlipped 
          }"
          autoplay
          playsinline
          muted
        />

        <!-- Placeholder when camera is not active -->
        <div v-if="!stream" class="camera-placeholder">
          <div class="placeholder-content">
            <svg 
              class="camera-icon" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              stroke-width="2"
            >
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
            <p class="placeholder-text">No camera stream</p>
            <p class="placeholder-subtext">Select a camera and click Start Camera</p>
          </div>
        </div>
      </div>

      <!-- Camera controls in a fixed container -->
      <div class="camera-controls" v-if="hasGetUserMedia">
        <div class="controls-wrapper">
          <!-- Camera selection -->
          <select 
            v-model="currentDevice"
            @change="handleDeviceChange"
            :disabled="!devices.length || stream || isContinuousCapture"
            class="camera-select"
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

          <!-- FPS Control -->
          <div class="fps-control" v-if="stream">
            <label class="control-label">Frame Rate (FPS)</label>
            <div class="fps-input-group">
              <input 
                type="range" 
                v-model.number="fps"
                min="1"
                max="30"
                step="1"
                class="fps-slider"
                :disabled="isContinuousCapture"
              />
              <span class="fps-value">{{ fps }} FPS</span>
            </div>
          </div>

          <!-- Control buttons -->
          <div class="button-group">
            <button 
              @click="startCamera" 
              v-if="!stream"
              class="control-button start"
              :disabled="!currentDevice"
            >
              Start Camera
            </button>
            <template v-if="stream">
              <button 
                @click="stopCamera" 
                class="control-button stop"
              >
                Stop Camera
              </button>
              <button 
                @click="isFlipped = !isFlipped" 
                class="control-button"
                :class="{ 'active': isFlipped }"
              >
                {{ isFlipped ? 'Unflip' : 'Flip' }}
              </button>
              <button 
                @click="toggleContinuousCapture" 
                class="control-button"
                :class="{ 'recording': isContinuousCapture }"
                :disabled="isSaving"
              >
                {{ isContinuousCapture ? 'Stop Capture' : 'Start Capture' }}
              </button>
              <button 
                @click="saveFrame" 
                class="control-button save"
                :disabled="isSaving || isContinuousCapture"
              >
                {{ isSaving ? 'Saving...' : 'Save Frame' }}
              </button>
            </template>
          </div>

          <!-- Capture Stats -->
          <div v-if="isContinuousCapture" class="capture-stats">
            <div class="stat-item">
              <span class="stat-label">Duration:</span>
              <span class="stat-value">{{ formatDuration(captureDuration) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Frames Sent:</span>
              <span class="stat-value">{{ framesSent }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Current FPS:</span>
              <span class="stat-value">{{ currentFps.toFixed(1) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Error message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="!hasGetUserMedia" class="error-message">
        Camera access is not supported in your browser.
      </div>
    </ClientOnly>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useCamera } from '~/composables/useCamera'
import { useConfig } from '~/composables/useConfig'
import { useNotification } from '~/composables/useNotification'

export default {
  name: 'WebRTCCamera',
  
  setup() {
    const localVideo = ref(null)
    const hasGetUserMedia = ref(false)
    const error = ref(null)
    const isSaving = ref(false)
    const isFlipped = ref(false)
    
    // Continuous capture state
    const fps = ref(15)
    const isContinuousCapture = ref(false)
    const framesSent = ref(0)
    const currentFps = ref(0)
    const captureInterval = ref(null)
    const lastFrameTime = ref(Date.now())
    const fpsUpdateInterval = ref(null)
    const captureStartTime = ref(null)
    const captureDuration = ref(0)
    const durationInterval = ref(null)

    const { 
      stream, 
      devices, 
      currentDevice, 
      error: cameraError,
      getCameraDevices,
      startCamera: initCamera,
      switchCamera,
      stopCamera: stopCameraStream
    } = useCamera()

    const {
      setupWebSocket,
      addMessageHandler,
      removeMessageHandler,
      sendMessage,
      connectionStatus,
      getFastAPIBaseUrl,
      getCurrentClientId
    } = useConfig()

    const { success, error: showError } = useNotification()

    // WebRTC configuration
    const peerConnection = ref(null)
    const isConnected = ref(false)
    const configuration = {
      iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
    }

    // WebRTC handlers
    const handleSignalingMessage = (data) => {
      if (!peerConnection.value) return

      try {
        switch (data.type) {
          case 'offer':
            handleOffer(data)
            break
          case 'answer':
            handleAnswer(data)
            break
          case 'ice-candidate':
            handleIceCandidate(data)
            break
          case 'client-disconnected':
            handleClientDisconnected(data)
            break
        }
      } catch (err) {
        console.error('Error handling signaling message:', err)
        error.value = 'Signaling error occurred'
      }
    }

    const createPeerConnection = () => {
      if (peerConnection.value) {
        peerConnection.value.close()
      }

      peerConnection.value = new RTCPeerConnection(configuration)

      peerConnection.value.onicecandidate = ({ candidate }) => {
        if (candidate) {
          sendMessage({
            type: 'ice-candidate',
            candidate
          })
        }
      }

      peerConnection.value.ontrack = (event) => {
        if (localVideo.value) {
          localVideo.value.srcObject = event.streams[0]
        }
      }

      peerConnection.value.onconnectionstatechange = () => {
        isConnected.value = peerConnection.value?.connectionState === 'connected'
        if (peerConnection.value?.connectionState === 'failed') {
          restartConnection()
        }
      }
    }

    const handleOffer = async (data) => {
      await peerConnection.value.setRemoteDescription(new RTCSessionDescription(data.offer))
      const answer = await peerConnection.value.createAnswer()
      await peerConnection.value.setLocalDescription(answer)
      
      sendMessage({
        type: 'answer',
        answer,
        targetId: data.clientId
      })
    }

    const handleAnswer = async (data) => {
      await peerConnection.value.setRemoteDescription(new RTCSessionDescription(data.answer))
    }

    const handleIceCandidate = async (data) => {
      if (data.candidate) {
        await peerConnection.value.addIceCandidate(new RTCIceCandidate(data.candidate))
      }
    }

    const handleClientDisconnected = (data) => {
      cleanup()
    }

    // Frame capture functions
    const captureFrame = async () => {
      if (!localVideo.value || !stream.value) return null

      const canvas = document.createElement('canvas')
      const video = localVideo.value
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      
      const ctx = canvas.getContext('2d')
      if (isFlipped.value) {
        ctx.scale(-1, 1)
        ctx.translate(-canvas.width, 0)
      }
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      
      return new Promise((resolve) => {
        canvas.toBlob((blob) => resolve(blob), 'image/jpeg', 0.95)
      })
    }

    // Update FPS calculation
    const updateCurrentFps = () => {
      const now = Date.now()
      const timeDiff = now - lastFrameTime.value
      currentFps.value = 1000 / timeDiff
      lastFrameTime.value = now
    }

    // Continuous capture functions
    const updateDuration = () => {
      if (captureStartTime.value) {
        const elapsed = Date.now() - captureStartTime.value
        captureDuration.value = Math.floor(elapsed / 1000)
      }
    }

    const formatDuration = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    const startContinuousCapture = () => {
      if (captureInterval.value) return

      const interval = Math.floor(1000 / fps.value)
      framesSent.value = 0
      captureStartTime.value = Date.now()
      captureDuration.value = 0

      // Start duration timer
      durationInterval.value = setInterval(updateDuration, 1000)
  
      captureInterval.value = setInterval(async () => {
        try {
          const frameBlob = await captureFrame()
          if (!frameBlob) return

          const formData = new FormData()
          formData.append('frame', frameBlob, 'frame.jpg')

          const response = await fetch(`${getFastAPIBaseUrl()}/save-frame/${getCurrentClientId()}`, {
            method: 'POST',
            body: formData
          })

          if (response.ok) {
            framesSent.value++
            updateCurrentFps()
          }
        } catch (err) {
          console.error('Frame capture error:', err)
        }
      }, interval)

      // Start FPS monitoring
      fpsUpdateInterval.value = setInterval(() => {
        if (framesSent.value > 0) {
          currentFps.value = fps.value // Smooth out display
        }
      }, 1000)
    }

    const stopContinuousCapture = () => {
      if (captureInterval.value) {
        clearInterval(captureInterval.value)
        captureInterval.value = null
      }
      if (fpsUpdateInterval.value) {
        clearInterval(fpsUpdateInterval.value)
        fpsUpdateInterval.value = null
      }
      if (durationInterval.value) {
        clearInterval(durationInterval.value)
        durationInterval.value = null
      }
      captureStartTime.value = null
      captureDuration.value = 0
      currentFps.value = 0
    }

    const toggleContinuousCapture = () => {
      isContinuousCapture.value = !isContinuousCapture.value
      if (isContinuousCapture.value) {
        startContinuousCapture()
        success(`Started continuous capture at ${fps.value} FPS`)
      } else {
        const duration = formatDuration(captureDuration.value)
        stopContinuousCapture()
        success(`Stopped continuous capture. Duration: ${duration}, Total frames: ${framesSent.value}`)
      }
    }

    // Single frame capture
    const saveFrame = async () => {
      const currentClientId = getCurrentClientId()
      
      if (!currentClientId) {
        showError('No active connection')
        return
      }

      try {
        isSaving.value = true
        const frameBlob = await captureFrame()
        if (!frameBlob) {
          throw new Error('Failed to capture frame')
        }

        const formData = new FormData()
        formData.append('frame', frameBlob, 'frame.jpg')

        const response = await fetch(`${getFastAPIBaseUrl()}/save-frame/${currentClientId}`, {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error('Failed to save frame')
        }

        const result = await response.json()
        console.log('Frame saved:', result)
        success('Frame saved successfully')
      } catch (err) {
        showError(err.message)
        console.error('Error saving frame:', err)
      } finally {
        isSaving.value = false
      }
    }

    // Camera control functions
    const startCamera = async () => {
      try {
        await initCamera(currentDevice.value)
        createPeerConnection()

        if (localVideo.value && stream.value) {
          localVideo.value.srcObject = stream.value
        }
        
        if (stream.value) {
          stream.value.getTracks().forEach(track => {
            peerConnection.value.addTrack(track, stream.value)
          })
          
          const offer = await peerConnection.value.createOffer()
          await peerConnection.value.setLocalDescription(offer)
          
          sendMessage({
            type: 'offer',
            offer
          })
        }
        
        error.value = null
      } catch (err) {
        error.value = 'Failed to start camera'
        console.error(err)
      }
    }

    const stopCamera = () => {
      if (isContinuousCapture.value) {
        stopContinuousCapture()
        isContinuousCapture.value = false
      }
      stopCameraStream()
      if (peerConnection.value) {
        peerConnection.value.close()
        peerConnection.value = null
      }
      error.value = null
    }

    const restartConnection = async () => {
      stopCamera()
      await new Promise(resolve => setTimeout(resolve, 1000))
      await startCamera()
    }

    const cleanup = () => {
      stopCamera()
      removeMessageHandler(handleSignalingMessage)
    }

    // Handle device selection change
    const handleDeviceChange = async () => {
      if (currentDevice.value && stream.value) {
        await switchCamera(currentDevice.value)
      }
    }

    // Watch for camera errors
    watch(cameraError, (newError) => {
      error.value = newError
    })

    // Watch for stream changes
    watch(stream, (newStream) => {
      if (!newStream && isContinuousCapture.value) {
        stopContinuousCapture()
        isContinuousCapture.value = false
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
        setupWebSocket()
        addMessageHandler(handleSignalingMessage)
      }
    })

    // Cleanup
    onUnmounted(() => {
      stopContinuousCapture()
      cleanup()
      if (durationInterval.value) {
        clearInterval(durationInterval.value)
        durationInterval.value = null
      }
    })

    return {
      localVideo,
      hasGetUserMedia,
      error,
      stream,
      devices,
      currentDevice,
      connectionStatus,
      startCamera,
      stopCamera,
      switchCamera,
      handleDeviceChange,
      saveFrame,
      isSaving,
      fps,
      isContinuousCapture,
      framesSent,
      currentFps,
      toggleContinuousCapture,
      captureDuration,
      formatDuration,
      isFlipped
    }
  }
}
</script>

<style scoped>
.camera-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  height: 100%;
}

.video-wrapper {
  position: relative;
  width: 100%;
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 16/9;
  margin-bottom: 20px;
}

.video-wrapper.no-camera {
  border: 2px dashed #404040;
  background: #2d2d2d;
}

.camera-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.flip-horizontal {
  transform: scaleX(-1);
}

.camera-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  max-width: 300px;
}

.camera-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  color: #808080;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.placeholder-text {
  font-size: 18px;
  font-weight: 500;
  margin: 8px 0;
  color: #808080;
}

.placeholder-subtext {
  font-size: 14px;
  color: #808080;
  opacity: 0.8;
  margin: 0;
}

.camera-controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.controls-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.camera-select {
  width: 100%;
  padding: 12px;
  background: #2d2d2d;
  border: 1px solid #404040;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.camera-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.camera-select option {
  background: #2d2d2d;
  color: white;
  padding: 8px;
}

.fps-control {
  margin-bottom: 16px;
}

.control-label {
  display: block;
  font-size: 14px;
  margin-bottom: 8px;
  color: #FFFFFF;
}

.fps-input-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.fps-slider {
  flex: 1;
  height: 4px;
  background: #404040;
  border-radius: 2px;
  appearance: none;
}

.fps-slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  background: #2196F3;
  border-radius: 50%;
  cursor: pointer;
}

.fps-value {
  min-width: 60px;
  text-align: right;
  font-size: 14px;
  color: #FFFFFF;
}

.button-group {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.control-button {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
  min-width: 120px;
  transition: all 0.2s ease;
  background: #2196F3;
  color: white;
}

.control-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.control-button.start {
  background: #4CAF50;
}

.control-button.stop {
  background: #f44336;
}

.control-button.save {
  background: #4CAF50;
}

.control-button.recording {
  background: #f44336;
  animation: pulse 2s infinite;
}

.control-button.active {
  background: #1976D2;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
  100% {
    opacity: 1;
  }
}

.capture-stats {
  background: rgba(0, 0, 0, 0.5);
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 12px;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  color: #FFFFFF;
  opacity: 0.8;
}

.stat-value {
  font-size: 16px;
  font-weight: 500;
  color: #FFFFFF;
}

.error-message {
  color: #ff5252;
  background: rgba(255, 82, 82, 0.1);
  text-align: center;
  padding: 12px;
  border-radius: 8px;
  margin-top: 10px;
  border: 1px solid rgba(255, 82, 82, 0.2);
}

.hidden {
  display: none;
}

/* Light theme */
@media (prefers-color-scheme: light) {
  .video-wrapper {
    background: #f5f5f5;
  }

  .video-wrapper.no-camera {
    border-color: #e0e0e0;
    background: #fafafa;
  }

  .camera-select {
    background: white;
    border-color: #e0e0e0;
    color: #333;
  }

  .camera-select option {
    background: white;
    color: #333;
  }

  .camera-icon {
    color: #666;
  }
  
  .placeholder-text,
  .placeholder-subtext {
    color: #666;
  }

  .control-label,
  .fps-value,
  .stat-label,
  .stat-value {
    color: #333333;
  }

  .capture-stats {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #e0e0e0;
  }

  .fps-slider {
    background: #E0E0E0;
  }
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .camera-container {
    padding: 0;
    height: calc(100vh - 80px);
    display: flex;
    flex-direction: column;
  }

  .video-wrapper {
    flex: 1;
    margin: 0;
    border-radius: 0;
    aspect-ratio: auto;
    min-height: 0;
    max-height: calc(100vh - 140px);
  }

  .camera-preview {
    height: 100%;
    object-fit: cover;
  }

  .camera-controls {
    position: relative;
    background: rgba(0, 0, 0, 0.8);
    padding: 12px;
    width: 100%;
    margin: 0;
  }

  .controls-wrapper {
    max-width: 500px;
    margin: 0 auto;
    gap: 8px;
  }

  .camera-select {
    padding: 8px 12px;
    font-size: 14px;
    background: rgba(22, 22, 22, 0.8);
  }

  .button-group {
    gap: 8px;
  }

  .control-button {
    padding: 8px 12px;
    font-size: 14px;
    min-width: 100px;
  }

  .capture-stats {
    flex-direction: column;
    gap: 8px;
  }

  .stat-item {
    justify-content: space-between;
  }

  /* Light theme adjustments for mobile */
  @media (prefers-color-scheme: light) {
    .camera-controls {
      background: rgba(255, 255, 255, 0.9);
      border-top: 1px solid rgba(0, 0, 0, 0.1);
    }

    .camera-select {
      background: white;
      border-color: #e0e0e0;
      color: #333;
    }
  }
}

/* Handle iPhone notch and safe areas */
@supports (padding: max(0px)) {
  @media (max-width: 768px) {
    .camera-container {
      height: calc(100vh - 80px - env(safe-area-inset-top));
    }

    .video-wrapper {
      max-height: calc(100vh - 140px - env(safe-area-inset-top));
    }

    .camera-controls {
      padding-bottom: max(12px, env(safe-area-inset-bottom));
    }
  }
}
</style>