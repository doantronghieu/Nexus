<template>
  <div class="unified-input-container" :class="{ 'processing': isProcessing }">
    <div class="input-section">
      <div class="text-input-container" 
           :class="{ 'recording': isRecording }"
           role="form"
           aria-label="Message input form">
        <!-- Control Group -->
        <div class="controls-wrapper">
          <!-- Voice Controls -->
          <div class="control-group" role="group" aria-label="Voice controls">
            <button
              class="control-button mic-button"
              :class="{ 'recording': isRecording }"
              @click="toggleRecording"
              :disabled="isProcessing"
              :aria-label="isRecording ? 'Stop recording' : 'Start recording'"
              :title="isRecording ? 'Stop recording' : 'Start recording'"
            >
              <div v-if="isRecording && recordingMode === 'timer'" class="recording-timer">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                <span>{{ (timeLeft / 1000).toFixed(1) }}s</span>
              </div>
              
              <span class="mic-wrapper" :class="{ pulse: isRecording }">
                <svg v-if="isRecording" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-pulse">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                  <line x1="12" y1="19" x2="12" y2="23"/>
                  <line x1="8" y1="23" x2="16" y2="23"/>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                  <line x1="12" y1="19" x2="12" y2="23"/>
                  <line x1="8" y1="23" x2="16" y2="23"/>
                </svg>
              </span>
              
              <template v-if="isRecording">
                <div class="recording-visualizer">
                  <div class="visualizer-bar" v-for="n in 4" :key="n"></div>
                </div>
              </template>
            </button>
            <div v-if="hasAudioRecording"
                 class="input-indicator"
                 @click="showAudioPreview"
                 role="button"
                 aria-label="Show audio preview"
                 title="Show audio preview">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 18V5l12-2v13"/>
                <circle cx="6" cy="18" r="3"/>
                <circle cx="18" cy="16" r="3"/>
              </svg>
            </div>
          </div>

          <!-- Wake Word -->
          <div class="control-group" role="group" aria-label="Wake word controls">
            <button
              class="control-button wake-word-button"
              :class="{ 'active': isWakeWordEnabled }"
              @click="toggleWakeWord"
              :aria-label="isWakeWordEnabled ? 'Disable wake word' : 'Enable wake word'"
              :title="isWakeWordEnabled ? 'Disable wake word' : 'Enable wake word'"
            >
              <span class="wake-word-icon" aria-hidden="true">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M2 12h4c1.1 0 2-.9 2-2s-.9-2-2-2H2v4z"/>
                  <path d="M8.5 12h4c1.1 0 2-.9 2-2s-.9-2-2-2h-4v4z"/>
                  <path d="M15 12h4c1.1 0 2-.9 2-2s-.9-2-2-2h-4v4z"/>
                  <line x1="2" y1="16" x2="22" y2="16"/>
                  <line x1="2" y1="8" x2="22" y2="8"/>
                </svg>
              </span>
              <span class="badge" v-if="isWakeWordEnabled">ON</span>
            </button>
          </div>

          <!-- Image Upload -->
          <div class="control-group" role="group" aria-label="Image upload controls">
            <button
              class="control-button upload-button"
              @click="triggerFileInput"
              aria-label="Upload image"
              title="Upload image"
            >
              <span class="upload-icon" aria-hidden="true">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <polyline points="21 15 16 10 5 21"/>
                </svg>
              </span>
            </button>
            <input
              ref="fileInput"
              type="file"
              accept="image/jpeg,image/png,image/gif"
              class="hidden"
              @change="handleFileSelect"
              aria-label="Image file input"
            />
            <div v-if="hasImage"
                 class="input-indicator"
                 @click="showImagePreview"
                 role="button"
                 aria-label="Show image preview"
                 title="Show image preview">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
              </svg>
            </div>
          </div>

          <!-- Divider -->
          <div class="control-divider"></div>

          <!-- Settings -->
          <div class="control-group" role="group" aria-label="Settings controls">
            <button
              class="control-button settings-button"
              :class="{ 'active': showSettingsModal }"
              @click="toggleSettings"
              aria-label="Open settings"
              title="Open settings"
            >
              <span class="settings-icon" aria-hidden="true">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </span>
            </button>
          </div>
        </div>

        <!-- Text Input -->
        <div class="input-wrapper">
          <input
            v-model="inputText"
            type="text"
            class="text-input"
            placeholder="Type your message..."
            :disabled="isRecording || isProcessing"
            @input="handleTextInput"
            @keyup.enter="sendMessage"
            aria-label="Message input"
          />
          <div v-if="inputText" class="clear-input" @click="clearInput">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
          </div>
        </div>

        <!-- Send Button -->
        <button
          class="send-button"
          :disabled="!canSend"
          @click="sendMessage"
          aria-label="Send message"
        >
          <span v-if="isProcessing" class="loading-dot-container" aria-label="Processing">
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
          </span>
          <span v-else-if="showSuccess" class="success-icon" aria-label="Message sent">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </span>
          <span v-else aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </span>
        </button>
      </div>
    </div>

    <!-- Preview Modal -->
    <Transition name="modal">
      <div v-if="showPreviewModal"
           class="modal-overlay"
           @click.self="closePreview"
           role="dialog"
           aria-modal="true"
           :aria-label="previewType === 'audio' ? 'Audio preview' : 'Image preview'">
        <div class="modal-content"
             role="document">
          <button class="modal-close"
                  @click="closePreview"
                  aria-label="Close preview">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
          
          <!-- Audio Preview -->
          <div v-if="previewType === 'audio'"
               class="audio-preview"
               role="region"
               aria-label="Audio player">
            <div class="audio-content">
              <audio
                controls
                :src="audioPreviewUrl"
                :type="audioMimeType"
                @error="handleAudioError"
              ></audio>
              <div v-if="audioPreviewError"
                   class="error-message"
                   role="alert">
                {{ audioPreviewError }}
              </div>
            </div>
          </div>
          
          <!-- Image Preview -->
          <div v-if="previewType === 'image'"
               class="image-preview"
               role="region"
               aria-label="Image preview">
            <div class="image-wrapper">
              <img :src="imagePreviewUrl"
                   alt="Preview"
                   @load="handleImageLoad"/>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Error Messages -->
    <Transition name="fade">
      <div v-if="errorMessage" 
           class="error-message"
           role="alert">
        <div class="error-content">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <span>{{ errorMessage }}</span>
          <button @click="dismissError" class="dismiss-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>

    <!-- Settings Modal -->
    <Transition name="modal">
      <div v-if="showSettingsModal"
           class="modal-overlay"
           @click.self="toggleSettings"
           role="dialog"
           aria-modal="true"
           aria-label="Recording settings">
        <div class="modal-content settings-modal">
          <button class="modal-close"
                  @click="toggleSettings"
                  aria-label="Close settings">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>

          <h2 class="settings-title">Recording Settings</h2>
          
          <div class="settings-section">
            <h3>Recording Mode</h3>
            <div class="settings-options">
              <label class="option">
                <input type="radio"
                       v-model="recordingMode"
                       value="timer"
                       @change="updateRecordingMode('timer')"
                />
                <span>Timer Mode</span>
              </label>
              <label class="option">
                <input type="radio"
                       v-model="recordingMode"
                       value="silence"
                       @change="updateRecordingMode('silence')"
                />
                <span>Silence Detection</span>
              </label>
            </div>
          </div>

          <div class="settings-section" v-if="recordingMode === 'timer'">
            <h3>Timer Duration</h3>
            <div class="settings-slider">
              <input type="range"
                     min="1"
                     max="10"
                     step="1"
                     :value="timerDuration / 1000"
                     @input="updateTimerDuration($event.target.value)"
              />
              <span>{{ timerDuration / 1000 }}s</span>
            </div>
          </div>

          <div class="settings-section" v-if="recordingMode === 'silence'">
            <h3>Silence Duration</h3>
            <div class="settings-slider">
              <input type="range"
                     min="1"
                     max="5"
                     step="0.5"
                     :value="silenceDuration / 1000"
                     @input="updateSilenceDuration($event.target.value)"
              />
              <span>{{ silenceDuration / 1000 }}s</span>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import services from '@/configs/services_info_p3.json'

