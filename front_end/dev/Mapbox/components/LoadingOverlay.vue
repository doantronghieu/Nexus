<template>
  <div class="loading-overlay">
    <div class="loading-text">Getting your location...</div>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(35, 55, 75, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-text {
  color: white;
  font-size: 1.5rem;
  font-family: monospace;
}
</style>