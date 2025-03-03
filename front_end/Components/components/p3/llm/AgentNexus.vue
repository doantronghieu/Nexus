<template>
  <div class="agent-nexus">
    <div class="agent-container" :class="{ 'audio-playing': isAudioPlaying }">
      <!-- Status Bar -->
      <div class="status-bar" :class="{ 'has-agent': currentAgent }">
        <div class="agent-indicator">
          <div class="status-dot" :class="{ active: currentAgent }"></div>
          <span class="agent-name">{{ currentAgent || 'Vehicle Assistant' }}</span>
          <div v-if="isAudioPlaying" class="audio-indicator">
            <div class="audio-wave">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
        <div class="connection-status">
          <span class="connection-dot" :class="{ connected: wsConnected }"></span>
          {{ wsConnected ? 'Connected' : 'Connecting...' }}
        </div>
      </div>

      <!-- Message Display -->
      <div class="message-container" :class="{ loading: isLoading }">
        <!-- Fixed Loading State -->
        <div v-if="isLoading" class="loading-state-fixed">
          <div class="loading-indicator">
            <div class="loading-animation">
              <div class="dot-pulse"></div>
            </div>
            <span class="loading-text">Processing your request...</span>
          </div>
        </div>
        
        <!-- Message Content -->
        <transition name="fade" mode="out-in">
          <div v-if="output" class="message-content" key="output">
            <div class="message-bubble">
              <div class="message-text typewriter">
                {{ output }}
              </div>
            </div>
          </div>
          <div v-else class="placeholder-message" key="placeholder">
            <div class="placeholder-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
            </div>
            <span>How can I assist you with your journey?</span>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, defineExpose } from 'vue'
import services from '@/configs/services_info_p3.json'

const output = ref('')
const currentAgent = ref('')
const ws = ref(null)
const pollInterval = ref(null)
const isLoading = ref(false)
const wsConnected = ref(false)
const audioContext = ref(null)
const isAudioPlaying = ref(false)

// Initialize audio context
onMounted(() => {
  audioContext.value = new (window.AudioContext || window.webkitAudioContext)()
})

const clearMessage = () => {
  output.value = ''
  isLoading.value = true
}