// State
const inputText = ref('')
const isRecording = ref(false)
const isProcessing = ref(false)
const isWakeWordEnabled = ref(false)
const errorMessage = ref('')
const fileInput = ref(null)
const showSuccess = ref(false)
const showSettingsModal = ref(false)

// Computed property to determine if message can be sent
const canSend = computed(() => {
  return (inputText.value.trim() || hasAudioRecording.value || hasImage.value) && !isProcessing.value && !isRecording.value
})

// Recording Settings
const recordingMode = ref('timer') // 'timer' or 'silence'
const timerDuration = ref(5000) // 5 seconds default
const silenceDuration = ref(2000) // 2 seconds default
const timeLeft = ref(0)
const timerInterval = ref(null)

// Settings Methods
const toggleSettings = () => {
  showSettingsModal.value = !showSettingsModal.value
}

const updateRecordingMode = (mode) => {
  recordingMode.value = mode
}

const updateTimerDuration = (duration) => {
  timerDuration.value = duration * 1000 // Convert to milliseconds
}

const updateSilenceDuration = (duration) => {
  silenceDuration.value = duration * 1000 // Convert to milliseconds
  wakeWordConfig.MIN_SILENCE_DURATION = silenceDuration.value
}

const startTimer = () => {
  timeLeft.value = timerDuration.value
  timerInterval.value = setInterval(() => {
    timeLeft.value -= 100 // Update every 100ms
    if (timeLeft.value <= 0) {
      stopRecording()
      clearInterval(timerInterval.value)
    }
  }, 100)
}

