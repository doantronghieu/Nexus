<template>
  <div class="settings-panel">
    <!-- Camera Settings -->
    <section class="settings-section">
      <h2 class="section-title">Camera Settings</h2>
      
      <div class="settings-grid">
        <div class="setting-item">
          <label class="setting-label">Default Video Quality</label>
          <select v-model="settings.camera.quality" class="setting-input">
            <option value="high">High (1280x720)</option>
            <option value="medium">Medium (854x480)</option>
            <option value="low">Low (640x360)</option>
          </select>
        </div>

        <div class="setting-item">
          <label class="setting-label">Frame Rate</label>
          <select v-model="settings.camera.frameRate" class="setting-input">
            <option value="30">30 FPS</option>
            <option value="24">24 FPS</option>
            <option value="15">15 FPS</option>
          </select>
        </div>

        <div class="setting-item">
          <label class="setting-label">Auto Start Camera</label>
          <div class="toggle-switch">
            <input 
              type="checkbox" 
              v-model="settings.camera.autoStart"
              id="autoStart"
            >
            <label for="autoStart"></label>
          </div>
        </div>

        <div class="setting-item">
          <label class="setting-label">Mirror Mode</label>
          <select v-model="settings.camera.mirror" class="setting-input">
            <option value="none">No Mirror</option>
            <option value="user">Front Camera Only</option>
            <option value="always">Always Mirror</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Connection Settings -->
    <section class="settings-section">
      <h2 class="section-title">Connection Settings</h2>
      
      <div class="settings-grid">
        <div class="setting-item">
          <label class="setting-label">Server URL</label>
          <input 
            type="text" 
            v-model="settings.server.url"
            class="setting-input"
            :placeholder="defaultServerUrl"
            @focus="handleServerUrlFocus"
          >
        </div>

        <div class="setting-item">
          <label class="setting-label">WebSocket URL</label>
          <input 
            type="text" 
            v-model="settings.server.wsUrl"
            class="setting-input"
            :placeholder="defaultWsUrl"
            @focus="handleWsUrlFocus"
          >
        </div>

        <div class="setting-item">
          <label class="setting-label">Auto Reconnect</label>
          <div class="toggle-switch">
            <input 
              type="checkbox" 
              v-model="settings.server.autoReconnect"
              id="autoReconnect"
            >
            <label for="autoReconnect"></label>
          </div>
        </div>

        <div class="setting-item">
          <label class="setting-label">Max Reconnect Attempts</label>
          <input 
            type="number" 
            v-model.number="settings.server.maxReconnectAttempts"
            class="setting-input"
            min="1"
            max="10"
          >
        </div>
      </div>
    </section>

    <!-- Storage Settings -->
    <section class="settings-section">
      <h2 class="section-title">Storage Settings</h2>
      
      <div class="settings-grid">
        <div class="setting-item">
          <label class="setting-label">Save Snapshots</label>
          <div class="toggle-switch">
            <input 
              type="checkbox" 
              v-model="settings.storage.saveSnapshots"
              id="saveSnapshots"
            >
            <label for="saveSnapshots"></label>
          </div>
        </div>

        <div class="setting-item">
          <label class="setting-label">Snapshot Quality</label>
          <input 
            type="range" 
            v-model.number="settings.storage.snapshotQuality"
            class="setting-slider"
            min="0"
            max="1"
            step="0.1"
          >
          <div class="slider-value">{{ Math.round(settings.storage.snapshotQuality * 100) }}%</div>
        </div>

        <div class="setting-item">
          <label class="setting-label">Auto Clear Cache</label>
          <div class="toggle-switch">
            <input 
              type="checkbox" 
              v-model="settings.storage.autoClear"
              id="autoClear"
            >
            <label for="autoClear"></label>
          </div>
        </div>

        <div class="setting-item">
          <label class="setting-label">Cache Duration (hours)</label>
          <input 
            type="number" 
            v-model.number="settings.storage.cacheDuration"
            class="setting-input"
            min="1"
            max="72"
          >
        </div>
      </div>
    </section>

    <!-- Advanced Settings -->
    <section class="settings-section">
      <h2 class="section-title">Advanced Settings</h2>
      
      <div class="settings-grid">
        <div class="setting-item">
          <label class="setting-label">Debug Mode</label>
          <div class="toggle-switch">
            <input 
              type="checkbox" 
              v-model="settings.advanced.debugMode"
              id="debugMode"
            >
            <label for="debugMode"></label>
          </div>
        </div>

        <div class="setting-item">
          <label class="setting-label">Log Level</label>
          <select 
            v-model="settings.advanced.logLevel"
            class="setting-input"
            :disabled="!settings.advanced.debugMode"
          >
            <option value="error">Error</option>
            <option value="warn">Warning</option>
            <option value="info">Info</option>
            <option value="debug">Debug</option>
          </select>
        </div>

        <div class="setting-item">
          <label class="setting-label">STUN Server</label>
          <input 
            type="text" 
            v-model="settings.advanced.stunServer"
            class="setting-input"
            placeholder="stun:stun.l.google.com:19302"
          >
        </div>

        <div class="setting-item">
          <label class="setting-label">Enable Statistics</label>
          <div class="toggle-switch">
            <input 
              type="checkbox" 
              v-model="settings.advanced.enableStats"
              id="enableStats"
            >
            <label for="enableStats"></label>
          </div>
        </div>
      </div>
    </section>

    <!-- Actions -->
    <div class="settings-actions">
      <button 
        @click="resetSettings" 
        class="button button-secondary"
        :disabled="isResetting"
      >
        Reset to Defaults
      </button>
      <button 
        @click="saveSettings" 
        class="button button-primary"
        :disabled="!hasChanges || isSaving"
      >
        {{ isSaving ? 'Saving...' : 'Save Changes' }}
      </button>
    </div>

    <!-- Notification -->
    <div 
      v-if="notification" 
      :class="['notification', `notification-${notification.type}`]"
    >
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useConfig } from '~/composables/useConfig'