const connectWebSocket = () => {
  const wsUrl = `ws://${services['app-llm'].host}:${services['app-llm'].port}/ws`
  ws.value = new WebSocket(wsUrl)

  ws.value.onopen = () => {
    wsConnected.value = true
  }

  ws.value.onmessage = async (event) => {
    isLoading.value = false
    output.value = event.data

    try {
      // Send text to text-to-speech service
      const response = await fetch(`${services['svc-tts'].url}/synthesize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: event.data,
          engine: 'openai',
          format: 'wav'
        })
      })

      if (!response.ok) {
        throw new Error('Text-to-speech request failed')
      }

      // Get audio data as ArrayBuffer
      const audioData = await response.arrayBuffer()
      
      // Create audio buffer from binary data
      const audioBuffer = await audioContext.value.decodeAudioData(audioData)
      
      // Create audio source and connect to context
      const source = audioContext.value.createBufferSource()
      source.buffer = audioBuffer
      source.connect(audioContext.value.destination)
      
      // Set playing state and play audio
      isAudioPlaying.value = true
      source.start(0)
      
      // Reset playing state when audio ends
      source.onended = () => {
        isAudioPlaying.value = false
      }
    } catch (error) {
      console.error('Text-to-speech playback failed:', error)
      isAudioPlaying.value = false
    }
  }

  ws.value.onclose = () => {
    wsConnected.value = false
    setTimeout(connectWebSocket, 1000)
  }

  ws.value.onerror = (error) => {
    wsConnected.value = false
    console.error('WebSocket error:', error)
  }
}

const fetchAgentStatus = async () => {
  try {
    const response = await fetch(`http://${services['app-llm'].host}:${services['app-llm'].port}/agent-status`)
    if (!response.ok) throw new Error('Failed to fetch agent status')
    const data = await response.json()
    currentAgent.value = data.current || ''
  } catch (error) {
    console.error('Error fetching agent status:', error)
  }
}

onMounted(() => {
  connectWebSocket()
  fetchAgentStatus()
  pollInterval.value = setInterval(fetchAgentStatus, 1000)
})

onBeforeUnmount(() => {
  if (ws.value) {
    ws.value.close()
  }
  if (pollInterval.value) {
    clearInterval(pollInterval.value)
  }
})

defineExpose({
  clearMessage,
  currentAgent
})
</script>

<style scoped>
.agent-nexus {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.agent-container {
  background: rgba(15, 23, 42, 0.95);
  border-radius: 1.5rem;
  padding: 0.75rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  backdrop-filter: blur(0.75rem);
  border: 1px solid rgba(51, 65, 85, 0.5);
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
}

.agent-container.audio-playing {
  border-color: rgba(59, 130, 246, 0.5);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

/* Status Bar */
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 0.75rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.status-bar.has-agent {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.2);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.agent-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-dot {
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background: #64748b;
  transition: all 0.3s ease;
  position: relative;
}

.status-dot.active {
  background: #3b82f6;
  box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.2);
}

.status-dot.active::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: inherit;
  opacity: 0.7;
  animation: pulse 2s infinite;
}

.agent-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
  letter-spacing: 0.01em;
}

.audio-indicator {
  margin-left: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.audio-wave {
  display: flex;
  align-items: center;
  gap: 0.125rem;
  height: 0.75rem;
}

.audio-wave span {
  display: block;
  width: 0.125rem;
  height: 100%;
  background-color: #3b82f6;
  border-radius: 1px;
  animation: wave 1s ease-in-out infinite;
}

.audio-wave span:nth-child(2) {
  animation-delay: 0.2s;
}

.audio-wave span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1); }
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #94a3b8;
  background: rgba(30, 41, 59, 0.6);
  padding: 0.375rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
}

.connection-dot {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background: #64748b;
  transition: all 0.3s ease;
}

.connection-dot.connected {
  background: #10b981;
  box-shadow: 0 0 0.25rem rgba(16, 185, 129, 0.4);
}

/* Message Container */
.message-container {
  flex: 1;
  background: rgba(15, 23, 42, 0.7);
  border-radius: 0.75rem;
  padding: 0.5rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 0;
  width: 100%;
}

.message-bubble {
  display: flex;
  width: 100%;
  margin: 0;
  animation: slideUp 0.3s ease forwards;
}

.message-text {
  background: rgba(30, 41, 59, 0.6);
  padding: 0.75rem;
  border-radius: 0.75rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  line-height: 1.4;
  border: 1px solid rgba(51, 65, 85, 0.5);
  position: relative;
  white-space: pre-wrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  text-align: center;
}

/* Typewriter effect for smoother text experience */
.typewriter {
  overflow: hidden;
  animation: typing 0.5s steps(40, end);
}

@keyframes typing {
  from { max-width: 0 }
  to { max-width: 100% }
}

.placeholder-message {
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  height: 100%;
  text-align: center;
  font-size: 0.85rem;
  animation: fadeIn 0.5s ease forwards;
}

.placeholder-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(59, 130, 246, 0.2);
  animation: pulse 2s infinite;
}

.placeholder-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