const stopTimer = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
  timeLeft.value = 0
}

// Server configuration
const P3_URL = `${services['app-llm'].url}/agent`
const STT_URL = `${services['svc-stt'].url}/api/v1/transcribe`

// Preview State
const showPreviewModal = ref(false)
const previewType = ref(null)
const imagePreviewUrl = ref(null)
const audioPreviewUrl = ref(null)
const hasImage = ref(false)
const hasAudioRecording = ref(false)
const audioMimeType = ref('')
const audioPreviewError = ref('')

// Audio Processing
const mediaRecorder = ref(null)
const audioChunks = ref([])

// Audio Error Handling
const handleAudioError = (event, isPreview = false) => {
  console.error('Audio error:', event)
  if (isPreview) {
    audioPreviewError.value = 'Failed to play audio preview. Please try recording again.'
  } else {
    errorMessage.value = 'Error playing audio notification'
  }
}

// Preview Methods
const showImagePreview = () => {
  previewType.value = 'image'
  showPreviewModal.value = true
}

const showAudioPreview = () => {
  if (!audioPreviewUrl.value) {
    errorMessage.value = 'No audio recording available'
    return
  }
  
  audioPreviewError.value = ''
  previewType.value = 'audio'
  showPreviewModal.value = true
}

const closePreview = () => {
  showPreviewModal.value = false
  previewType.value = null
}

// Image handling method
const handleImageLoad = (event) => {
  const img = event.target
  const naturalRatio = img.naturalWidth / img.naturalHeight
  
  const imageWrapper = img.parentElement
  if (naturalRatio > 1) {
    imageWrapper.style.width = '90vw'
    imageWrapper.style.height = 'auto'
  } else {
    imageWrapper.style.width = 'auto'
    imageWrapper.style.height = '90vh'
  }
}

// Text Input Methods
const handleTextInput = () => {
  errorMessage.value = ''
  showSuccess.value = false
}

const clearInput = () => {
  inputText.value = ''
}

const dismissError = () => {
  errorMessage.value = ''
}

const emit = defineEmits(['messageSent'])

const sendMessage = async () => {
  if (!canSend.value) return

  isProcessing.value = true
  showSuccess.value = false
  errorMessage.value = ''

  try {
    emit('messageSent') // Emit event before sending
    
    const response = await fetch(P3_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: inputText.value
      })
    })

    if (!response.ok) {
      throw new Error('Failed to send message')
    }

    await response.json()
    showSuccess.value = true
    inputText.value = ''
    
    setTimeout(() => {
      showSuccess.value = false
    }, 2000)
  } catch (error) {
    errorMessage.value = error.message || 'Failed to communicate with vehicle agent'
    console.error('Vehicle Agent Error:', error)
  } finally {
    isProcessing.value = false
  }
}

// Audio Processing

// Wake Word Methods
const socket = ref(null)
const audioAccumulator = ref([])
const wakeWordAudio = ref(null)
const finishTranscribeAudio = ref(null)
const silenceStartTime = ref(null)
const audioContext = ref(null)
const processor = ref(null)
const WWD_URL = services['svc-wwd'].url
const wakeWordConfig = {
  SAMPLE_RATE: 16000,
  CHUNK_SIZE: 1280,
  WEBSOCKET_URL: WWD_URL.replace('http', 'ws') + '/ws',
  SILENCE_THRESHOLD: 0.005,
  MIN_SILENCE_DURATION: 2000  // 2 seconds
}

const playSound = async (audioElement) => {
  if (audioElement) {
    try {
      audioElement.currentTime = 0
      await audioElement.play()
    } catch (error) {
      handleAudioError(error)
    }
  }
}

const connectWebSocket = () => {
  if (socket.value) {
    socket.value.close()
  }

  socket.value = new WebSocket(wakeWordConfig.WEBSOCKET_URL)
  
  socket.value.onopen = () => {
    console.log('WebSocket connected to wake word service')
  }
  
  socket.value.onmessage = async (event) => {
    try {
      const data = JSON.parse(event.data)
      
      if (data.type === 'result' && data.data.wake_word_detected) {
        // Wake word detected
        await playSound(wakeWordAudio.value)
        startRecording() // Auto start recording for speech-to-text
      }
    } catch (error) {
      console.error('Error processing WebSocket message:', error)
    }
  }
  
  socket.value.onclose = () => {
    console.log('WebSocket disconnected, attempting to reconnect...')
    setTimeout(connectWebSocket, 2000)
  }

  socket.value.onerror = (error) => {
    console.error('WebSocket error:', error)
    errorMessage.value = 'Error connecting to wake word service'
  }
}

