import { useNuxtApp } from '#app'
import { ref, computed } from 'vue'

export function useServerConfig() {
  const { $serverConfig } = useNuxtApp()
  
  // Local state for form handling
  const localServerHost = ref('')
  const localIsSecure = ref(false)
  const showValidation = ref(false)
  const showOptions = ref(false)

  // URLs for display
  const displayHttpUrl = computed(() => $serverConfig.getHttpUrl() || 'Not configured')
  const displayWsUrl = computed(() => $serverConfig.getWsUrl() || 'Not configured')

  // Methods
  const selectHost = (host: string) => {
    localServerHost.value = host
    showOptions.value = false
  }

  const toggleOptions = () => {
    showOptions.value = !showOptions.value
  }

  const applyConfig = () => {
    showValidation.value = true
    showOptions.value = false
    
    if (localServerHost.value.trim()) {
      $serverConfig.setServerInfo(localServerHost.value, localIsSecure.value)
    }
  }

  const setupClickOutside = () => {
    const handleClickOutside = (event: MouseEvent) => {
      const form = document.querySelector('form')
      if (form && !form.contains(event.target as Node)) {
        showOptions.value = false
      }
    }

    document.addEventListener('click', handleClickOutside)

    return () => {
      document.removeEventListener('click', handleClickOutside)
    }
  }

  const resetConfig = () => {
    localServerHost.value = ''
    localIsSecure.value = false
    showValidation.value = false
    showOptions.value = false
    $serverConfig.resetServerInfo()
  }

  return {
    // Server config state
    serverHost: $serverConfig.serverHost,
    protocol: $serverConfig.protocol,
    isConfigured: $serverConfig.isConfigured,
    getHttpUrl: $serverConfig.getHttpUrl,
    getWsUrl: $serverConfig.getWsUrl,

    // Form state
    localServerHost,
    localIsSecure,
    showValidation,
    showOptions,

    // Computed
    displayHttpUrl,
    displayWsUrl,

    // Methods
    selectHost,
    toggleOptions,
    applyConfig,
    setupClickOutside,
    resetConfig,

    // Constants
    predefinedHosts
  }
}
