
<template>
  <div class="app-container">
    <nav class="nav-bar">
      <div class="nav-content">
        <div class="nav-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['nav-button', { active: currentTab === tab.id }]"
            @click="currentTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <div v-show="currentTab === 'camera'" class="tab-panel">
        <WebRTCCamera />
      </div>

      <div v-show="currentTab === 'status'" class="tab-panel">
        <StatusPanel />
      </div>

      <div v-show="currentTab === 'settings'" class="tab-panel">
        <SettingsPanel />
      </div>

      <div v-show="currentTab === 'manager'" class="tab-panel">
        <ManagerDashboard />
      </div>
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'
import WebRTCCamera from '~/components/WebRTCCamera.vue'
import StatusPanel from '~/components/dashboard/Status.vue'
import SettingsPanel from '~/components/dashboard/Settings.vue'
import ManagerDashboard from '~/components/dashboard/Manager.vue'

export default {
  name: 'IndexPage',
  components: {
    WebRTCCamera,
    StatusPanel,
    SettingsPanel,
    ManagerDashboard,
  },

  setup() {
    const currentTab = ref('camera')
    const tabs = [
      { id: 'camera', label: 'Camera' },
      { id: 'status', label: 'Status' },
      { id: 'settings', label: 'Settings' },
      { id: 'manager', label: 'Manager' },
    ]

    return {
      currentTab,
      tabs
    }
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #121212;
  color: #FFFFFF;
}

.nav-bar {
  background: #1E1E1E;
  padding: 16px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
}

.nav-tabs {
  display: flex;
  gap: 8px;
}

.nav-button {
  padding: 8px 16px;
  background: none;
  border: none;
  color: #FFFFFF;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.nav-button:hover {
  background: #2D2D2D;
}

.nav-button.active {
  background: #2196F3;
  color: #FFFFFF;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

.tab-panel {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Light theme */
@media (prefers-color-scheme: light) {
  .app-container {
    background: #F5F5F5;
    color: #000000;
  }

  .nav-bar {
    background: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .nav-button {
    color: #424242;
  }

  .nav-button:hover {
    background: #E0E0E0;
  }

  .nav-button.active {
    background: #2196F3;
    color: #FFFFFF;
  }
}

/* Mobile responsive */
@media (max-width: 768px) {
  .nav-bar {
    padding: 12px;
  }

  .nav-button {
    font-size: 14px;
    padding: 8px 12px;
  }

  .main-content {
    padding: 16px 8px;
  }
}
</style>
