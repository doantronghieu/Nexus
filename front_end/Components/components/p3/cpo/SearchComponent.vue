<template>
  <div class="search-container">
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Enter Charger ID, Customer ID or name" 
        @input="handleSearch"
        class="search-input"
      />
      <button class="search-button" @click="handleSearch">Search</button>
    </div>
    <div v-if="recentSearches.length > 0" class="recent-searches">
      <div class="recent-searches-title">Recent searches:</div>
      <div class="recent-searches-list">
        <div 
          v-for="(search, index) in recentSearches" 
          :key="index" 
          class="recent-search-item"
          @click="setSearch(search)"
        >
          {{ search }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchComponent',
  data() {
    return {
      searchQuery: '',
      recentSearches: ['CH-2023-10045', 'CUST-78945', 'Anna Schmidt']
    }
  },
  methods: {
    handleSearch() {
      if (!this.searchQuery) return;
      
      // Emit search event to parent component
      this.$emit('search', this.searchQuery);
      
      // Add to recent searches if not already there
      if (!this.recentSearches.includes(this.searchQuery)) {
        this.recentSearches.unshift(this.searchQuery);
        if (this.recentSearches.length > 5) {
          this.recentSearches.pop();
        }
      }
    },
    setSearch(search) {
      this.searchQuery = search;
      this.handleSearch();
    }
  }
}
</script>

<style scoped>
.search-container {
  margin-bottom: 1rem;
  width: 100%;
}

.search-box {
  display: flex;
  width: 100%;
}

.search-input {
  flex-grow: 1;
  padding: 0.5rem 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px 0 0 4px;
  font-size: 1rem;
}

.search-button {
  padding: 0.5rem 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.recent-searches {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.recent-searches-title {
  font-size: 0.75rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.recent-searches-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.recent-search-item {
  padding: 0.25rem 0.5rem;
  background-color: #e9ecef;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
}

.recent-search-item:hover {
  background-color: #dee2e6;
}
</style>
