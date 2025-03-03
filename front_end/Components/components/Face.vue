<template>
  <div class="face-dashboard">
    <div class="face-container">
      <div class="layout-wrapper">
        <!-- Controls Section -->
        <div class="controls-section">
          <!-- Registration Section -->
          <transition name="fade">
            <div v-if="showRegistration" class="register-section">
              <div class="input-group">
                <input
                  v-model="registrationName"
                  type="text"
                  placeholder="Enter your name"
                  class="name-input"
                  @keypress.enter="handleRegistration"
                >
                <button
                  class="register-button"
                  :disabled="isRegistering"
                  @click="handleRegistration"
                >
                  <span v-if="isRegistering" class="loading-dots">
                    <span></span><span></span><span></span>
                  </span>
                  <span v-else>Register</span>
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- Camera Section -->
        <div class="camera-section">
          <div class="camera-view">
            <template v-if="isClient">
              <video ref="videoRef" autoplay playsinline></video>
              <canvas ref="canvasRef"></canvas>
            </template>
            
            <!-- Embedded Status Bar (Top Left) -->
            <div class="embedded-status-bar">
              <div class="title-section">
                <h2 class="title">Face Recognition</h2>
                <div class="connection-status">
                  <div :class="['status-indicator', wsConnectionStatus]"></div>
                  <span>{{ connectionStatusText }}</span>
                </div>
              </div>
            </div>
            
            <!-- Embedded Status Section (Top Right) -->
            <div class="embedded-status" :class="{ 'has-face': showRegistration }">
              <div class="detection-status">
                {{ detectionStatus }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Notification -->
      <transition name="notification">
        <div v-if="notificationState.show" 
             :class="['notification', notificationState.type]"
             role="alert">
          {{ notificationState.message }}
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted, onBeforeMount } from 'vue'
import services from '@/configs/services_info.json'

// Client-side detection
const isClient = ref(false)

onBeforeMount(() => {
  isClient.value = typeof window !== 'undefined'
})

// Reactive State
const state = reactive({
  wsConnected: false,
  processingRegistration: false,
  lastCapturedImage: null,
  detectionMessage: 'Initializing camera...',
  showRegisterForm: false
})

// Refs
const videoRef = ref(null)
const canvasRef = ref(null)
const registrationName = ref('')
const ws = ref()
const detectionInterval = ref(null)

// Computed Properties
const wsConnectionStatus = computed(() => state.wsConnected ? 'connected' : 'disconnected')
const connectionStatusText = computed(() => state.wsConnected ? 'Connected' : 'Connecting...')
const showRegistration = computed(() => state.showRegisterForm)
const isRegistering = computed(() => state.processingRegistration)
const detectionStatus = computed(() => state.detectionMessage)

// Notification State
const notificationState = reactive({
  show: false,
  message: '',
  type: 'info'
})

// Services configuration
const API_BASE_URL = services['svc-face']?.url || ''

// Methods
const showNotification = (message, type = 'error') => {
  notificationState.show = true
  notificationState.message = message
  notificationState.type = type
  
  setTimeout(() => {
    notificationState.show = false
  }, 3000)
}

const initCamera = async () => {
  if (!isClient.value || !videoRef.value) {
    return false
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 }
      }
    })
    
    if (videoRef.value) {
      videoRef.value.srcObject = stream
      await videoRef.value.play()
      return true
    }
    return false
  } catch (error) {
    showNotification("Camera access denied: " + (error?.message || 'Unknown error'))
    return false
  }
}

