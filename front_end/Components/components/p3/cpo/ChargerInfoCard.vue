<template>
  <section class="info-section charger-section">
    <div class="section-header">
      <div class="section-title">
        <span class="section-icon">🔌</span>
        Charger
      </div>
      <div class="status-badge online">{{ charger.status }}</div>
    </div>
    
    <div class="charger-details">
      <div class="details-grid">
        <div class="details-group">
          <div class="details-label">ID</div>
          <div class="details-value">{{ charger.id }}</div>
        </div>
        
        <div class="details-group">
          <div class="details-label">Model</div>
          <div class="details-value">{{ charger.model }}</div>
        </div>
        
        <div class="details-group" v-if="charger.location">
          <div class="details-label">Location</div>
          <div class="details-value">{{ charger.location.address }}</div>
          <div class="details-value">{{ charger.location.country }}</div>
        </div>
        
        <div class="details-group">
          <div class="details-label">Backend</div>
          <div class="details-value">{{ charger.backend_system }}</div>
        </div>
        
        <div class="details-group">
          <div class="details-label">Maintained</div>
          <div class="details-value">{{ formatDate(charger.last_maintenance) }}</div>
        </div>
        
        <div class="details-group" v-if="charger.connectors && charger.connectors.length">
          <div class="details-label">Connectors</div>
          <div class="connectors-list">
            <span v-for="(connector, index) in charger.connectors" :key="index" class="connector-item">
              {{ connector.type }}
              <span class="connector-status">{{ connector.status }}</span>
            </span>
          </div>
        </div>
      </div>
      
      <div class="section-footer">
        <button class="secondary-button">Run Diagnostics</button>
        <button class="secondary-button">Restart Charger</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ChargerInfoCard',
  props: {
    charger: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    }
  }
}
</script>

<style scoped>
.info-section {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background-color: var(--neutral-100);
  border-bottom: 1px solid var(--neutral-200);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  font-size: 14px;
}

.section-icon {
  font-size: 16px;
}

.status-badge {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: lowercase;
}

.status-badge.online {
  background-color: rgba(0, 200, 83, 0.1);
  color: var(--success-green);
}

.status-badge.offline {
  background-color: rgba(240, 62, 62, 0.1);
  color: var(--error-red);
}

.charger-details {
  padding: 12px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px 24px;
  margin-bottom: 16px;
}

.details-label {
  font-size: 12px;
  color: var(--neutral-600);
  margin-bottom: 4px;
}

.details-value {
  font-size: 13px;
  color: var(--neutral-800);
}

.connectors-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
}

.connector-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  background-color: var(--neutral-100);
  border-radius: 4px;
  font-size: 12px;
}

.connector-status {
  font-size: 11px;
  color: var(--neutral-600);
}

.section-footer {
  display: flex;
  gap: 12px;
  padding-top: 8px;
}

.secondary-button {
  background-color: var(--neutral-100);
  color: var(--neutral-800);
  border: 1px solid var(--neutral-300);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-button:hover {
  background-color: var(--neutral-200);
}
</style>
