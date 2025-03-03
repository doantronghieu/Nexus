<template>
  <div class="relative">
    <button
      @click="toggleRecording"
      :class="{ 'recording': isRecording }"
      class="text-white p-2 rounded-full hover:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 bg-blue-600"
      :title="getProviderInfo"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <line x1="12" y1="19" x2="12" y2="23" />
        <line x1="8" y1="23" x2="16" y2="23" />
        <g class="wave-group">
          <path v-for="(wave, index) in waves" :key="index" :d="getWavePath(index, wave.amplitude)" class="wave" :style="{ opacity: isRecording ? 1 : 0 }" />
        </g>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUserPreferencesStore } from '~/stores/chatbot/userPreferences'
import { useAIService } from '~/services/aiHandler'

const emit = defineEmits(['send-message'])
const isRecording = ref(false)
const mediaRecorder = ref(null)
const audioContext = ref(null)
const analyser = ref(null)
const dataArray = ref(null)
const audioChunks = ref([])

const userPreferencesStore = useUserPreferencesStore()
const aiService = useAIService()

const sttSettings = computed(() => userPreferencesStore.getAISettings('speechToText'))
const getProviderInfo = computed(() => {
  const provider = sttSettings.value.provider
  return `Speech-to-Text: ${provider}`
})

const waves = ref([
  { amplitude: 0 },
  { amplitude: 0 },
  { amplitude: 0 },
])

const getWavePath = (index, amplitude) => {
  const baseY = 16
  const controlY1 = baseY - 2 - amplitude * 3
  const controlY2 = baseY + 2 + amplitude * 3
  return `M0 ${baseY} Q6 ${controlY1} 12 ${baseY} Q18 ${controlY2} 24 ${baseY}`
}

const handleTranscription = async (audioBlob) => {
  try {
    const transcription = await aiService.transcribeAudio(audioBlob)
    return transcription
  } catch (error) {
    console.error('Transcription error:', error)
    throw error
  }
}

const toggleRecording = async () => {
  if (!isRecording.value) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder.value = new MediaRecorder(stream)
      audioChunks.value = []

      audioContext.value = new (window.AudioContext || window.webkitAudioContext)()
      analyser.value = audioContext.value.createAnalyser()
      const source = audioContext.value.createMediaStreamSource(stream)
      source.connect(analyser.value)

      analyser.value.fftSize = 32
      const bufferLength = analyser.value.frequencyBinCount
      dataArray.value = new Uint8Array(bufferLength)

      mediaRecorder.value.ondataavailable = (event) => {
        audioChunks.value.push(event.data)
      }

      mediaRecorder.value.onstop = async () => {
        const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' })
        try {
          const transcription = await handleTranscription(audioBlob)
          emit('send-message', transcription)
        } catch (error) {
          console.error('Error processing audio:', error)
          emit('send-message', 'Sorry, I couldn\'t understand the audio. Please try again.')
        }
      }

      mediaRecorder.value.start()
      isRecording.value = true
      animateWaves()
    } catch (error) {
      console.error('Error accessing microphone:', error)
    }
  } else {
    mediaRecorder.value.stop()
    isRecording.value = false
    if (audioContext.value) {
      audioContext.value.close()
    }
  }
}

const animateWaves = () => {
  if (!isRecording.value) return

  analyser.value.getByteFrequencyData(dataArray.value)
  
  // Use different frequency ranges for each wave
  const lowFreq = dataArray.value.slice(0, 3).reduce((a, b) => a + b) / 3
  const midFreq = dataArray.value.slice(3, 6).reduce((a, b) => a + b) / 3
  const highFreq = dataArray.value.slice(6, 9).reduce((a, b) => a + b) / 3

  waves.value[0].amplitude = lowFreq / 128 * 2
  waves.value[1].amplitude = midFreq / 128 * 2
  waves.value[2].amplitude = highFreq / 128 * 2

  requestAnimationFrame(animateWaves)
}

onUnmounted(() => {
  if (audioContext.value) {
    audioContext.value.close()
  }
})
</script>

<style scoped>
.recording {
  @apply bg-red-600;
}

.wave {
  @apply transition-all duration-75;
}

.wave-group {
  @apply transition-opacity duration-200;
}
</style>