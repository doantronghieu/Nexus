<template>
  <section class="info-section customer-section">
    <div class="section-header">
      <div class="section-title">
        <span class="section-icon">👤</span>
        Customer
      </div>
      <div class="membership-badge">PREMIUM</div>
    </div>
    
    <div class="customer-details">
      <div class="customer-name">{{ customer.name }}</div>
      <div class="customer-id">{{ customer.id }}</div>
      
      <div class="details-grid">
        <div class="details-group">
          <div class="details-label">Contact</div>
          <div class="details-value">{{ customer.email }}</div>
          <div class="details-value">{{ customer.phone }}</div>
        </div>
        
        <div class="details-group">
          <div class="details-label">Language</div>
          <div class="details-value">{{ customer.language }}</div>
        </div>
        
        <div class="details-group" v-if="customer.vehicle">
          <div class="details-label">Vehicle</div>
          <div class="details-value">{{ customer.vehicle.model }} ({{ customer.vehicle.year }})</div>
          <div class="details-value license-plate">{{ customer.vehicle.license_plate }}</div>
        </div>
        
        <div class="details-group">
          <div class="details-label">Last Charging</div>
          <div class="details-value">{{ formatDate(customer.last_charging) }}</div>
        </div>
        
        <div class="details-group">
          <div class="details-label">Member Since</div>
          <div class="details-value">{{ formatDate(customer.account_created) }}</div>
        </div>
      </div>
      
      <div class="section-footer">
        <button class="link-button">Charging History</button>
        <button class="link-button">View Messages</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'CustomerInfoCard',
  props: {
    customer: {
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

.membership-badge {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  background-color: var(--primary-light);
  color: var(--primary-blue);
  border-radius: 12px;
  text-transform: uppercase;
}

.customer-details {
  padding: 12px;
}

.customer-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 2px;
}

.customer-id {
  font-size: 12px;
  color: var(--neutral-600);
  margin-bottom: 12px;
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

.license-plate {
  font-family: monospace;
}

.section-footer {
  display: flex;
  gap: 12px;
  padding-top: 8px;
}

.link-button {
  background: none;
  color: var(--primary-blue);
  padding: 6px 0;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.link-button:hover {
  text-decoration: underline;
}
</style>