const DEFAULT_SETTINGS = {
  camera: {
    quality: 'high',
    frameRate: '30',
    autoStart: false,
    mirror: 'user'
  },
  server: {
    url: '',
    wsUrl: '',
    autoReconnect: true,
    maxReconnectAttempts: 5
  },
  storage: {
    saveSnapshots: true,
    snapshotQuality: 0.8,
    autoClear: true,
    cacheDuration: 24
  },
  advanced: {
    debugMode: false,
    logLevel: 'error',
    stunServer: 'stun:stun.l.google.com:19302',
    enableStats: true
  }
}

export default {
  name: 'SettingsPanel',

  setup() {
    const settings = ref({ ...DEFAULT_SETTINGS })
    const originalSettings = ref(null)
    const notification = ref(null)
    const isSaving = ref(false)
    const isResetting = ref(false)
    const { getFastAPIBaseUrl, getFastAPIWSBaseUrl, config } = useConfig()

    const defaultServerUrl = computed(() => getFastAPIBaseUrl())
    const defaultWsUrl = computed(() => getFastAPIWSBaseUrl())

    const hasChanges = computed(() => {
      if (!originalSettings.value) return false
      return JSON.stringify(settings.value) !== JSON.stringify(originalSettings.value)
    })

    const loadSettings = () => {
      try {
        const savedSettings = localStorage.getItem('camera-settings')
        if (savedSettings) {
          const parsed = JSON.parse(savedSettings)
          settings.value = {
            ...DEFAULT_SETTINGS,
            ...parsed
          }
        } else {
          // If no saved settings, use the current server URLs from config
          settings.value.server.url = defaultServerUrl.value
          settings.value.server.wsUrl = defaultWsUrl.value
        }
        originalSettings.value = JSON.parse(JSON.stringify(settings.value))
      } catch (err) {
        console.error('Failed to load settings:', err)
        showNotification('Failed to load settings', 'error')
      }
    }

    const handleServerUrlFocus = () => {
      if (!settings.value.server.url) {
        settings.value.server.url = defaultServerUrl.value
      }
    }

    const handleWsUrlFocus = () => {
      if (!settings.value.server.wsUrl) {
        settings.value.server.wsUrl = defaultWsUrl.value
      }
    }

    const saveSettings = async () => {
      try {
        isSaving.value = true
        localStorage.setItem('camera-settings', JSON.stringify(settings.value))
        originalSettings.value = JSON.parse(JSON.stringify(settings.value))
        
        // Update the config with new server URLs if they've changed
        if (settings.value.server.url) {
          const url = new URL(settings.value.server.url)
          config.fastAPI.host = url.hostname
          config.fastAPI.port = url.port
          config.fastAPI.protocol = url.protocol.replace(':', '')
        }
        
        if (settings.value.server.wsUrl) {
          const wsUrl = new URL(settings.value.server.wsUrl)
          config.fastAPI.wsProtocol = wsUrl.protocol.replace(':', '')
        }
        
        showNotification('Settings saved successfully', 'success')
      } catch (err) {
        console.error('Failed to save settings:', err)
        showNotification('Failed to save settings', 'error')
      } finally {
        isSaving.value = false
      }
    }

    const resetSettings = async () => {
      try {
        isResetting.value = true
        settings.value = { ...DEFAULT_SETTINGS }
        settings.value.server.url = defaultServerUrl.value
        settings.value.server.wsUrl = defaultWsUrl.value
        await saveSettings()
        showNotification('Settings reset to defaults', 'success')
      } finally {
        isResetting.value = false
      }
    }

    const showNotification = (message, type = 'info') => {
      notification.value = { message, type }
      setTimeout(() => {
        notification.value = null
      }, 3000)
    }

    // Watch for config changes and update settings if needed
    watch(() => config.fastAPI.host, (newHost) => {
      if (settings.value.server.url) {
        const url = new URL(settings.value.server.url)
        if (url.hostname !== newHost) {
          settings.value.server.url = defaultServerUrl.value
          settings.value.server.wsUrl = defaultWsUrl.value
        }
      }
    })

    onMounted(() => {
      loadSettings()
    })

    return {
      settings,
      hasChanges,
      notification,
      isSaving,
      isResetting,
      defaultServerUrl,
      defaultWsUrl,
      saveSettings,
      resetSettings,
      handleServerUrlFocus,
      handleWsUrlFocus
    }
  }
}
</script>

