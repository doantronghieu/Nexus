import { defineStore } from 'pinia'
import { useServerStore } from './server'
import type { ServerStats } from '@/composables/types'

let pollInterval: number | null = null

export const useWebSocketStatsStore = defineStore('websocketStats', {
  state: () => ({
    stats: null as ServerStats | null,
    isLoading: false,
    error: null as string | null,
    isPolling: false,
    pollInterval: 5000, // 5 seconds default
  }),

  actions: {
    async fetchStats(): Promise<boolean> {
      const serverStore = useServerStore()
      
      if (!serverStore.isConfigured) {
        this.error = 'Server not configured'
        return false
      }

      try {
        this.isLoading = true
        const response = await fetch(`${serverStore.getHttpUrl}/ws/stats`, {
          headers: {
            'Accept': 'application/json',
            'ngrok-skip-browser-warning': 'true'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to fetch WebSocket stats')
        }

        const data: ServerStats = await response.json()
        this.stats = data
        this.error = null
        return true
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Unknown error'
        return false
      } finally {
        this.isLoading = false
      }
    },

    async startAutoRefresh(): Promise<boolean> {
      // First attempt to fetch stats
      const success = await this.fetchStats()
      if (!success) {
        return false
      }

      // If successful, start polling
      this.startPolling()
      return true
    },

    startPolling() {
      this.stopPolling()
      this.isPolling = true
      pollInterval = window.setInterval(() => {
        this.fetchStats()
      }, this.pollInterval)
    },

    stopPolling() {
      if (pollInterval) {
        clearInterval(pollInterval)
        pollInterval = null
      }
      this.isPolling = false
    },

    togglePolling() {
      if (this.isPolling) {
        this.stopPolling()
      } else {
        this.startPolling()
      }
    }
  },

  persist: {
    paths: ['isPolling']
  }
})