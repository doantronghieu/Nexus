<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Audio Streaming</h1>
    
    <div class="space-y-4">
      <div class="flex space-x-4">
        <button
          @click="startRecording"
          :disabled="isRecording"
          class="bg-green-500 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Start Recording
        </button>
        
        <button
          @click="stopRecording"
          :disabled="!isRecording"
          class="bg-red-500 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Stop Recording
        </button>
      </div>
      
      <div class="status-display p-4 border rounded">
        <p>Connection Status: {{ isConnected ? 'Connected' : 'Disconnected' }}</p>
        <p>Recording Status: {{ isRecording ? 'Recording' : 'Stopped' }}</p>
        <p>Chunks Sent: {{ chunksSent }}</p>
      </div>
      
      <div class="audio-visualizer border h-32">
        <!-- Add visualization here if desired -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: null,
      mediaRecorder: null,
      audioContext: null,
      isConnected: false,
      isRecording: false,
      chunksSent: 0,
      chunkInterval: 500, // 0.5 seconds in milliseconds
    }
  },
  
  mounted() {
    this.connectWebSocket()
  },
  
  beforeDestroy() {
    this.stopRecording()
    if (this.socket) {
      this.socket.close()
    }
  },
  
  methods: {
    connectWebSocket() {
      this.socket = new WebSocket('ws://localhost:8000/ws')
      
      this.socket.onopen = () => {
        this.isConnected = true
        console.log('WebSocket connected')
      }
      
      this.socket.onclose = () => {
        this.isConnected = false
        console.log('WebSocket disconnected')
        setTimeout(this.connectWebSocket, 5000)
      }
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
    },
    
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        
        // Create MediaRecorder
        this.mediaRecorder = new MediaRecorder(stream, {
          mimeType: 'audio/webm',
          audioBitsPerSecond: 16000
        })
        
        let audioChunk = []
        let sendInterval
        
        this.mediaRecorder.ondataavailable = (event) => {
          audioChunk.push(event.data)
        }
        
        // Send chunks every 500ms
        sendInterval = setInterval(() => {
          if (audioChunk.length > 0) {
            const blob = new Blob(audioChunk, { type: 'audio/webm' })
            this.sendAudioChunk(blob)
            audioChunk = []
            this.chunksSent++
          }
        }, this.chunkInterval)
        
        this.mediaRecorder.onstop = () => {
          clearInterval(sendInterval)
          stream.getTracks().forEach(track => track.stop())
        }
        
        // Request data every 500ms
        this.mediaRecorder.start(this.chunkInterval)
        this.isRecording = true
        
      } catch (error) {
        console.error('Error starting recording:', error)
      }
    },
    
    stopRecording() {
      if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop()
        this.isRecording = false
      }
    },
    
    async sendAudioChunk(blob) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        // Convert blob to array buffer before sending
        const arrayBuffer = await blob.arrayBuffer()
        this.socket.send(arrayBuffer)
      }
    }
  }
}
</script>