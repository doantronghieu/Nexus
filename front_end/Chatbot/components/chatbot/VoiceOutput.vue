<template>
  <button
    @click="toggleSpeech"
    :class="[
      'text-white p-2 rounded-full hover:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200',
      isSpeaking ? 'animate-speaking bg-gradient-to-r from-green-500 to-blue-500' : 'bg-blue-600'
    ]"
    :title="getProviderInfo"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        stroke-width="2" 
        d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" 
      />
    </svg>
  </button>
</template>

<script setup>
import { ref, watch, computed, onMounted, onBeforeUnmount } from 'vue'
import { useTokensStore } from '~/stores/chatbot/tokens'
import { useUserPreferencesStore } from '~/stores/chatbot/userPreferences'
import { useAIService } from '~/services/aiHandler'

const tokensStore = useTokensStore()
const userPreferencesStore = useUserPreferencesStore()

const aiService = useAIService()

const props = defineProps({
  text: {
    type: String,
    required: true
  }
})

const isSpeaking = ref(true)
const currentAudio = ref(null)
const isProcessingQueue = ref(false)

const ttsSettings = computed(() => userPreferencesStore.getAISettings('textToSpeech'))
const getProviderInfo = computed(() => {
  const provider = ttsSettings.value.provider
  const voice = ttsSettings.value.options.voice
  return `Text-to-Speech: ${provider} (${voice})`
})

// Stop characters that trigger text-to-speech generation
const stopCharacters = ['.', '!', '?', ':', ';', '\n', ',']

// Watch for new tokens and process them
watch(() => tokensStore.textAccumulator, async (text) => {
  if (!text || !isSpeaking.value) return

  for (const char of text) {
    if (stopCharacters.includes(char)) {
      const chunk = tokensStore.textAccumulator.trim()
      if (chunk) {
        const chunkId = await tokensStore.addToAudioQueue(chunk)
        processChunk(chunk, chunkId)
      }
      tokensStore.clearTextAccumulator()
      break
    }
  }
}, { immediate: true })

// Process a single chunk of text
const processChunk = async (text, chunkId) => {
  try {
    const audioData = await aiService.textToSpeech(text)
    const duration = await aiService.getAudioDuration(audioData)
    const audioBlob = new Blob([audioData], { type: 'audio/mpeg' })
    const audioUrl = URL.createObjectURL(audioBlob)
    const audio = new Audio(audioUrl)
    
    tokensStore.updateAudioChunk(chunkId, audio, duration)
    processAudioQueue()
  } catch (error) {
    console.error('Error processing audio chunk:', error)
    tokensStore.removeFromQueue(chunkId)
  }
}

// Process the audio queue sequentially
const processAudioQueue = async () => {
  if (isProcessingQueue.value || !isSpeaking.value) return
  
  isProcessingQueue.value = true
  
  try {
    while (tokensStore.hasNextChunk && isSpeaking.value) {
      const chunk = tokensStore.nextAudioChunk
      if (!chunk) break

      currentAudio.value = chunk.audio
      
      try {
        await new Promise((resolve, reject) => {
          chunk.audio.onended = resolve
          chunk.audio.onerror = reject
          chunk.audio.play()
        })
        
        // Wait a small additional time to ensure clear separation between audio chunks
        await new Promise(resolve => setTimeout(resolve, 100))
      } catch (error) {
        console.error('Error playing audio chunk:', error)
      } finally {
        tokensStore.removeFromQueue(chunk.id)
        tokensStore.currentAudioId++
      }
    }
  } finally {
    isProcessingQueue.value = false
    currentAudio.value = null
  }
}

// Toggle speech on/off
const toggleSpeech = () => {
  isSpeaking.value = !isSpeaking.value
  
  if (!isSpeaking.value && currentAudio.value) {
    currentAudio.value.pause()
    currentAudio.value = null
  } else if (isSpeaking.value) {
    processAudioQueue()
  }
}

// Clean up on unmount
onBeforeUnmount(() => {
  isSpeaking.value = false
  if (currentAudio.value) {
    currentAudio.value.pause()
  }
})
</script>

<style scoped>
@keyframes speakingAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-speaking {
  background-size: 200% 200%;
  animation: speakingAnimation 2s ease infinite;
  box-shadow: 0 0 15px rgba(74, 222, 128, 0.5);
}

button {
  position: relative;
  overflow: hidden;
}

button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(45deg);
  transition: all 0.3s ease;
}

button:hover::after {
  transform: rotate(45deg) translate(50%, 50%);
}
</style>