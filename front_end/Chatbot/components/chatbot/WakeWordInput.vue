<template>
  <div class="relative group">
    <!-- Main Button -->
    <button
      @click="toggleWakeWordDetection"
      :class="[
        'text-white p-2 rounded-full hover:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200',
        isListening ? 'bg-red-600 animate-pulse' : 'bg-blue-600'
      ]"
      :title="isListening ? 'Stop Wake Word Detection' : 'Start Wake Word Detection'"
      :disabled="disabled"
    >
      <!-- Custom Wake Word Icon -->
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        class="h-6 w-6" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
      >
        <!-- Sound Wave Lines -->
        <path d="M12 4v16" />
        <path d="M8 8v8" />
        <path d="M16 8v8" />
        <path d="M4 12h2" />
        <path d="M18 12h2" />
        <!-- Text Indicator (Hi) -->
        <path d="M20 6h1" />
        <path d="M20 4c0 1.5 -1.5 2 -1.5 2" />
      </svg>

      <!-- Alternative Icon Design Option -->
      <!-- <svg 
        xmlns="http://www.w3.org/2000/svg" 
        class="h-6 w-6" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="2"
      >
        <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <path d="M12 18.5v.5" />
        <path d="M10 3.5c4 2 4 2 4 0" />
        <path d="M8 6.5c8 3 8 3 8 0" />
      </svg> -->

      <!-- Animated Wave Circles when listening -->
      <div 
        v-if="isListening" 
        class="absolute inset-0 flex items-center justify-center"
        aria-hidden="true"
      >
        <div v-for="i in 3" :key="i"
             class="absolute inset-0 rounded-full border-2 border-white opacity-75 wave-circle"
             :style="{ animationDelay: `${i * 0.3}s` }"
        ></div>
      </div>
    </button>

    <!-- Full Screen Wake Word Alert Overlay -->
    <transition
      enter-active-class="transition duration-500 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="showWakeWordAlert"
        class="fixed inset-0 flex items-center justify-center z-50"
      >
        <!-- Animated Backdrop -->
        <div class="absolute inset-0 bg-gradient-to-r from-gray-900/95 to-black/95 backdrop-blur-md">
          <!-- Floating Particles Background -->
          <div v-for="i in 20" :key="i"
              class="particle absolute w-1 h-1 bg-blue-500/30 rounded-full"
              :style="{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`
              }"
          ></div>
        </div>

        <!-- Main Content Container - Moved up with margin-top-negative -->
        <div class="relative z-10 flex flex-col items-center -mt-20">
          <!-- Tech Circle Interface -->
          <div class="relative mb-8"> <!-- Added margin-bottom -->
            <!-- Outer Rotating Ring -->
            <div class="absolute -inset-4 border-2 border-blue-500/30 rounded-full tech-ring"></div>
            
            <!-- Scanner Line Effect -->
            <div class="absolute inset-0 overflow-hidden rounded-full">
              <div class="w-full h-[200%] scanner-line"></div>
            </div>

            <!-- Middle Hexagon Pattern -->
            <div class="absolute -inset-8">
              <svg class="w-full h-full animate-spin-slow" viewBox="0 0 100 100">
                <path
                  d="M50 0 L93.3 25 L93.3 75 L50 100 L6.7 75 L6.7 25 Z"
                  fill="none"
                  stroke="rgba(59, 130, 246, 0.2)"
                  stroke-width="0.5"
                />
              </svg>
            </div>

            <!-- Core Circle -->
            <div class="relative w-32 h-32 rounded-full bg-gradient-to-br from-blue-600 to-blue-900 
                        flex items-center justify-center shadow-2xl shadow-blue-500/50
                        border border-blue-400/30 backdrop-blur-xl">
              
              <!-- Holographic Wave Effect -->
              <div class="absolute inset-0 rounded-full hologram-effect"></div>

              <!-- Center Icon Container -->
              <div class="relative z-10 w-20 h-20 rounded-full bg-blue-900/50 
                          flex items-center justify-center border border-blue-400/30">
                <!-- AI Assistant Icon -->
                <svg 
                  class="w-12 h-12 text-blue-300 transform-gpu" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  stroke-width="1.5"
                >
                  <path class="tech-path" d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                  <path class="tech-path" d="M19 10v2a7 7 0 0 1-14 0v-2" />
                  <path class="tech-path" d="M12 18.5c4 0 7-1.5 7-4" />
                  <path class="tech-path" d="M5 14.5c0 2.5 3 4 7 4" />
                </svg>
              </div>
            </div>

            <!-- Orbiting Dots -->
            <div class="absolute inset-0 orbit-container">
              <div v-for="i in 8" :key="i"
                  class="orbit-dot"
                  :style="{ transform: `rotate(${i * 45}deg) translateX(72px)` }"
              ></div>
            </div>
          </div>

          <!-- Text Interface - Adjusted spacing -->
          <div class="space-y-6"> <!-- Increased vertical spacing -->
            <div class="relative inline-block">
              <h2 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r 
                        from-blue-400 to-blue-600 cyber-text tracking-wider">
                WAKE WORD DETECTED
              </h2>
              <!-- Glitch Effect Layers -->
              <h2 class="absolute top-0 left-0 text-3xl font-bold text-blue-500 
                        glitch-layer tracking-wider" aria-hidden="true">
                WAKE WORD DETECTED
              </h2>
              <h2 class="absolute top-0 left-0 text-3xl font-bold text-red-500 
                        glitch-layer-2 tracking-wider" aria-hidden="true">
                WAKE WORD DETECTED
              </h2>
            </div>

            <!-- Status Text -->
            <p class="text-lg text-blue-300/90 font-light tracking-wide typing-text">
              INITIALIZING VOICE INTERFACE...
            </p>

            <!-- Interactive Sound Wave - Moved up and adjusted size -->
            <div class="flex items-center justify-center space-x-0.5 h-6 mb-4"> <!-- Reduced height -->
              <div v-for="i in 12" :key="i"
                  class="w-0.5 rounded-full bg-gradient-to-t from-blue-600 to-blue-300 tech-wave"
                  :style="{
                    height: `${Math.sin((i / 12) * Math.PI) * 16 + 4}px`, // Reduced height
                    animationDelay: `${i * 0.1}s`
                  }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Hidden Audio Elements -->
    <audio 
      ref="wakeWordSound" 
      preload="auto"
      @error="handleAudioError"
    >
      <source :src="CONFIG.SOUNDS.WAKE_WORD_SOUND" type="audio/wav">
    </audio>
    <audio 
      ref="finishTranscribeSound" 
      preload="auto"
      @error="handleAudioError"
    >
      <source :src="CONFIG.SOUNDS.TRANSCRIBE_COMPLETE_SOUND" type="audio/wav">
    </audio>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useAIService } from '~/services/aiHandler'

