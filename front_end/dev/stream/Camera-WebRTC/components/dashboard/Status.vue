<template>
  <div class="status-panel">
    <!-- Connection Status -->
    <section class="status-section">
      <h2 class="section-title">System Status</h2>
      <div class="status-grid">
        <div class="status-item">
          <h3 class="status-label">API Server</h3>
          <div class="status-value" :class="apiStatus.status">
            {{ apiStatus.message }}
          </div>
          <div class="status-debug" v-if="showDebug">
            Attempting: {{ getFastAPIBaseUrl() }}
          </div>
        </div>
        <div class="status-item">
          <h3 class="status-label">WebSocket</h3>
          <div class="status-value" :class="wsConnectionState">
            {{ wsConnectionMessage }}
          </div>
          <div class="status-debug" v-if="showDebug">
            Attempting: {{ getFastAPIWSBaseUrl() }}
          </div>
        </div>
      </div>
    </section>

    <!-- System Stats -->
    <section class="status-section">
      <h2 class="section-title">System Statistics</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">CPU Usage</div>
          <div class="stat-value">{{ systemStats?.cpu_usage ?? 0 }}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Memory Usage</div>
          <div class="stat-value">{{ systemStats?.memory_usage ?? 0 }}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Active Streams</div>
          <div class="stat-value">{{ systemStats?.active_streams ?? 0 }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Total Frames</div>
          <div class="stat-value">{{ systemStats?.total_frames ?? 0 }}</div>
        </div>
      </div>
    </section>

    <!-- Server Info -->
    <section class="status-section">
      <h2 class="section-title">Server Information</h2>
      <div class="info-grid">
        <div class="info-card">
          <div class="info-label">Version</div>
          <div class="info-value">{{ healthInfo?.version ?? '1.0.0' }}</div>
        </div>
        <div class="info-card">
          <div class="info-label">Uptime</div>
          <div class="info-value">{{ formatUptime(healthInfo?.uptime ?? 0) }}</div>
        </div>
      </div>
    </section>

    <!-- Debug Toggle -->
    <div class="actions">
      <button 
        @click="refreshStatus" 
        :disabled="isLoading" 
        class="refresh-button"
      >
        {{ isLoading ? 'Refreshing...' : 'Refresh Status' }}
      </button>
      <button 
        @click="showDebug = !showDebug" 
        class="debug-button"
      >
        {{ showDebug ? 'Hide Debug Info' : 'Show Debug Info' }}
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useConfig } from '~/composables/useConfig'

