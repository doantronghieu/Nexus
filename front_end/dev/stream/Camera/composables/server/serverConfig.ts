import { ref, computed } from 'vue'
import { useServerUrl } from './serverUrl'

export const predefinedHosts = [
  'key-amoeba-basically.ngrok-free.app',
  'positive-viper-presently.ngrok-free.app',
  'localhost:8000'
] as const

export const useServerConfig = () => {
  const { serverHost, protocol, isConfigured, getHttpUrl, getWsUrl, setServerInfo, resetServerInfo } = useServerUrl()

  // Local state
  const localServerHost = ref('')
  const localIsSecure = ref(false)
  const showValidation = ref(false)
  const showOptions = ref(false)

  // URLs for display
  const displayHttpUrl = computed(() => getHttpUrl() || 'Not configured')
  const displayWsUrl = computed(() => getWsUrl() || 'Not configured')

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
      setServerInfo(localServerHost.value, localIsSecure.value)
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
    resetServerInfo()
  }

  return {
    // State
    localServerHost,
    localIsSecure,
    showValidation,
    showOptions,
    isConfigured,

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