// Centralized Configuration
const CONFIG = {
  SERVER: {
    BASE_URL: 'http://localhost:8000',
    WEBSOCKET_URL: 'ws://localhost:8000/ws',
    ENDPOINTS: {
      SET_MODE: '/set_mode',
      GET_MODE: '/get_mode'
    }
  },
  AUDIO: {
    SAMPLE_RATE: 16000,
    BUFFER_SIZE: 2048,
    CHUNK_SIZE: 1280
  },
  SOUNDS: {
    WAKE_WORD_SOUND: '/sounds/wake-word-detected.wav',
    TRANSCRIBE_COMPLETE_SOUND: '/sounds/finished-transcribed.wav'
  },
  UI: {
    ALERT_DURATION: 3000,
    RECORDING_DURATION: 5000,
    WEBSOCKET_RECONNECT_DELAY: 5000
  }
}

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send-message'])

// State
const isListening = ref(false)
const showWakeWordAlert = ref(false)
const audioContext = ref(null)
const processor = ref(null)
const socket = ref(null)
const audioAccumulator = ref([])
const alertTimeout = ref(null)

// Audio elements
const wakeWordSound = ref(null)
const finishTranscribeSound = ref(null)

// Initialize AI service
const aiService = useAIService()

// Sound playback helper
const playSound = (audioElement) => {
  if (audioElement) {
    audioElement.currentTime = 0
    audioElement.play().catch(error => {
      console.error('Error playing sound:', error)
    })
  }
}

