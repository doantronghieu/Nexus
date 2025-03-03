// app.vue
<template>
  <div>
    <NuxtPage />
    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from '~/components/ui/notification/ToastContainer.vue'
</script>

<style>
:root {
  --primary-color: #2196F3;
  --error-color: #f44336;
  --success-color: #4CAF50;
  --warning-color: #FFC107;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
  line-height: 1.5;
  color: #333;
}

button {
  font-family: inherit;
}

/* Focus styles */
:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Scrollbar styles */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  body {
    color: #e0e0e0;
  }

  ::-webkit-scrollbar-track {
    background: #2d2d2d;
  }

  ::-webkit-scrollbar-thumb {
    background: #666;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #888;
  }
}
</style>