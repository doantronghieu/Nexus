import { ref, onUnmounted } from 'vue'
import { useServerUrl } from './serverUrl'
import type { ServerStats } from '../types'

export const useWebSocketStats = () => {
  const { getHttpUrl, isConfigured } = useServerUrl()
  const stats = ref<ServerStats | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  let pollInterval: number | null = null

  const fetchStats = async () => {
    if (!isConfigured.value) {
      error.value = 'Server not configured'
      return
    }

    try {
      isLoading.value = true
      const baseUrl = getHttpUrl()
      const response = await fetch(`${baseUrl}/ws/stats`, {
        headers: {
          'Accept': 'application/json',
          'ngrok-skip-browser-warning': 'true'
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch WebSocket stats')
      }

      const data: ServerStats = await response.json()
      stats.value = data
      error.value = null
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally {
      isLoading.value = false
    }
  }

  const startPolling = (interval = 5000) => {
    stopPolling()
    fetchStats()
    pollInterval = window.setInterval(fetchStats, interval)
  }

  const stopPolling = () => {
    if (pollInterval) {
      clearInterval(pollInterval)
      pollInterval = null
    }
  }

  onUnmounted(() => {
    stopPolling()
  })

  return {
    stats,
    isLoading,
    error,
    fetchStats,
    startPolling,
    stopPolling
  }
}