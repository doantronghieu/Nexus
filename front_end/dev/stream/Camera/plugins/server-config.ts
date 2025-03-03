import { defineNuxtPlugin } from '#app'
import { ref } from 'vue'

// Shared state for server configuration
const serverHost = ref('')
const protocol = ref('http')
const isConfigured = ref(false)

export default defineNuxtPlugin((nuxtApp) => {
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
      if (process.client) {
        localStorage.setItem('serverConfig', JSON.stringify({ 
          host: serverHost.value, 
          protocol: protocol.value,
          isConfigured: true
        }))
      }
    } else {
      resetServerInfo()
    }
  }

  const resetServerInfo = (): void => {
    serverHost.value = ''
    protocol.value = 'http'
    isConfigured.value = false
    if (process.client) {
      localStorage.removeItem('serverConfig')
    }
  }

  // Load saved configuration on client side
  if (process.client) {
    const savedConfig = localStorage.getItem('serverConfig')
    if (savedConfig) {
      try {
        const config = JSON.parse(savedConfig)
        serverHost.value = config.host
        protocol.value = config.protocol
        isConfigured.value = config.isConfigured
      } catch (error) {
        console.error('Error loading saved server configuration:', error)
        resetServerInfo()
      }
    }
  }

  return {
    provide: {
      serverConfig: {
        serverHost,
        protocol,
        isConfigured,
        getHttpUrl,
        getWsUrl,
        setServerInfo,
        resetServerInfo
      }
    }
  }
})