const sendAudioChunk = (chunk) => {
  if (socket.value?.readyState === WebSocket.OPEN) {
    try {
      socket.value.send(chunk.buffer)
    } catch (error) {
      console.error('Error sending audio chunk:', error)
    }
  }
}

const processAudioForSilence = (inputData) => {
  // Only process silence detection in silence mode
  if (recordingMode.value !== 'silence') return false

  // Calculate RMS volume
  const rms = Math.sqrt(inputData.reduce((acc, val) => acc + val * val, 0) / inputData.length)
  
  if (rms < wakeWordConfig.SILENCE_THRESHOLD) {
    if (!silenceStartTime.value) {
      silenceStartTime.value = Date.now()
    } else if (Date.now() - silenceStartTime.value > silenceDuration.value) {
      stopRecording()
      return true
    }
  } else {
    silenceStartTime.value = null
  }
  return false
}

const startWakeWordDetection = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: wakeWordConfig.SAMPLE_RATE,
        channelCount: 1
      }
    })

    audioContext.value = new AudioContext({ sampleRate: wakeWordConfig.SAMPLE_RATE })
    const source = audioContext.value.createMediaStreamSource(stream)
    processor.value = audioContext.value.createScriptProcessor(2048, 1, 1)
    
    processor.value.onaudioprocess = (e) => {
      const inputData = e.inputBuffer.getChannelData(0)
      const int16Data = new Int16Array(inputData.length)
      
      for (let i = 0; i < inputData.length; i++) {
        int16Data[i] = Math.max(-32768, Math.min(32767, Math.floor(inputData[i] * 32768)))
      }
      
      audioAccumulator.value.push(...int16Data)
      
      if (isRecording.value) {
        processAudioForSilence(inputData)
      }
      
      while (audioAccumulator.value.length >= wakeWordConfig.CHUNK_SIZE) {
        const chunk = new Int16Array(
          audioAccumulator.value.slice(0, wakeWordConfig.CHUNK_SIZE)
        )
        audioAccumulator.value = audioAccumulator.value.slice(
          wakeWordConfig.CHUNK_SIZE
        )
        sendAudioChunk(chunk)
      }
    }

    source.connect(processor.value)
    processor.value.connect(audioContext.value.destination)

  } catch (error) {
    console.error('Error starting wake word detection:', error)
    errorMessage.value = 'Error accessing microphone'
  }
}

const stopWakeWordDetection = () => {
  if (processor.value) {
    processor.value.disconnect()
    processor.value = null
  }
  if (audioContext.value) {
    audioContext.value.close()
    audioContext.value = null
  }
  if (socket.value) {
    socket.value.close()
    socket.value = null
  }
  audioAccumulator.value = []
}

const toggleWakeWord = () => {
  isWakeWordEnabled.value = !isWakeWordEnabled.value
  if (isWakeWordEnabled.value) {
    startWakeWordDetection()
    connectWebSocket()
  } else {
    stopWakeWordDetection()
  }
}

// Audio Methods
const getSupportedMimeType = () => {
  const types = ['audio/webm', 'audio/mp4', 'audio/ogg']
  return types.find(type => MediaRecorder.isTypeSupported(type)) || ''
}

const startRecording = async () => {
  try {
    // Clear any existing timer and audio URLs
    stopTimer()
    if (audioPreviewUrl.value) {
      URL.revokeObjectURL(audioPreviewUrl.value)
      audioPreviewUrl.value = null
    }
    
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    // Start timer if in timer mode
    if (recordingMode.value === 'timer') {
      startTimer()
    }
    
    const mimeType = getSupportedMimeType()
    if (!mimeType) {
      throw new Error('No supported audio MIME type found')
    }
    
    audioMimeType.value = mimeType
    const options = {
      mimeType,
      audioBitsPerSecond: 16000
    }
    
    mediaRecorder.value = new MediaRecorder(stream, options)
    audioChunks.value = []
    audioPreviewError.value = ''

    mediaRecorder.value.ondataavailable = (event) => {
      audioChunks.value.push(event.data)
    }

    mediaRecorder.value.onstop = async () => {
      isProcessing.value = true
      
      try {
        const audioBlob = new Blob(audioChunks.value, {
          type: audioMimeType.value
        })
        
        if (audioPreviewUrl.value) {
          URL.revokeObjectURL(audioPreviewUrl.value)
        }
        
        audioPreviewUrl.value = URL.createObjectURL(audioBlob)
        hasAudioRecording.value = true
    
        const formData = new FormData()
        formData.append('file', audioBlob, `recording.${audioMimeType.value.split('/')[1]}`)
        formData.append('model', 'openai_whisper')
        
        const response = await fetch(STT_URL, {
          method: 'POST',
          body: formData
        })
    
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'STT processing failed')
        }
    
        const result = await response.json()
        inputText.value = result.text
        
        // Play transcription complete sound
        await playSound(finishTranscribeAudio.value)
        
        // Auto send message after a short delay
        setTimeout(() => {
          if (inputText.value.trim()) {
            sendMessage()
          }
        }, 1000)
        
      } catch (error) {
        errorMessage.value = error.message || 'Failed to process speech'
        console.error('STT Error:', error)
      } finally {
        isProcessing.value = false
      }
    }

    mediaRecorder.value.start(100)
    isRecording.value = true
    hasAudioRecording.value = false
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = 'Microphone access denied'
    console.error('Error accessing microphone:', error)
  }
}