// WebSocket handlers
const connectWebSocket = () => {
  socket.value = new WebSocket(CONFIG.SERVER.WEBSOCKET_URL)
  
  socket.value.onopen = () => {
    console.log('WebSocket connected')
  }
  
  socket.value.onmessage = async (event) => {
    const data = JSON.parse(event.data)
    
    if (data.wake_word_detected) {
      showWakeWordAlert.value = true
      playSound(wakeWordSound.value)
      
      // Start recording for speech-to-text
      const audioStream = await startAudioCapture()
      if (audioStream) {
        processAudioForSTT(audioStream)
      }
      
      if (alertTimeout.value) {
        clearTimeout(alertTimeout.value)
      }
      
      alertTimeout.value = setTimeout(() => {
        showWakeWordAlert.value = false
      }, CONFIG.UI.ALERT_DURATION)
    }
  }
  
  socket.value.onclose = () => {
    console.log('WebSocket disconnected')
    setTimeout(connectWebSocket, CONFIG.UI.WEBSOCKET_RECONNECT_DELAY)
  }
}

// Audio processing
const startAudioCapture = async () => {
  try {
    return await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: CONFIG.AUDIO.SAMPLE_RATE,
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true
      }
    })
  } catch (error) {
    console.error('Error accessing microphone:', error)
    return null
  }
}

const processAudioForSTT = async (stream) => {
  let recordedChunks = []
  
  const mediaRecorder = new MediaRecorder(stream)
  
  mediaRecorder.ondataavailable = async (event) => {
    if (event.data.size > 0) {
      recordedChunks.push(event.data)
    }
  }
  
  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(recordedChunks, { type: 'audio/wav' })
    try {
      // Play transcription complete sound
      playSound(finishTranscribeSound.value)
      
      // Transcribe audio
      const transcription = await aiService.transcribeAudio(audioBlob)
      if (transcription) {
        emit('send-message', transcription)
      }
    } catch (error) {
      console.error('Error processing audio:', error)
    }
  }
  
  // Record for specified duration after wake word detection
  mediaRecorder.start()
  setTimeout(() => {
    mediaRecorder.stop()
    stream.getTracks().forEach(track => track.stop())
  }, CONFIG.UI.RECORDING_DURATION)
}

const sendAudioChunk = (chunk) => {
  if (socket.value?.readyState === WebSocket.OPEN) {
    socket.value.send(chunk.buffer)
  }
}

const startListening = async () => {
  try {
    const stream = await startAudioCapture()
    if (!stream) return
    
    audioContext.value = new AudioContext({ sampleRate: CONFIG.AUDIO.SAMPLE_RATE })
    const source = audioContext.value.createMediaStreamSource(stream)
    processor.value = audioContext.value.createScriptProcessor(CONFIG.AUDIO.BUFFER_SIZE, 1, 1)
    
    processor.value.onaudioprocess = (e) => {
      const inputData = e.inputBuffer.getChannelData(0)
      const int16Data = new Int16Array(inputData.length)
      
      for (let i = 0; i < inputData.length; i++) {
        int16Data[i] = Math.max(-32768, Math.min(32767, Math.floor(inputData[i] * 32768)))
      }
      
      audioAccumulator.value.push(...int16Data)
      
      while (audioAccumulator.value.length >= CONFIG.AUDIO.CHUNK_SIZE) {
        const chunk = new Int16Array(audioAccumulator.value.slice(0, CONFIG.AUDIO.CHUNK_SIZE))
        audioAccumulator.value = audioAccumulator.value.slice(CONFIG.AUDIO.CHUNK_SIZE)
        sendAudioChunk(chunk)
      }
    }
    
    source.connect(processor.value)
    processor.value.connect(audioContext.value.destination)
    isListening.value = true
    
  } catch (error) {
    console.error('Error starting wake word detection:', error)
  }
}

