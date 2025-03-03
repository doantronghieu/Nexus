import { ref, onUnmounted } from 'vue'
import { useServerUrl } from '../server'
import type { WebSocketMessage } from '../types'

export const useWebSocket = () => {
  const { getWsUrl, isConfigured } = useServerUrl()
  const socket = ref(null)
  const isConnected = ref(false)
  const messages = ref([])
  const clientId = ref('')
  const displayName = ref('')

  const connect = (userName?: string) => {
    try {
      if (!isConfigured.value) {
        throw new Error('Please apply server configuration first')
      }

      let wsUrl = getWsUrl()
      if (userName) {
        wsUrl += `?client_name=${encodeURIComponent(userName)}`
      }

      socket.value = new WebSocket(wsUrl)
      
      socket.value.onopen = () => {
        isConnected.value = true
      }
      
      socket.value.onmessage = (event) => {
        const data: WebSocketMessage = JSON.parse(event.data)
        
        if (data.type === 'client_info') {
          clientId.value = data.client_id
          displayName.value = data.display_name
          messages.value.push(`Connected as ${data.display_name}`)
        } else if (data.type === 'message') {
          messages.value.push(`${data.sender}: ${data.content}`)
        }
      }
      
      socket.value.onclose = () => {
        isConnected.value = false
        messages.value.push('Disconnected from server')
        clientId.value = ''
        displayName.value = ''
      }
      
      socket.value.onerror = (error) => {
        messages.value.push(`WebSocket error: ${error.message}`)
        isConnected.value = false
      }
    } catch (error) {
      messages.value.push(`Failed to connect: ${error.message}`)
    }
  }

  const disconnect = () => {
    if (socket.value) {
      socket.value.close()
      socket.value = null
      isConnected.value = false
      clientId.value = ''
      displayName.value = ''
    }
  }

  const sendMessage = (text: string) => {
    if (socket.value && text.trim()) {
      socket.value.send(text)
      return true
    }
    return false
  }

  const clearMessages = () => {
    messages.value = []
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    messages,
    clientId,
    displayName,
    connect,
    disconnect,
    sendMessage,
    clearMessages
  }
}