const connectWebSocket = () => {
  if (!isClient.value || !API_BASE_URL) {
    return
  }

  const wsUrl = `${API_BASE_URL.replace('http', 'ws')}/ws`
  
  try {
    ws.value = new WebSocket(wsUrl)

    ws.value.onopen = () => {
      state.wsConnected = true
      startDetection()
    }

    ws.value.onclose = () => {
      state.wsConnected = false
      if (detectionInterval.value) {
        clearInterval(detectionInterval.value)
        detectionInterval.value = null
      }
      setTimeout(connectWebSocket, 2000)
    }

    ws.value.onerror = (error) => {
      console.error('WebSocket error:', error)
      showNotification('Connection error')
    }

    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.error) {
          showNotification(data.error)
          return
        }

        if (data.faces && data.faces.length > 0) {
          const recognizedFaces = data.faces.filter(face => face.name !== 'Unknown')

          if (recognizedFaces.length > 0) {
            const names = recognizedFaces.map(face => face.name).join(', ')
            state.detectionMessage = `Welcome, ${names}!`
            state.showRegisterForm = false
          } else {
            state.detectionMessage = 'Face detected. Please register.'
            state.showRegisterForm = true
          }
        } else {
          state.detectionMessage = 'No face detected'
          state.showRegisterForm = false
        }
      } catch (err) {
        console.error('Error processing message:', err)
        showNotification('Error processing data')
      }
    }
  } catch (error) {
    console.error('WebSocket connection error:', error)
    showNotification('Failed to connect')
  }
}

const captureFrame = () => {
  if (!isClient.value || !videoRef.value || !canvasRef.value || !videoRef.value.videoWidth) {
    return null
  }

  try {
    const canvas = canvasRef.value
    canvas.width = videoRef.value.videoWidth
    canvas.height = videoRef.value.videoHeight
    
    const context = canvas.getContext('2d')
    if (!context) return null
    
    context.drawImage(videoRef.value, 0, 0, canvas.width, canvas.height)
    
    return canvas.toDataURL('image/jpeg', 0.8)
  } catch (error) {
    console.error('Error capturing frame:', error)
    return null
  }
}

const startDetection = () => {
  if (!isClient.value) return
  
  if (detectionInterval.value) {
    clearInterval(detectionInterval.value)
  }
  
  detectionInterval.value = setInterval(() => {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
      const frame = captureFrame()
      if (frame) {
        state.lastCapturedImage = frame
        ws.value.send(frame)
      }
    }
  }, 2000)
}

const handleRegistration = async () => {
  if (!isClient.value || !state.lastCapturedImage) {
    showNotification("No face captured")
    return
  }

  const name = registrationName.value.trim()
  if (!name) {
    showNotification("Please enter your name")
    return
  }

  state.processingRegistration = true

  try {
    const formData = new FormData()
    formData.append('image_data', state.lastCapturedImage)
    formData.append('name', name)

    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      body: formData
    })

    const data = await response.json()
    if (data.error) {
      showNotification(data.error)
    } else {
      showNotification(data.message || 'Registration successful', 'success')
      registrationName.value = ''
      state.showRegisterForm = false
    }
  } catch (error) {
    showNotification('Registration error: ' + (error?.message || 'Unknown error'))
  } finally {
    state.processingRegistration = false
  }
}

// Lifecycle hooks
onMounted(async () => {
  if (!isClient.value) return
  
  // Small delay to ensure DOM is fully rendered
  setTimeout(async () => {
    const cameraReady = await initCamera()
    if (cameraReady) {
      connectWebSocket()
    }
  }, 100)
})

onUnmounted(() => {
  if (!isClient.value) return
  
  if (detectionInterval.value) {
    clearInterval(detectionInterval.value)
    detectionInterval.value = null
  }

  if (ws.value) {
    ws.value.close()
    ws.value = null
  }

  if (videoRef.value?.srcObject) {
    const tracks = videoRef.value.srcObject.getTracks()
    if (tracks) {
      tracks.forEach(track => track.stop())
    }
  }
})
</script>

<style scoped>
/* Base layout and container queries setup */
.face-dashboard {
  height: 100%;
  padding: clamp(0.25rem, 1vw, 0.75rem);
  container-type: inline-size;
}

.face-container {
  height: 100%;
  background: rgba(15, 23, 42, 0.95);
  border-radius: clamp(0.75rem, 3vw, 1rem);
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(51, 65, 85, 0.5);
  overflow: hidden;
  position: relative;
  backdrop-filter: blur(0.75rem);
}

.layout-wrapper {
  display: grid;
  grid-template-rows: auto 1fr;
  height: 100%;
  gap: clamp(0.5rem, 2vw, 0.75rem);
  padding: clamp(0.5rem, 2vw, 0.75rem);
}