const stopListening = () => {
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
  isListening.value = false
  showWakeWordAlert.value = false
  
  if (alertTimeout.value) {
    clearTimeout(alertTimeout.value)
  }
}

const toggleWakeWordDetection = () => {
  if (isListening.value) {
    stopListening()
  } else {
    startListening()
    connectWebSocket()
  }
}

const setServerMode = async () => {
  try {
    const response = await fetch(`${CONFIG.SERVER.BASE_URL}${CONFIG.SERVER.ENDPOINTS.SET_MODE}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ just_wwd: true })
    })
    if (!response.ok) {
      throw new Error('Failed to set WWD-only mode')
    }
    console.log('Server set to WWD-only mode')
  } catch (error) {
    console.error('Error setting WWD-only mode:', error)
  }
}

// Lifecycle hooks
onMounted(async () => {
  wakeWordSound.value = document.getElementById('wakeWordSound')
  finishTranscribeSound.value = document.getElementById('finishTranscribeSound')
  await setServerMode()
})

onBeforeUnmount(() => {
  stopListening()
})
</script>

<style scoped>
.wave-circle {
  animation: wave-out 2s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}

@keyframes wave-out {
  0% {
    transform: scale(0.5);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Tech Ring Rotation */
@keyframes tech-ring-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.tech-ring {
  animation: tech-ring-spin 10s linear infinite;
}

/* Scanner Effect */
@keyframes scanner {
  from { transform: translateY(-100%); }
  to { transform: translateY(100%); }
}

.scanner-line {
  background: linear-gradient(to bottom,
    transparent,
    rgba(59, 130, 246, 0.5),
    transparent
  );
  animation: scanner 2s ease-in-out infinite;
}

/* Hologram Effect */
@keyframes hologram {
  0% { opacity: 0.3; }
  50% { opacity: 0.5; }
  100% { opacity: 0.3; }
}

.hologram-effect {
  background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
  animation: hologram 2s ease-in-out infinite;
}

/* Tech Path Animation */
@keyframes tech-path {
  0% { stroke-dashoffset: 100; }
  100% { stroke-dashoffset: 0; }
}

.tech-path {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: tech-path 2s ease-out forwards;
}

/* Particle Float */
@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-20px) scale(1.2); }
}

.particle {
  animation: float 3s ease-in-out infinite;
}

/* Orbit Animation */
.orbit-container {
  animation: tech-ring-spin 20s linear infinite;
}

.orbit-dot {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #3b82f6;
  border-radius: 50%;
  box-shadow: 0 0 10px #3b82f6;
}

/* Tech Wave Animation */
@keyframes tech-wave {
  0%, 100% { transform: scaleY(0.5); filter: brightness(0.8); }
  50% { transform: scaleY(1.2); filter: brightness(1.2); }
}

.tech-wave {
  animation: tech-wave 1.5s ease-in-out infinite;
  transform-origin: bottom;
}

/* Cyber Text Effect */
.cyber-text {
  text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

/* Glitch Effect */
@keyframes glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
}

.glitch-layer {
  animation: glitch 3s infinite;
  opacity: 0.5;
  mix-blend-mode: screen;
}

.glitch-layer-2 {
  animation: glitch 3s infinite reverse;
  opacity: 0.3;
  mix-blend-mode: multiply;
}

/* Typing Text Effect */
@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}

.typing-text {
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid #3b82f6;
  animation: typing 2s steps(30), blink 1s infinite;
}

@keyframes blink {
  50% { border-color: transparent; }
}

.animate-spin-slow {
  animation: tech-ring-spin 20s linear infinite;
}
</style>