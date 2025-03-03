<template>
  <div class="cpo-dashboard">
    <!-- Header -->
    <header-bar 
      :search-query="searchQuery"
      :selected-language="selectedLanguage"
      @update:search-query="searchQuery = $event"
      @update:selected-language="selectedLanguage = $event"
      @search="handleSearch"
    />
    
    <!-- Main content -->
    <div class="dashboard-content">
      <!-- Left column: Customer & Charger -->
      <div class="left-column">
        <!-- Customer Section -->
        <customer-info-card 
          v-if="customer" 
          :customer="customer" 
        />
        <div v-else class="placeholder-card">Loading customer data...</div>
        
        <!-- Charger Section -->
        <charger-info-card 
          v-if="charger" 
          :charger="charger" 
        />
        <div v-else class="placeholder-card">Loading charger data...</div>
      </div>
      
      <!-- Right column: Issue, Session, Communication -->
      <div class="right-column">
        <!-- Active Issue Section -->
        <active-issue-panel 
          v-if="supportCase" 
          :support-case="supportCase"
          class="issue-panel"
        />
        <div v-else class="placeholder-card">Loading issue data...</div>
        
        <div class="bottom-panels">
          <!-- Charging Session Section -->
          <session-viewer 
            v-if="session" 
            :session="session" 
          />
          <div v-else class="placeholder-card">Loading session data...</div>
          
          <!-- Communication Log Section -->
          <communication-log 
            v-if="supportCase && supportCase.communication_log" 
            :case-id="supportCase?.case_id"
            :initial-entries="supportCase?.communication_log || []"
            @entry-added="handleNewEntry"
          />
          <div v-else class="placeholder-card">Loading communication data...</div>
        </div>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading data...</div>
    </div>
  </div>
</template>

<script>
import HeaderBar from '~/components/p3/cpo/HeaderBar.vue'
import CustomerInfoCard from '~/components/p3/cpo/CustomerInfoCard.vue'
import ChargerInfoCard from '~/components/p3/cpo/ChargerInfoCard.vue'
import ActiveIssuePanel from '~/components/p3/cpo/ActiveIssuePanel.vue'
import SessionViewer from '~/components/p3/cpo/SessionViewer.vue'
import CommunicationLog from '~/components/p3/cpo/CommunicationLog.vue'

export default {
  name: 'CPOSupportDashboard',
  components: {
    HeaderBar,
    CustomerInfoCard,
    ChargerInfoCard,
    ActiveIssuePanel,
    SessionViewer,
    CommunicationLog
  },
  data() {
    return {
      searchQuery: '',
      selectedLanguage: 'en',
      charger: null,
      customer: null,
      supportCase: null,
      session: null,
      isLoading: false,
      errorMessage: ''
    }
  },
  mounted() {
    this.loadDummyData();
  },
  methods: {
    async loadDummyData() {
      this.isLoading = true;
      
      try {
        // Load chargers data
        const chargersResp = await fetch('/assets/data/p3/chargers.json');
        const chargersData = await chargersResp.json();
        if (chargersData && chargersData.length > 0) {
          this.charger = chargersData[0];
        }
        
        // Load customers data
        const customersResp = await fetch('/assets/data/p3/customers.json');
        const customersData = await customersResp.json();
        if (customersData && customersData.length > 0) {
          this.customer = customersData[0];
        }
        
        // Load support cases data
        const casesResp = await fetch('/assets/data/p3/support_cases.json');
        const casesData = await casesResp.json();
        if (casesData && casesData.length > 0) {
          this.supportCase = casesData[0];
        }
        
        // Load charging sessions data
        const sessionsResp = await fetch('/assets/data/p3/charging_sessions.json');
        const sessionsData = await sessionsResp.json();
        if (sessionsData && sessionsData.length > 0) {
          this.session = sessionsData[0];
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        this.errorMessage = 'Failed to load data. Please refresh the page.';
      } finally {
        this.isLoading = false;
      }
    },
    handleSearch() {
      console.log('Searching for:', this.searchQuery);
      // In a real app, this would filter data based on the search query
    },
    handleNewEntry(entry) {
      if (!this.supportCase) return;
      
      if (!this.supportCase.communication_log) {
        this.supportCase.communication_log = [];
      }
      
      this.supportCase.communication_log.push(entry);
    }
  }
}
</script>

<style>
/* CSS Variables - shared across components */
:root {
  --primary-blue: #3563E9;
  --primary-light: #D6E4FF;
  --success-green: #00C853;
  --warning-yellow: #FFB800;
  --error-red: #F03E3E;
  --neutral-100: #F7FAFC;
  --neutral-200: #EDF2F7;
  --neutral-300: #E2E8F0;
  --neutral-400: #CBD5E0;
  --neutral-500: #A0AEC0;
  --neutral-600: #718096;
  --neutral-700: #4A5568;
  --neutral-800: #2D3748;
  --neutral-900: #1A202C;
}
</style>

<style scoped>
/* Reset and base styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Main layout */
.cpo-dashboard {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  font-size: 14px;
  color: var(--neutral-800);
  background-color: var(--neutral-100);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Dashboard content */
.dashboard-content {
  display: flex;
  flex: 1;
  padding: 16px;
  gap: 20px;
  height: calc(100vh - 48px);
  overflow: hidden;
}

.left-column {
  width: 30%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  max-height: 100%;
}

/* Right column layout */
.right-column {
  width: 70%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  max-height: 100%;
}

.issue-panel {
  flex: 0 0 auto;
}

.bottom-panels {
  display: flex;
  gap: 16px;
  min-height: 0; /* Important for proper flex sizing */
  flex: 1;
}

.bottom-panels > * {
  flex: 1;
  min-width: 0; /* Important for preventing overflow */
  max-height: 100%;
}

/* Placeholder card */
.placeholder-card {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 20px;
  color: var(--neutral-600);
  text-align: center;
  font-style: italic;
}

/* Loading overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(53, 99, 233, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-blue);
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-text {
  font-size: 14px;
  color: var(--neutral-700);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive layout */
@media (max-width: 1200px) {
  .dashboard-content {
    flex-direction: column;
  }
  
  .left-column, .right-column {
    width: 100%;
  }

  .bottom-panels {
    flex-direction: column;
  }
}
</style>
