<template>
  <div class="flex items-center space-x-2 p-3 bg-gray-700 bg-opacity-50 rounded-lg max-w-fit">
    <div class="typing-dot"></div>
    <div class="typing-dot" style="animation-delay: 0.2s"></div>
    <div class="typing-dot" style="animation-delay: 0.4s"></div>
  </div>
</template>

<style scoped>
.typing-dot {
  width: 8px;
  height: 8px;
  background: #4fd1c5;
  border-radius: 50%;
  animation: typingAnimation 1.4s infinite ease-in-out;
}

@keyframes typingAnimation {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-10px); }
}
</style>