/* Controls section */
.controls-section {
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 2vw, 0.75rem);
  margin-top: 0.5rem;
}

/* Status area with grid layout */
.status-row {
  display: flex;
  gap: clamp(0.5rem, 2vw, 0.75rem);
  align-items: center;
}

.status-bar {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 0.75rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  padding: clamp(0.5rem, 2vw, 1rem);
}

/* Camera section with aspect ratio */
.camera-section {
  display: flex;
  flex-direction: column;
  min-height: 0;
  width: 100%;
}

.camera-view {
  position: relative;
  width: 100%;
  aspect-ratio: 4/3;
  background: #000;
  border-radius: 0.75rem;
  overflow: hidden;
  border: 1px solid rgba(51, 65, 85, 0.5);
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1); /* Flip camera horizontally by default */
}

canvas {
  display: none;
}

/* Typography and content */
.title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.title {
  font-size: clamp(0.875rem, 2.5vw, 1.125rem);
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
  text-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.3);
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
  color: #94a3b8;
  text-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.3);
}

.status-indicator {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background: #64748b;
  transition: all 0.3s ease;
}

.status-indicator.connected {
  background: #22c55e;
  box-shadow: 0 0 0 0.188rem rgba(34, 197, 94, 0.2);
  animation: pulse 2s infinite;
}

.status-indicator.disconnected {
  background: #ef4444;
}

.detection-status {
  text-align: center;
  font-size: clamp(0.875rem, 2.5vw, 1rem);
  font-weight: 500;
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
  letter-spacing: 0.01em;
  text-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.3);
}

/* Embedded status bar (top left) */
.embedded-status-bar {
  position: absolute;
  top: 1rem;
  left: 1rem;
  max-width: 60%;
  padding: clamp(0.5rem, 2vw, 0.75rem);
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(0.25rem);
  border-radius: 0.75rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  transition: all 0.3s ease;
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.2);
  z-index: 10;
}

