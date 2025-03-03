import { ref } from 'vue'
import { useWebSocket } from './websocket'
import { useConnectionPreferences } from './connectionPreferences'

export const useChat = () => {
  const {
    isConnected,
    messages,
    clientId,
    displayName,
    connect,
    disconnect,
    sendMessage,
    clearMessages
  } = useWebSocket()

  const preferences = useConnectionPreferences()
  const currentMessage = ref('')

  const handleConnect = () => {
    if (!preferences.validateInput()) {
      return
    }

    const nameToUse = preferences.getSelectedName()
    connect(nameToUse)
  }

  const handleDisconnect = () => {
    disconnect()
    preferences.resetPreferences()
  }

  const handleSendMessage = () => {
    if (currentMessage.value.trim()) {
      sendMessage(currentMessage.value)
      currentMessage.value = ''
    }
  }

  return {
    // Connection state
    isConnected,
    displayName,
    messages,
    currentMessage,

    // Connection preferences
    ...preferences,

    // Actions
    handleConnect,
    handleDisconnect,
    handleSendMessage,
    clearMessages
  }
}