// pages/index.vue
<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">WebSocket Chat</h1>
    
    <div class="mb-4">
      <input
        v-model="message"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Type a message..."
        class="border p-2 rounded w-full"
      />
      <button
        @click="sendMessage"
        class="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Send
      </button>
    </div>

    <div class="border rounded p-4 h-64 overflow-y-auto">
      <div v-for="(msg, index) in messages" :key="index" class="mb-2">
        {{ msg }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: null,
      message: '',
      messages: [],
      isConnected: false
    }
  },
  
  mounted() {
    this.connectWebSocket()
  },
  
  beforeDestroy() {
    if (this.socket) {
      this.socket.close()
    }
  },
  
  methods: {
    connectWebSocket() {
      this.socket = new WebSocket('ws://localhost:8000/ws')
      
      this.socket.onopen = () => {
        this.isConnected = true
        this.messages.push('Connected to WebSocket server')
      }
      
      this.socket.onmessage = (event) => {
        this.messages.push(event.data)
      }
      
      this.socket.onclose = () => {
        this.isConnected = false
        this.messages.push('Disconnected from WebSocket server')
        // Attempt to reconnect after 5 seconds
        setTimeout(this.connectWebSocket, 5000)
      }
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.messages.push('Error connecting to WebSocket server')
      }
    },
    
    sendMessage() {
      if (this.message.trim() && this.isConnected) {
        this.socket.send(this.message)
        this.message = ''
      }
    }
  }
}
</script>