const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
    isRecording.value = false
    
    mediaRecorder.value.stream.getTracks().forEach(track => track.stop())
  }
}

const toggleRecording = () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

// Image Upload Methods
const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  processImageFile(file)
}

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    processImageFile(file)
  } else {
    errorMessage.value = 'Please drop an image file'
  }
}

const processImageFile = (file) => {
  if (file && file.type.startsWith('image/')) {
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreviewUrl.value = e.target.result
      hasImage.value = true
      errorMessage.value = ''
    }
    reader.readAsDataURL(file)
  } else {
    errorMessage.value = 'Invalid file type'
  }
}

const handleKeydown = (e) => {
  // If the space key is pressed while the input is focused,
  // stop the event from propagating
  if (e.code === 'Space' && 
     (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
    e.stopPropagation(); // This prevents the event from reaching the music component
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
  
  // Initialize wake word and transcribe complete audio
  wakeWordAudio.value = new Audio('/sounds/wake-word-detected.wav');
  finishTranscribeAudio.value = new Audio('/sounds/finished-transcribed.wav');
  
  // Add error handlers for audio elements
  wakeWordAudio.value.addEventListener('error', e => handleAudioError(e, false));
  finishTranscribeAudio.value.addEventListener('error', e => handleAudioError(e, false));

  // Update audio element reference in audio preview
  const audioElement = document.querySelector('audio');
  if (audioElement) {
    audioElement.addEventListener('error', e => handleAudioError(e, true));
  }
});

// Cleanup
onBeforeUnmount(() => {
  // Stop any active recording
  if (isRecording.value) {
    stopRecording()
  }

  // Stop wake word detection
  if (isWakeWordEnabled.value) {
    stopWakeWordDetection()
  }

  // Clean up audio elements
  if (wakeWordAudio.value) {
    wakeWordAudio.value.pause()
    wakeWordAudio.value.src = ''
  }
  if (finishTranscribeAudio.value) {
    finishTranscribeAudio.value.pause()
    finishTranscribeAudio.value.src = ''
  }

  // Clean up URLs
  if (audioPreviewUrl.value) {
    URL.revokeObjectURL(audioPreviewUrl.value)
  }
  if (imagePreviewUrl.value && imagePreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(imagePreviewUrl.value)
  }

  // Remove event listeners
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.unified-input-container {
  width: 100%;
  padding: 1.25rem;
  background: rgba(30, 41, 59, 0.95);
  border-radius: 1.5rem;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(0.75rem);
  border: 1px solid rgba(51, 65, 85, 0.5);
  position: relative;
}

.text-input-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 1rem;
  padding: 0.75rem 1rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(51, 65, 85, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.text-input-container:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.1);
}

.text-input-container.recording {
  border-color: #ef4444;
  box-shadow: 0 0 0 0.25rem rgba(239, 68, 68, 0.1);
  background: rgba(15, 23, 42, 0.8);
}

.controls-wrapper {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.control-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper {
  flex: 1;
  min-width: 0;
  position: relative;
}

.text-input {
  width: 100%;
  padding: 0.875rem 2.5rem 0.875rem 1rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  border-radius: 0.875rem;
  font-size: 1rem;
  font-weight: 500;
  color: #e2e8f0;
  background: rgba(15, 23, 42, 0.6);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 3.5rem; /* 56px touch target */
}

.text-input::placeholder {
  color: #94a3b8;
  opacity: 0.8;
}

.text-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.text-input:disabled {
  background: rgba(15, 23, 42, 0.4);
  cursor: not-allowed;
}

.clear-input {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  transition: all 0.2s ease;
}

.clear-input:hover {
  opacity: 1;
  transform: translateY(-50%) scale(1.1);
}

.clear-input svg {
  width: 100%;
  height: 100%;
}

.control-button {
  width: 3.5rem;
  height: 3.5rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  border-radius: 0.875rem;
  background: rgba(30, 41, 59, 0.5);
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  position: relative;
}

.control-button:hover:not(:disabled) {
  background: rgba(51, 65, 85, 0.6);
  color: #e2e8f0;
  transform: translateY(-0.0625rem);
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
}

.control-button:active:not(:disabled) {
  transform: translateY(0);
}

.control-button svg {
  width: 1.5rem;
  height: 1.5rem;
}

.control-button.recording {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.control-button.wake-word-button.active {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.3);
}

.badge {
  position: absolute;
  top: -0.25rem;
  right: -0.25rem;
  background: #3b82f6;
  color: white;
  font-size: 0.625rem;
  font-weight: 700;
  padding: 0.125rem 0.375rem;
  border-radius: 9999px;
  border: 2px solid rgba(15, 23, 42, 0.9);
}

.mic-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: transparent;
  transition: all 0.3s ease;
}

.mic-wrapper.pulse {
  animation: mic-pulse 2s infinite;
}

@keyframes mic-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  70% {
    box-shadow: 0 0 0 0.625rem rgba(239, 68, 68, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}

.recording-visualizer {
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 0.5rem;
  gap: 0.125rem;
}

.visualizer-bar {
  width: 0.25rem;
  background: #ef4444;
  border-radius: 0.125rem;
  animation: sound 1.5s ease-in-out infinite;
}

.visualizer-bar:nth-child(1) {
  height: 0.375rem;
  animation-delay: 0.2s;
}

.visualizer-bar:nth-child(2) {
  height: 0.625rem;
  animation-delay: 0.6s;
}

.visualizer-bar:nth-child(3) {
  height: 0.375rem;
  animation-delay: 0.3s;
}

.visualizer-bar:nth-child(4) {
  height: 0.5rem;
  animation-delay: 0.5s;
}

@keyframes sound {
  0%, 100% {
    transform: scaleY(0.8);
  }
  50% {
    transform: scaleY(1.5);
  }
}

.send-button {
  padding: 0.875rem;
  border: none;
  border-radius: 0.875rem;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 3.5rem;
  height: 3.5rem;
  box-shadow: 0 0.25rem 0.75rem rgba(59, 130, 246, 0.2);
}

.send-button:hover:not(:disabled) {
  transform: translateY(-0.0625rem);
  box-shadow: 0 0.375rem 1rem rgba(59, 130, 246, 0.3);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
}

.send-button:disabled {
  background: #64748b;
  cursor: not-allowed;
  opacity: 0.7;
}

.send-button svg {
  width: 1.5rem;
  height: 1.5rem;
}

.input-indicator {
  position: absolute;
  top: -0.5rem;
  right: -0.5rem;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0.125rem 0.625rem rgba(59, 130, 246, 0.3);
  padding: 0.375rem;
}

.input-indicator:hover {
  transform: scale(1.15);
}

.input-indicator svg {
  width: 100%;
  height: 100%;
  min-width: 1.25rem;
  min-height: 1.25rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(0.75rem);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-content {
  background: rgba(30, 41, 59, 0.95);
  padding: 2rem;
  border-radius: 1.25rem;
  position: relative;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(51, 65, 85, 0.5);
  width: min(90%, 60rem);
  height: auto;
  max-height: 85vh;
  aspect-ratio: 16/9;
  margin: auto;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.modal-close {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  width: 3rem;
  height: 3rem;
  border: none;
  background: rgba(15, 23, 42, 0.9);
  color: white;
  border-radius: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 1100;
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.2);
}

.modal-close:hover {
  background: rgb(15, 23, 42);
  transform: scale(1.05);
}

.modal-close svg {
  width: 1.25rem;
  height: 1.25rem;
}

.image-preview {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.image-wrapper {
  width: auto;
  height: auto;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 0.5rem;
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.08);
}

.audio-preview {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.audio-content {
  width: 100%;
  max-width: 31.25rem;
  min-width: 18.75rem;
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 1rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
}

.audio-preview audio {
  width: 100%;
  height: 3rem;
  border-radius: 0.5rem;
  background: rgba(30, 41, 59, 0.9);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
}

.error-message {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10000;
  animation: slideUp 0.3s ease-out forwards;
  width: max-content;
  max-width: 90vw;
}

.error-content {
  background: rgba(239, 68, 68, 0.9);
  color: white;
  padding: 1rem 3rem 1rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  backdrop-filter: blur(0.25rem);
  box-shadow: 0 0.25rem 1rem rgba(239, 68, 68, 0.3);
  position: relative;
}

.dismiss-button {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: white;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.dismiss-button:hover {
  opacity: 1;
}

.dismiss-button svg {
  width: 1rem;
  height: 1rem;
}

.error-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

/* Recording Timer */
.recording-timer {
  position: absolute;
  top: -2.75rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 23, 42, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  color: #e2e8f0;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(0.5rem);
  z-index: 10;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.recording-timer svg {
  width: 1rem;
  height: 1rem;
  color: #ef4444;
  animation: pulse 2s infinite;
}

/* Animations */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  70% { box-shadow: 0 0 0 0.375rem rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translate(-50%, 1rem); }
  to { opacity: 1; transform: translate(-50%, 0); }
}

/* Loading animation */
.loading-dot-container {
  display: flex;
  gap: 0.25rem;
  align-items: center;
  height: 1.5rem;
}

.loading-dot {
  width: 0.375rem;
  height: 0.375rem;
  background: currentColor;
  border-radius: 50%;
  opacity: 0.8;
  animation: loading-dot 1.4s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes loading-dot {
  0%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-0.5rem);
    opacity: 1;
  }
}

/* Settings Modal and Timer Styles */
.settings-modal {
  max-width: 31.25rem;
  padding: 2rem;
}

.settings-title {
  color: #e2e8f0;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
}

.settings-section {
  margin-bottom: 2rem;
}

.settings-section h3 {
  color: #e2e8f0;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.settings-options {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e2e8f0;
  cursor: pointer;
}

.settings-slider {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.settings-slider input[type="range"] {
  flex: 1;
  height: 0.25rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 0.125rem;
  -webkit-appearance: none;
}

.settings-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 1rem;
  height: 1rem;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-slider input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  background: #2563eb;
}

.settings-slider span {
  color: #e2e8f0;
  min-width: 3rem;
  text-align: right;
}

.control-divider {
  width: 0.0625rem;
  height: 1.5rem;
  background: rgba(51, 65, 85, 0.5);
  margin: 0 0.5rem;
}

.settings-button {
  position: relative;
}

.settings-button.active {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.3);
}

/* Radio button styling */
.option input[type="radio"] {
  -webkit-appearance: none;
  appearance: none;
  width: 1.15em;
  height: 1.15em;
  border: 0.15em solid #94a3b8;
  border-radius: 50%;
  margin: 0;
  display: grid;
  place-content: center;
  cursor: pointer;
}

.option input[type="radio"]::before {
  content: "";
  width: 0.65em;
  height: 0.65em;
  border-radius: 50%;
  transform: scale(0);
  transition: transform 0.2s ease-in-out;
  background-color: #3b82f6;
}

.option input[type="radio"]:checked {
  border-color: #3b82f6;
}

.option input[type="radio"]:checked::before {
  transform: scale(1);
}

/* Success animation */
.success-icon {
  animation: success-pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes success-pop {
  0% {
    transform: scale(0.8);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Light Mode Support */
@media (prefers-color-scheme: light) {
  .unified-input-container {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .text-input-container {
    background: rgba(248, 250, 252, 0.8);
  }

  .text-input {
    color: #1e293b;
    background: white;
  }

  .text-input::placeholder {
    color: #64748b;
  }

  .text-input:focus {
    background: white;
  }

  .control-button {
    background: rgba(241, 245, 249, 0.8);
    color: #64748b;
  }

  .control-button:hover:not(:disabled) {
    background: rgba(226, 232, 240, 0.9);
    color: #1e293b;
  }

  .modal-overlay {
    background: rgba(255, 255, 255, 0.2);
  }

  .modal-content {
    background: rgba(255, 255, 255, 0.95);
  }
  
  .settings-title, 
  .settings-section h3,
  .option,
  .settings-slider span {
    color: #1e293b;
  }
  
  .recording-timer {
    background: rgba(248, 250, 252, 0.9);
    color: #1e293b;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .unified-input-container {
    margin: clamp(0.5rem, 2vh, 1.5rem);
    padding: clamp(0.75rem, 2vh, 1.25rem);
  }

  .text-input-container {
    padding: clamp(0.5rem, 1.5vh, 0.75rem);
    gap: clamp(0.375rem, 1vw, 0.75rem);
  }

  .control-button {
    width: clamp(2.75rem, 8vw, 3.25rem);  /* Increased minimum touch target */
    height: clamp(2.75rem, 8vw, 3.25rem);
  }

  .control-button svg {
    width: clamp(1.125rem, 3vw, 1.5rem);
    height: clamp(1.125rem, 3vw, 1.5rem);
  }

  .send-button {
    min-width: clamp(2.75rem, 8vw, 3.25rem);  /* Match control button size */
    height: clamp(2.75rem, 8vw, 3.25rem);
    padding: clamp(0.5rem, 1.5vw, 0.875rem);
  }

  .send-button svg {
    width: clamp(1.125rem, 3vw, 1.5rem);
    height: clamp(1.125rem, 3vw, 1.5rem);
  }

  .modal-content {
    padding: clamp(1rem, 3vh, 2rem);
    width: min(95%, 40rem);
  }

  .modal-close {
    top: clamp(0.75rem, 2vh, 1.25rem);
    right: clamp(0.75rem, 2vh, 1.25rem);
    width: clamp(2.75rem, 8vw, 3.25rem);
    height: clamp(2.75rem, 8vw, 3.25rem);
  }

  .modal-close svg {
    width: clamp(1rem, 2.5vw, 1.25rem);
    height: clamp(1rem, 2.5vw, 1.25rem);
  }
}

@media (max-width: 480px) {
  .text-input-container {
    flex-direction: column;
    padding: clamp(0.5rem, 2vh, 0.75rem);
    gap: clamp(0.5rem, 2vh, 1rem);
  }

  .controls-wrapper {
    width: 100%;
    justify-content: space-between;
    margin-bottom: clamp(0.5rem, 2vh, 1rem);
    flex-wrap: wrap;
    gap: clamp(0.375rem, 1.5vw, 0.75rem);
  }

  .input-wrapper {
    width: 100%;
  }

  .text-input {
    padding: clamp(0.625rem, 2vh, 1rem);
    font-size: clamp(1rem, 4vw, 1.125rem);
    min-height: clamp(3rem, 10vh, 4rem);
  }

  .modal-content {
    padding: clamp(0.75rem, 3vh, 1.5rem);
    width: 95%;
    max-height: 90vh;
  }
  
  /* Ensure minimum touch target sizes on small screens */
  .control-button,
  .send-button,
  .modal-close {
    min-width: 3rem;
    min-height: 3rem;
  }
}

/* Touch Device Optimizations */
@media (hover: none) and (pointer: coarse) {
  .control-button,
  .send-button,
  .modal-close {
    min-height: 2.75rem;
    min-width: 2.75rem;
  }

  .text-input {
    font-size: 1rem;
    padding: 0.75rem 2.5rem 0.75rem 0.75rem;
  }

  .text-input-container {
    gap: 0.75rem;
    padding: 0.75rem;
  }
}

/* Focus styles for accessibility */
.control-button:focus-visible,
.send-button:focus-visible,
.modal-close:focus-visible {
  outline: none;
  box-shadow: 0 0 0 0.1875rem rgba(59, 130, 246, 0.5);
}

/* Hidden elements */
.hidden {
  display: none;
}

/* Improve modal content scrolling */
.modal-content {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  scrollbar-color: rgba(203, 213, 225, 0.4) transparent;
}

.modal-content::-webkit-scrollbar {
  width: 0.375rem;
}

.modal-content::-webkit-scrollbar-track {
  background: transparent;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: rgba(203, 213, 225, 0.4);
  border-radius: 0.1875rem;
}

/* Ensure image preview maintains aspect ratio */
.image-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 90vw;
  max-height: 90vh;
}

.image-wrapper img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* Prevent body scroll when modal is open */
.modal-open {
  overflow: hidden;
  padding-right: var(--scrollbar-width, 0);
}

/* Improve audio player styling */
.audio-preview audio {
  width: 100%;
  height: 3rem;
  border-radius: 0.5rem;
  background: rgba(30, 41, 59, 0.9);
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.05);
}

/* Error message animation */
.error-message {
  z-index: 1000;
  animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
  10%, 90% {
    transform: translate3d(-51%, 0, 0);
  }
  20%, 80% {
    transform: translate3d(-49%, 0, 0);
  }
  30%, 50%, 70% {
    transform: translate3d(-52%, 0, 0);
  }
  40%, 60% {
    transform: translate3d(-48%, 0, 0);
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .unified-input-container {
    background: white;
    border: 0.125rem solid black;
  }

  .text-input-container {
    background: white;
    border: 0.125rem solid black;
  }

  .text-input {
    background: white;
    color: black;
    border: 0.125rem solid black;
  }

  .control-button {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }

  .send-button {
    background: black;
    color: white;
    border: 0.125rem solid black;
  }

  .error-message {
    border: 0.125rem solid #ef4444;
    background: white;
    color: black;
  }
  
  .recording-timer {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }
  
  .modal-content {
    background: white;
    border: 0.125rem solid black;
  }
  
  .settings-title, 
  .settings-section h3,
  .option,
  .settings-slider span {
    color: black;
  }
}
</style>