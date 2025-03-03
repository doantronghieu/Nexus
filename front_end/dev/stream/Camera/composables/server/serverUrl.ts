import { ref, readonly } from 'vue'

// Create a single shared state instance
const serverHost = ref('')
const protocol = ref('http')
const isConfigured = ref(false)

export const useServerUrl = () => {
  const getHttpUrl = (): string => {
    if (!serverHost.value.trim()) {
      return ''
    }
    return `${protocol.value}://${serverHost.value.trim()}`
  }

  const getWsUrl = (): string => {
    if (!serverHost.value.trim()) {
      return ''
    }
    const wsProtocol = protocol.value === 'https' ? 'wss' : 'ws'
    return `${wsProtocol}://${serverHost.value.trim()}/ws`
  }

  const setServerInfo = (host: string, isSecure = false): void => {
    if (host.trim()) {
      serverHost.value = host.trim()
      protocol.value = isSecure ? 'https' : 'http'
      isConfigured.value = true
      console.log('Server configuration updated:', {
        host: serverHost.value,
        protocol: protocol.value,
        isConfigured: isConfigured.value
      })
    } else {
      resetServerInfo()
    }
  }

  const resetServerInfo = (): void => {
    serverHost.value = ''
    protocol.value = 'http'
    isConfigured.value = false
    console.log('Server configuration reset')
  }

  return {
    serverHost: readonly(serverHost),
    protocol: readonly(protocol),
    isConfigured: readonly(isConfigured),
    getHttpUrl,
    getWsUrl,
    setServerInfo,
    resetServerInfo
  }
}