export default {
  name: 'StatusPanel',
  
  setup() {
    const { 
      getFastAPIBaseUrl, 
      getFastAPIWSBaseUrl,
      setupWebSocket,
      addMessageHandler,
      removeMessageHandler,
      connectionStatus,
      sendMessage
    } = useConfig()
    
    const healthInfo = ref(null)
    const systemStats = ref(null)
    const isLoading = ref(false)
    const showDebug = ref(false)
    
    const apiStatus = ref({ status: 'unknown', message: 'Checking...' })

    const wsConnectionState = computed(() => 
      connectionStatus.value?.state || 'unknown'
    )
    
    const wsConnectionMessage = computed(() => 
      connectionStatus.value?.message || 'Checking connection...'
    )

    const handleServerMessage = (data) => {
      console.log('Received server message:', data)
      if (data.type === 'health_update') {
        healthInfo.value = {
          version: data.version,
          uptime: data.uptime,
          ws_connections: data.ws_connections
        }
        systemStats.value = data.system_stats
      }
    }

    const requestStatusUpdate = () => {
      sendMessage({
        type: 'status_request'
      })
    }

    const checkHealth = async () => {
      try {
        const url = getFastAPIBaseUrl() + '/health'
        const response = await fetch(url)
        if (response.ok) {
          healthInfo.value = await response.json()
          apiStatus.value = { status: 'connected', message: 'Connected' }
        } else {
          apiStatus.value = { status: 'error', message: 'Error' }
        }
      } catch (err) {
        apiStatus.value = { status: 'error', message: 'Unreachable' }
        console.error('Health check error:', err)
      }
    }

    const refreshStatus = async () => {
      isLoading.value = true
      await checkHealth()
      requestStatusUpdate()
      isLoading.value = false
    }

    const formatUptime = (seconds) => {
      const days = Math.floor(seconds / 86400)
      const hours = Math.floor((seconds % 86400) / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      return `${days}d ${hours}h ${minutes}m`
    }

    onMounted(() => {
      // Initialize WebSocket connection if not already established
      setupWebSocket()
      
      // Register message handler
      addMessageHandler(handleServerMessage)
      
      // Initial status check
      refreshStatus()
      
      // Set up periodic status refresh
      const statusInterval = setInterval(refreshStatus, 30000)
      
      onUnmounted(() => {
        clearInterval(statusInterval)
        removeMessageHandler(handleServerMessage)
      })
    })

    return {
      healthInfo,
      systemStats,
      apiStatus,
      wsConnectionState,
      wsConnectionMessage,
      isLoading,
      showDebug,
      getFastAPIBaseUrl,
      getFastAPIWSBaseUrl,
      refreshStatus,
      formatUptime
    }
  }
}
</script>

<style scoped>
.status-panel {
  background: #1E1E1E;
  border-radius: 8px;
  padding: 24px;
}

.status-section {
  margin-bottom: 32px;
}

.section-title {
  color: #FFFFFF;
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 16px;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.status-item {
  background: #2D2D2D;
  padding: 16px;
  border-radius: 8px;
}

.status-label {
  color: #FFFFFF;
  font-size: 14px;
  font-weight: normal;
  margin-bottom: 8px;
}

.status-value {
  font-size: 16px;
  font-weight: 500;
}

.status-value.connected {
  color: #4CAF50;
}

.status-value.error {
  color: #F44336;
}

.status-value.unknown {
  color: #9E9E9E;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.stat-card {
  background: #2D2D2D;
  padding: 16px;
  border-radius: 8px;
}

.stat-label {
  color: #FFFFFF;
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  color: #FFFFFF;
  font-size: 20px;
  font-weight: 500;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-card {
  background: #2D2D2D;
  padding: 16px;
  border-radius: 8px;
}

.info-label {
  color: #FFFFFF;
  font-size: 14px;
  margin-bottom: 8px;
}

.info-value {
  color: #FFFFFF;
  font-size: 20px;
  font-weight: 500;
}

.actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.refresh-button {
  background: #2196F3;
  color: #FFFFFF;
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.refresh-button:hover:not(:disabled) {
  background: #1976D2;
}

.refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Light theme */
@media (prefers-color-scheme: light) {
  .status-panel {
    background: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .section-title {
    color: #000000;
  }

  .status-item,
  .stat-card,
  .info-card {
    background: #F5F5F5;
  }

  .status-label,
  .stat-label,
  .info-label {
    color: #424242;
  }

  .status-value,
  .stat-value,
  .info-value {
    color: #000000;
  }

  .status-value.connected {
    color: #2E7D32;
  }

  .status-value.error {
    color: #D32F2F;
  }

  .status-value.unknown {
    color: #757575;
  }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .status-panel {
    padding: 16px;
    border-radius: 0;
  }

  .status-grid,
  .stats-grid,
  .info-grid {
    grid-template-columns: 1fr;
  }

  .actions {
    justify-content: stretch;
  }

  .refresh-button {
    width: 100%;
  }
}

.debug-button {
  background: #404040;
  color: #FFFFFF;
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  margin-left: 8px;
}

.status-debug {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  word-break: break-all;
}

/* Light theme */
@media (prefers-color-scheme: light) {
  .debug-button {
    background: #E0E0E0;
    color: #424242;
  }

  .status-debug {
    color: #999;
  }
}
</style>