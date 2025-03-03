<template>
  <div
    @click="toggleChat"
    class="fixed bottom-6 right-6 w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center cursor-pointer hover:bg-blue-600 transition-colors duration-300 shadow-lg"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      class="w-8 h-8 text-white"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
      />
    </svg>
  </div>
</template>

<script setup>
const emit = defineEmits(['toggle-chat'])

const toggleChat = () => {
  emit('toggle-chat')
}
</script>