/* Embedded status section (top right) */
.embedded-status {
  position: absolute;
  top: 1rem;
  right: 1rem;
  max-width: 60%;
  padding: clamp(0.5rem, 2vw, 0.75rem);
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(0.25rem);
  border-radius: 0.75rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  transition: all 0.3s ease;
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.embedded-status.has-face {
  background: rgba(59, 130, 246, 0.4);
  border-color: rgba(59, 130, 246, 0.5);
  box-shadow: 0 0 0.75rem rgba(59, 130, 246, 0.3);
}

/* Registration form */
.register-section {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 0.75rem;
  padding: clamp(0.5rem, 2vw, 0.75rem);
  border: 1px solid rgba(51, 65, 85, 0.5);
}

.input-group {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.name-input {
  flex: 1;
  min-width: 8rem;
  padding: 0.625rem 0.875rem;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(51, 65, 85, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  font-size: clamp(0.875rem, 2vw, 1rem);
  transition: all 0.2s ease;
  min-height: 2.75rem; /* 44px touch target */
}

.name-input::placeholder {
  color: #94a3b8;
}

.name-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.125rem rgba(59, 130, 246, 0.1);
}

.register-button {
  padding: 0.625rem 1rem;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: clamp(0.875rem, 2vw, 1rem);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 5.625rem;
  min-height: 2.75rem; /* 44px touch target */
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.register-button:hover:not(:disabled) {
  transform: translateY(-0.0625rem);
  box-shadow: 0 0.25rem 0.75rem rgba(59, 130, 246, 0.3);
}

.register-button:active:not(:disabled) {
  transform: scale(0.98);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Loading Animation */
.loading-dots {
  display: flex;
  align-items: center;
  gap: 0.188rem;
}

.loading-dots span {
  width: 0.188rem;
  height: 0.188rem;
  border-radius: 50%;
  background: currentColor;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

/* Notification */
.notification {
  position: absolute;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  padding: clamp(0.5rem, 2vw, 0.625rem) clamp(0.75rem, 3vw, 1rem);
  border-radius: 0.5rem;
  font-size: clamp(0.8125rem, 2vw, 0.875rem);
  font-weight: 500;
  animation: slideDown 0.3s ease;
  z-index: 100;
  max-width: 90%;
  text-align: center;
}

.notification.error {
  background: rgba(239, 68, 68, 0.9);
  color: white;
}

.notification.success {
  background: rgba(34, 197, 94, 0.9);
  color: white;
}

.notification.info {
  background: rgba(59, 130, 246, 0.9);
  color: white;
}

/* Animations */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
  70% { box-shadow: 0 0 0 0.25rem rgba(34, 197, 94, 0); }
  100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

@keyframes slideDown {
  from { transform: translate(-50%, -100%); opacity: 0; }
  to { transform: translate(-50%, 0); opacity: 1; }
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-0.625rem);
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -100%);
}

/* Container queries */
@container (max-width: 30rem) {
  .embedded-status, 
  .embedded-status-bar {
    max-width: 80%;
  }
  
  .title-section {
    justify-content: center;
  }
  
  .input-group {
    flex-direction: column;
  }
  
  .register-button {
    width: 100%;
  }
}

/* Media queries for device sizes */
@media (max-width: 30rem) {
  /* Extra small devices/phones */
  .face-dashboard {
    padding: 0.5rem;
  }
  
  .layout-wrapper {
    gap: 0.5rem;
    padding: 0.5rem;
  }
  
  .embedded-status-bar, 
  .embedded-status {
    padding: 0.375rem 0.5rem;
  }
  
  /* Stack the embedded elements on very small screens */
  .embedded-status-bar {
    top: 0.5rem;
    left: 0.5rem;
  }
  
  .embedded-status {
    top: 0.5rem;
    right: 0.5rem;
  }
}

@media (min-width: 30.0625rem) and (max-width: 48rem) {
  /* Small devices/tablets */
  .input-group {
    flex-wrap: nowrap;
  }
}

@media (min-width: 48.0625rem) and (max-width: 64rem) {
  /* Medium devices/desktops */
  .layout-wrapper {
    display: flex;
    flex-direction: column;
  }
  
  .controls-section {
    order: 2;
  }
  
  .camera-section {
    order: 1;
    flex: 1;
  }
  
  /* Allow embedded elements to be larger */
  .embedded-status-bar,
  .embedded-status {
    max-width: 40%;
  }
}

/* Accessibility enhancements */
@media (prefers-reduced-motion: reduce) {
  .status-indicator.connected {
    animation: none;
  }
  
  .fade-enter-active,
  .fade-leave-active,
  .notification-enter-active,
  .notification-leave-active {
    transition: opacity 0.1s linear;
  }
  
  .fade-enter-from,
  .fade-leave-to,
  .notification-enter-from,
  .notification-leave-to {
    transform: none;
  }
}

/* Light Mode Support */
@media (prefers-color-scheme: light) {
  .face-container {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .status-bar,
  .register-section {
    background: rgba(248, 250, 252, 0.8);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .embedded-status-bar {
    background: rgba(255, 255, 255, 0.7);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .embedded-status {
    background: rgba(255, 255, 255, 0.7);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .embedded-status.has-face {
    background: rgba(59, 130, 246, 0.2);
  }

  .title {
    color: #1e293b;
  }

  .detection-status {
    color: #1e293b;
    text-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1);
  }

  .name-input {
    background: white;
    color: #1e293b;
    border-color: rgba(226, 232, 240, 0.8);
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .face-container {
    background: white;
    border: 0.125rem solid black;
  }

  .status-bar,
  .register-section {
    background: white;
    border: 0.125rem solid black;
  }

  .embedded-status-bar {
    background: white;
    border: 0.125rem solid black;
    box-shadow: none;
  }

  .embedded-status {
    background: white;
    border: 0.125rem solid black;
    box-shadow: none;
  }

  .embedded-status.has-face {
    background: white;
    border: 0.125rem solid black;
    outline: 0.125rem solid black;
    box-shadow: none;
  }

  .title {
    color: black;
  }

  .detection-status {
    color: black;
    text-shadow: none;
  }

  .register-button {
    background: black;
    color: white;
  }

  .name-input {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }
}
</style>