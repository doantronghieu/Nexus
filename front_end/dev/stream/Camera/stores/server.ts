import { defineStore } from 'pinia'

export const predefinedHosts = [
  'key-amoeba-basically.ngrok-free.app',
  'positive-viper-presently.ngrok-free.app',
  'localhost:8000'
] as const

interface HealthCheckResult {
  ok: boolean
  message: string
}

export const useServerStore = defineStore('server', {
  state: () => ({
    serverHost: '',
    protocol: 'http',
    isConfigured: false,
    healthStatus: null as HealthCheckResult | null,
    isLoading: false,
    error: null as string | null
  }),

  getters: {
    getHttpUrl: (state): string => {
      if (!state.serverHost.trim()) {
        return ''
      }
      return `${state.protocol}://${state.serverHost.trim()}`
    },

    getWsUrl: (state): string => {
      if (!state.serverHost.trim()) {
        return ''
      }
      const wsProtocol = state.protocol === 'https' ? 'wss' : 'ws'
      return `${wsProtocol}://${state.serverHost.trim()}/ws`
    }
  },

  actions: {
    setServerInfo(host: string, isSecure = false): void {
      if (host.trim()) {
        this.serverHost = host.trim()
        this.protocol = isSecure ? 'https' : 'http'
        this.isConfigured = true
      } else {
        this.resetServerInfo()
      }
    },

    resetServerInfo(): void {
      this.serverHost = ''
      this.protocol = 'http'
      this.isConfigured = false
      this.healthStatus = null
      this.error = null
    },

    async checkHealth(): Promise<HealthCheckResult> {
      if (!this.isConfigured) {
        return {
          ok: false,
          message: 'Server not configured'
        }
      }

      this.isLoading = true
      this.error = null

      try {
        const response = await fetch(`${this.getHttpUrl}/health`, {
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
        this.healthStatus = {
          ok: response.ok && data.status === 'healthy',
          message: data.status === 'healthy' ? 'Server is healthy' : 'Server health check failed'
        }

        return this.healthStatus

      } catch (error) {
        const result = {
          ok: false,
          message: error instanceof Error ? error.message : 'Unknown error occurred'
        }
        this.healthStatus = result
        this.error = result.message
        return result
      } finally {
        this.isLoading = false
      }
    }
  },

  persist: true
})