/* Fixed Loading State */
.loading-state-fixed {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  background: rgba(15, 23, 42, 0.75);
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  backdrop-filter: blur(4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease forwards;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  font-size: 0.95rem;
  color: #3b82f6;
  font-weight: 500;
  white-space: nowrap;
}

.loading-animation {
  position: relative;
  width: 8px;
  height: 8px;
  margin: 0 12px;
}

.dot-pulse {
  position: relative;
  left: -9999px;
  width: 8px;
  height: 8px;
  border-radius: 5px;
  background-color: #3b82f6;
  color: #3b82f6;
  box-shadow: 9999px 0 0 -5px;
  animation: dot-pulse 1.5s infinite linear;
  animation-delay: 0.25s;
}

.dot-pulse::before, .dot-pulse::after {
  content: '';
  display: inline-block;
  position: absolute;
  top: 0;
  width: 8px;
  height: 8px;
  border-radius: 5px;
  background-color: #3b82f6;
  color: #3b82f6;
}

.dot-pulse::before {
  box-shadow: 9984px 0 0 -5px;
  animation: dot-pulse-before 1.5s infinite linear;
  animation-delay: 0s;
}

.dot-pulse::after {
  box-shadow: 10014px 0 0 -5px;
  animation: dot-pulse-after 1.5s infinite linear;
  animation-delay: 0.5s;
}

@keyframes dot-pulse-before {
  0% {
    box-shadow: 9984px 0 0 -5px;
  }
  30% {
    box-shadow: 9984px 0 0 2px;
  }
  60%, 100% {
    box-shadow: 9984px 0 0 -5px;
  }
}

@keyframes dot-pulse {
  0% {
    box-shadow: 9999px 0 0 -5px;
  }
  30% {
    box-shadow: 9999px 0 0 2px;
  }
  60%, 100% {
    box-shadow: 9999px 0 0 -5px;
  }
}

@keyframes dot-pulse-after {
  0% {
    box-shadow: 10014px 0 0 -5px;
  }
  30% {
    box-shadow: 10014px 0 0 2px;
  }
  60%, 100% {
    box-shadow: 10014px 0 0 -5px;
  }
}

/* Animations */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
  70% { box-shadow: 0 0 0 0.75rem rgba(59, 130, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(0.5rem); }
  to { opacity: 1; transform: translateY(0); }
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(0.625rem);
}

/* Removed scrollbar styling as container is no longer scrollable */

/* Light Mode Support */
@media (prefers-color-scheme: light) {
  .agent-container {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .status-bar {
    background: rgba(248, 250, 252, 0.8);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .status-bar.has-agent {
    background: rgba(59, 130, 246, 0.1);
  }

  .agent-name {
    color: #1e293b;
  }

  .audio-indicator {
    background: rgba(59, 130, 246, 0.1);
    border-color: rgba(59, 130, 246, 0.3);
  }

  .connection-status {
    color: #64748b;
    background: rgba(248, 250, 252, 0.8);
  }

  .message-container {
    background: rgba(248, 250, 252, 0.7);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .message-text {
    background: rgba(255, 255, 255, 0.8);
    color: #1e293b;
    border-color: rgba(226, 232, 240, 0.8);
  }

  .placeholder-message {
    color: #64748b;
  }
  
  .loading-state-fixed {
    background: rgba(248, 250, 252, 0.85);
    border-color: rgba(226, 232, 240, 0.8);
  }
}

/* Touch Device Optimizations */
@media (hover: none) and (pointer: coarse) {
  .status-bar {
    padding: 1rem 1.25rem;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .agent-container,
  .status-bar,
  .message-container {
    background: white;
    border: 2px solid black;
  }

  .message-text {
    color: black;
    background: white;
    border: 2px solid black;
  }

  .status-dot.active {
    background: blue;
  }

  .connection-dot.connected {
    background: green;
  }

  .audio-indicator {
    background: white;
    border: 2px solid blue;
  }

  .audio-wave span {
    background-color: blue;
  }
  
  .placeholder-icon {
    background: white;
    border: 2px solid blue;
    color: blue;
  }
  
  .loading-animation .dot-pulse,
  .loading-animation .dot-pulse::before,
  .loading-animation .dot-pulse::after {
    background-color: blue;
    color: blue;
  }
  
  .loading-state-fixed {
    background: white;
    border: 2px solid black;
  }
  
  .loading-text {
    color: black;
  }
}

/* Responsive Design for smaller screens */
@media (max-width: 768px) {
  .status-bar {
    padding: 0.5rem 0.75rem;
  }
  
  .agent-name {
    font-size: 0.8rem;
  }
  
  .message-text {
    font-size: 0.85rem;
    padding: 0.625rem;
  }
  
  .message-bubble {
    gap: 0.5rem;
  }
}
</style>