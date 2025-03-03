import { ref } from 'vue'
import { useServerUrl } from './serverUrl'
import type { HealthStatus } from '../types'

export const useHealthCheck = () => {
  const { getHttpUrl, isConfigured } = useServerUrl()
  const isLoading = ref(false)
  const healthStatus = ref<HealthStatus | null>(null)

  const checkHealth = async () => {
    healthStatus.value = null
    isLoading.value = true
    
    try {
      if (!isConfigured.value) {
        throw new Error('Please apply server configuration first')
      }

      const baseUrl = getHttpUrl()
      const response = await fetch(`${baseUrl}/health`, {
        headers: {
          'Accept': 'application/json',
          'ngrok-skip-browser-warning': 'true'
        }
      })
      
      const contentType = response.headers.get('content-type')
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Server returned non-JSON response')
      }
      
      const data = await response.json()
      
      healthStatus.value = {
        ok: response.ok && data.status === 'healthy',
        message: data.status === 'healthy' ? 'Server is responding normally' : 'Server returned unexpected status'
      }
    } catch (error) {
      healthStatus.value = {
        ok: false,
        message: `Failed to connect to server: ${error instanceof Error ? error.message : 'Unknown error'}`
      }
    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    healthStatus,
    checkHealth
  }
}