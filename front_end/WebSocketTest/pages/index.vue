// Modified constants in VoiceInput.vue

// Modified checkSilence function


// Modified stopRecording function
<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">Voice Assistant</h1>
        <p class="text-gray-600">Say "Hi I Vee" to activate</p>
        
        <!-- Mode Toggle Switch -->
        <div class="mt-4">
          <label class="relative inline-flex items-center cursor-pointer">
            <input 
              type="checkbox" 
              v-model="justDoWWD" 
              class="sr-only peer"
              @change="handleModeChange"
            >
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            <span class="ml-3 text-sm font-medium text-gray-900">
              {{ justDoWWD ? 'Wake Word Detection Only' : 'Full Pipeline' }}
            </span>
          </label>
        </div>
      </div>
      
      <!-- Main Control Panel -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div class="flex justify-center space-x-4 mb-6">
          <button
            @click="startRecording"
            :disabled="isRecording"
            class="flex items-center px-6 py-3 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:hover:scale-100"
            :class="{
              'bg-green-500 hover:bg-green-600 text-white disabled:bg-green-300': !isRecording,
              'opacity-50 cursor-not-allowed': isRecording
            }"
          >
            <span class="mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </span>
            Start Listening
          </button>
          
          <button
            @click="stopRecording"
            :disabled="!isRecording"
            class="flex items-center px-6 py-3 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:hover:scale-100"
            :class="{
              'bg-red-500 hover:bg-red-600 text-white disabled:bg-red-300': isRecording,
              'opacity-50 cursor-not-allowed': !isRecording
            }"
          >
            <span class="mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
              </svg>
            </span>
            Stop Listening
          </button>
        </div>

        <!-- Live Audio Level Visualization -->
        <div class="mb-6">
          <div class="flex justify-between mb-2">
            <span class="text-gray-600">Audio Level</span>
            <span class="text-gray-800 font-medium">{{ audioLevel.toFixed(2) }}</span>
          </div>
          <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              class="h-full transition-all duration-100 bg-blue-500 rounded-full"
              :style="{ width: `${Math.min(audioLevel * 100, 100)}%` }"
            ></div>
          </div>
        </div>

        <!-- Status Panel -->
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex items-center justify-between">
              <span class="text-gray-600">Connection:</span>
              <span :class="{
                'text-green-500': isConnected,
                'text-red-500': !isConnected
              }">{{ isConnected ? 'Connected' : 'Disconnected' }}</span>
            </div>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex items-center justify-between">
              <span class="text-gray-600">Status:</span>
              <span :class="{
                'text-green-500': currentState === 'Recording Speech',
                'text-blue-500': currentState === 'Listening for Wake Word',
                'text-yellow-500': currentState === 'Processing with LLM...',
                'text-red-500': currentState === 'Error' || currentState === 'Disconnected'
              }">{{ currentState }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Wake Word Alert -->
      <div v-if="showWakeWordAlert"
           class="bg-green-100 border-l-4 border-green-500 p-4 rounded-lg mb-6 animate-pulse">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm leading-5 text-green-700">
              {{ justDoWWD ? 'Wake word detected!' : 'Wake word detected! I\'m listening...' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Only show these sections if not in WWD-only mode -->
      <template v-if="!justDoWWD">
        <!-- Speech Processing Indicator -->
        <div v-if="isProcessingSpeech"
             class="bg-blue-100 border-l-4 border-blue-500 p-4 rounded-lg mb-6">
          <div class="flex items-center">
            <svg class="animate-spin h-5 w-5 text-blue-500 mr-3" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-blue-700">Processing your speech...</span>
          </div>
        </div>

        <!-- LLM Processing Indicator -->
        <div v-if="currentState === 'Processing with LLM...'"
             class="bg-yellow-100 border-l-4 border-yellow-500 p-4 rounded-lg mb-6">
          <div class="flex items-center">
            <svg class="animate-spin h-5 w-5 text-yellow-500 mr-3" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-yellow-700">Getting response from LLM...</span>
          </div>
        </div>

        <!-- Conversation Display -->
        <div v-if="conversations.length > 0" 
             class="bg-white rounded-xl shadow-lg p-6 transition-all duration-500 animate-fade-in">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Conversation</h2>
          <div class="space-y-4">
            <div v-for="(conv, index) in conversations" :key="index" class="space-y-4">
              <!-- User Message -->
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                </div>
                <div class="flex-1 bg-blue-50 rounded-lg p-3">
                  <p class="text-gray-800">{{ conv.user_text }}</p>
                </div>
              </div>

              <!-- Assistant Message -->
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <div class="flex-1 bg-green-50 rounded-lg p-3">
                  <p class="text-gray-800">{{ conv.assistant_text }}</p>
                  <button
                    v-if="conv.audio && conv.assistant_text !== '...'"
                    @click="replayResponse(index)"
                    class="mt-2 text-sm text-green-600 hover:text-green-700 flex items-center"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Replay Response
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Audio elements -->
      <audio id="wakeWordSound" preload="auto">
        <source src="assets/sounds/wake-word-detected.wav" type="audio/mpeg">
      </audio>
      <audio id="finishTranscribeSound" preload="auto">
        <source src="assets/sounds/finished-transcribed.wav" type="audio/mpeg">
      </audio>
      <audio id="ttsAudio" preload="auto"></audio>
    </div>
  </div>
</template>

<script>
// Configurations
const Config = {
  AUDIO: {
    SAMPLE_RATE: 16000,
    BUFFER_SIZE: 2048,
    CHUNK_ACCUMULATOR_SIZE: 1280,
    AUDIO_SCALE: 0.1  // For audio level visualization
  },
  SERVER: {
    WEBSOCKET_URL: 'ws://localhost:8000/ws',
    RECONNECT_DELAY: 5000,
    BASE_URL: 'http://localhost:8000',
  },
  SOUNDS: {
    WAKE_WORD_SOUND: 'assets/sounds/wake-word-detected.wav',
    TRANSCRIBE_COMPLETE_SOUND: 'assets/sounds/finished-transcribed.wav'
  },
  UI: {
    ALERT_DURATION: 3000,
    TTS_PLAY_DELAY: 500
  }
}

export default {
  data() {
    return {
      justDoWWD: false,
      socket: null,
      audioContext: null,
      processor: null,
      isConnected: false,
      isRecording: false,
      isProcessingSpeech: false,
      showWakeWordAlert: false,
      alertTimeout: null,
      audioAccumulator: [],
      currentState: 'Idle',
      audioLevel: 0,
      wakeWordSound: null,
      finishTranscribeSound: null,
      ttsAudio: null,
      conversations: [],
    }
  },
  
  async mounted() {
    // Get initial mode from server
    try {
      const response = await fetch(`${Config.SERVER.BASE_URL}/get_mode`)
      const data = await response.json()
      this.justDoWWD = data.just_wwd
      console.log(`Initial mode set to: ${this.justDoWWD ? 'WWD-only' : 'full pipeline'}`)
    } catch (error) {
      console.error('Error getting initial mode:', error)
    }
    
    this.connectWebSocket()
    // Initialize audio elements
    this.wakeWordSound = document.getElementById('wakeWordSound')
    this.finishTranscribeSound = document.getElementById('finishTranscribeSound')
    this.ttsAudio = document.getElementById('ttsAudio')
  },
  
  methods: {
    async handleModeChange() {
      try {
        // Send mode change to server with proper JSON structure
        const response = await fetch(`${Config.SERVER.BASE_URL}/set_mode`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ just_wwd: this.justDoWWD })  // Changed this line
        });
        
        if (!response.ok) {
          throw new Error(`Failed to update server mode: ${response.status}`);
        }

        // Reset states when changing modes
        this.stopRecording();
        this.conversations = [];
        this.showWakeWordAlert = false;
        this.currentState = 'Idle';
        
        // Reconnect WebSocket to get fresh state
        if (this.socket) {
          this.socket.close();
          this.socket = null;
          // Small delay before reconnecting to ensure clean state
          setTimeout(() => {
            this.connectWebSocket();
          }, 1000);
        }

        console.log(`Mode changed to: ${this.justDoWWD ? 'WWD-only' : 'full pipeline'}`);
      } catch (error) {
        console.error('Error changing mode:', error);
        // Revert the toggle if server update failed
        this.justDoWWD = !this.justDoWWD;
      }
    },

    playSound(audioElement) {
      if (audioElement) {
        audioElement.currentTime = 0
        audioElement.play().catch(error => {
          console.error('Error playing sound:', error)
        })
      }
    },

    connectWebSocket() {
      this.socket = new WebSocket(Config.SERVER.WEBSOCKET_URL)
      
      this.socket.onopen = () => {
        this.isConnected = true
        this.currentState = 'Connected'
        console.log('WebSocket connected')
      }
      
      this.socket.onmessage = this.handleWebSocketMessage
      
      this.socket.onclose = () => {
        this.isConnected = false
        this.currentState = 'Disconnected'
        console.log('WebSocket disconnected')
        setTimeout(this.connectWebSocket, Config.SERVER.RECONNECT_DELAY)
      }
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.currentState = 'Error'
      }
    },

    handleWebSocketMessage(event) {
      const data = JSON.parse(event.data)
      
      if (data.mode === 'wwd_only') {
        // Handle WWD-only mode messages
        if (data.wake_word_detected) {
          this.showWakeWordAlert = true
          this.playSound(this.wakeWordSound)
          
          if (this.alertTimeout) {
            clearTimeout(this.alertTimeout)
          }
          
          this.alertTimeout = setTimeout(() => {
            this.showWakeWordAlert = false
          }, Config.UI.ALERT_DURATION)
        }
      } else {
        // Handle full pipeline mode messages
        if (data.action === 'start_recording') {
          this.handleWakeWordDetection()
          this.currentState = 'Recording Speech'
          this.isProcessingSpeech = true
        } 
        else if (data.action === 'transcription_complete') {
          console.log('Received transcription:', data.user_text)
          this.handleTranscriptionReceived(data.user_text)
        }
        else if (data.action === 'llm_complete') {
          console.log('Received LLM response')
          this.handleAssistantResponse(data.assistant_text, data.tts_audio)
        }
      }
    },
    
    handleWakeWordDetection() {
      this.showWakeWordAlert = true
      this.playSound(this.wakeWordSound)
      
      if (this.alertTimeout) {
        clearTimeout(this.alertTimeout)
      }
      
      this.alertTimeout = setTimeout(() => {
        this.showWakeWordAlert = false
      }, Config.UI.ALERT_DURATION)
    },

    handleTranscriptionReceived(userText) {
      // Play transcription complete sound
      this.playSound(this.finishTranscribeSound)
      
      // Add user message to conversation immediately
      this.conversations.push({
        user_text: userText,
        assistant_text: "...", // Placeholder while waiting for LLM
        audio: null
      })
      
      this.isProcessingSpeech = false
      this.currentState = 'Processing with LLM...'
    },
    
    handleAssistantResponse(assistantText, ttsAudio) {
      // Update the latest conversation with the assistant's response
      if (this.conversations.length > 0) {
        const lastConversation = this.conversations[this.conversations.length - 1]
        lastConversation.assistant_text = assistantText
        lastConversation.audio = ttsAudio
      }

      this.currentState = 'Conversation Complete'
      
      // Play TTS audio after a short delay
      setTimeout(() => {
        console.log('Playing TTS response')
        this.playTTSResponse(ttsAudio)
      }, Config.UI.TTS_PLAY_DELAY)
    },

    playTTSResponse(audioData) {
      if (!audioData) {
        console.error('No audio data provided')
        return
      }

      try {
        console.log('Creating audio blob')
        const audioBlob = this.base64ToBlob(audioData, 'audio/mp3')
        const audioUrl = URL.createObjectURL(audioBlob)
        
        this.ttsAudio.src = audioUrl
        this.ttsAudio.oncanplay = () => {
          console.log('Audio can play, starting playback')
          this.ttsAudio.play()
            .then(() => console.log('Audio playback started'))
            .catch(error => console.error('Error playing audio:', error))
        }
        
        this.ttsAudio.onended = () => {
          console.log('Audio playback ended')
          URL.revokeObjectURL(audioUrl)
        }
      } catch (error) {
        console.error('Error setting up audio playback:', error)
      }
    },

    base64ToBlob(base64, type) {
      try {
        console.log('Converting base64 to blob')
        const byteCharacters = atob(base64)
        const byteArrays = []

        for (let offset = 0; offset < byteCharacters.length; offset += 512) {
          const slice = byteCharacters.slice(offset, offset + 512)
          const byteNumbers = new Array(slice.length)
          
          for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i)
          }
          
          const byteArray = new Uint8Array(byteNumbers)
          byteArrays.push(byteArray)
        }

        const blob = new Blob(byteArrays, { type: type })
        console.log('Blob created successfully')
        return blob
      } catch (error) {
        console.error('Error converting base64 to blob:', error)
        return null
      }
    },

    replayResponse(index) {
      const conversation = this.conversations[index]
      if (conversation && conversation.audio) {
        console.log('Replaying response at index:', index)
        this.playTTSResponse(conversation.audio)
      }
    },

    calculateAudioLevel(audioData) {
      const sum = audioData.reduce((acc, val) => acc + (val * val), 0)
      const rms = Math.sqrt(sum / audioData.length)
      this.audioLevel = Math.min(1, Math.max(0, rms * Config.AUDIO.AUDIO_SCALE))
    },

    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          audio: {
            sampleRate: Config.AUDIO.SAMPLE_RATE,
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true
          }
        })
        
        this.audioContext = new AudioContext({
          sampleRate: Config.AUDIO.SAMPLE_RATE
        })
        
        const source = this.audioContext.createMediaStreamSource(stream)
        this.processor = this.audioContext.createScriptProcessor(
          Config.AUDIO.BUFFER_SIZE, 
          1, 
          1
        )
        
        this.processor.onaudioprocess = (e) => {
          const inputData = e.inputBuffer.getChannelData(0)
          this.calculateAudioLevel(inputData)
          
          const int16Data = new Int16Array(inputData.length)
          for (let i = 0; i < inputData.length; i++) {
            int16Data[i] = Math.max(-32768, Math.min(32767, Math.floor(inputData[i] * 32768)))
          }
          
          this.audioAccumulator.push(...int16Data)
          
          while (this.audioAccumulator.length >= Config.AUDIO.CHUNK_ACCUMULATOR_SIZE) {
            const chunk = new Int16Array(
              this.audioAccumulator.slice(0, Config.AUDIO.CHUNK_ACCUMULATOR_SIZE)
            )
            this.audioAccumulator = this.audioAccumulator.slice(
              Config.AUDIO.CHUNK_ACCUMULATOR_SIZE
            )
            this.sendAudioChunk(chunk)
          }
        }
        
        source.connect(this.processor)
        this.processor.connect(this.audioContext.destination)
        this.isRecording = true
        this.currentState = 'Listening for Wake Word'
        
      } catch (error) {
        console.error('Error starting recording:', error)
        this.currentState = 'Error Starting Recording'
      }
    },
    
    stopRecording() {
      if (this.processor) {
        this.processor.disconnect()
        this.processor = null
      }
      if (this.audioContext) {
        this.audioContext.close()
        this.audioContext = null
      }
      this.audioAccumulator = []
      this.isRecording = false
      this.isProcessingSpeech = false
      this.audioLevel = 0
      this.currentState = 'Stopped'
      this.showWakeWordAlert = false
      if (this.alertTimeout) {
        clearTimeout(this.alertTimeout)
      }
    },

    sendAudioChunk(chunk) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(chunk.buffer)
      }
    }
  },

  beforeUnmount() {
    this.stopRecording()
    if (this.socket) {
      this.socket.close()
    }
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
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
    opacity: 0.7;
  }
}
</style>