<style scoped>
.settings-panel {
  background: #1E1E1E;
  border-radius: 8px;
  padding: 24px;
  color: #FFFFFF;
}

.settings-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 16px;
  color: #FFFFFF;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.setting-label {
  font-size: 14px;
  color: #FFFFFF;
}

.setting-input {
  padding: 8px 12px;
  background: #2D2D2D;
  border: 1px solid #404040;
  border-radius: 4px;
  color: #FFFFFF;
  font-size: 14px;
}

.setting-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-switch label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #404040;
  border-radius: 24px;
  transition: 0.4s;
}

.toggle-switch label:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: #FFFFFF;
  border-radius: 50%;
  transition: 0.4s;
}

.toggle-switch input:checked + label {
  background-color: #2196F3;
}

.toggle-switch input:checked + label:before {
  transform: translateX(26px);
}

/* Slider */
.setting-slider {
  width: 100%;
  height: 4px;
  background: #404040;
  border-radius: 2px;
  appearance: none;
}

.setting-slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  background: #2196F3;
  border-radius: 50%;
  cursor: pointer;
}

.slider-value {
  text-align: center;
  font-size: 14px;
  color: #FFFFFF;
  margin-top: 4px;
}

/* Action Buttons */
.settings-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
}

.button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.button-primary {
  background: #2196F3;
  color: #FFFFFF;
}

.button-secondary {
  background: #404040;
  color: #FFFFFF;
}

.button-primary:not(:disabled):hover {
  background: #1976D2;
}

.button-secondary:not(:disabled):hover {
  background: #4A4A4A;
}

/* Notification */
.notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 14px;
  animation: slideIn 0.3s ease-out;
}

.notification-success {
  background: #43A047;
  color: #FFFFFF;
}

.notification-error {
  background: #D32F2F;
  color: #FFFFFF;
}

.notification-info {
  background: #1976D2;
  color: #FFFFFF;
}

@keyframes slideIn {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Light Theme */
@media (prefers-color-scheme: light) {
  .settings-panel {
    background: #FFFFFF;
    color: #000000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .section-title {
    color: #000000;
  }

  .setting-label {
    color: #424242;
  }

  .setting-input {
    background: #F5F5F5;
    border-color: #E0E0E0;
    color: #000000;
  }

  .setting-input:focus {
    border-color: #2196F3;
    background: #FFFFFF;
  }

  .toggle-switch label {
    background-color: #E0E0E0;
  }

  .toggle-switch input:checked + label {
    background-color: #2196F3;
  }

  .setting-slider {
    background: #E0E0E0;
  }

  .setting-slider::-webkit-slider-thumb {
    background: #2196F3;
  }

  .slider-value {
    color: #424242;
  }

  .button-secondary {
    background: #E0E0E0;
    color: #424242;
  }

  .button-secondary:hover:not(:disabled) {
    background: #BDBDBD;
  }
}

/* Mobile Responsive Design */
@media (max-width: 768px) {
  .settings-panel {
    padding: 16px;
    border-radius: 0;
  }

  .settings-grid {
    grid-template-columns: 1fr;
  }

  .setting-item {
    gap: 6px;
  }

  .settings-actions {
    flex-direction: column-reverse;
    margin-top: 24px;
  }

  .button {
    width: 100%;
    padding: 12px;
  }

  .notification {
    bottom: 16px;
    right: 16px;
    left: 16px;
    text-align: center;
  }
}

/* Accessibility Improvements */
@media (prefers-reduced-motion: reduce) {
  .notification {
    animation: none;
  }

  .toggle-switch label,
  .toggle-switch label:before {
    transition: none;
  }
}

/* High Contrast Mode */
@media (forced-colors: active) {
  .toggle-switch input:checked + label {
    background-color: Highlight;
  }

  .button-primary {
    background-color: Highlight;
    color: HighlightText;
  }

  .setting-input:focus {
    outline: 2px solid Highlight;
  }
}
</style>