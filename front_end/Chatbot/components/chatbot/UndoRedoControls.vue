<template>
  <div class="flex justify-end space-x-2 p-2">
    <button
      @click="$emit('undo')"
      class="text-gray-500 hover:text-gray-700 focus:outline-none"
      :disabled="!canUndo"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
      </svg>
    </button>
    <button
      @click="$emit('redo')"
      class="text-gray-500 hover:text-gray-700 focus:outline-none"
      :disabled="!canRedo"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMessagesStore } from '~/stores/chatbot/messages'

const messagesStore = useMessagesStore()

const canUndo = computed(() => messagesStore.canUndo)
const canRedo = computed(() => messagesStore.canRedo)

defineEmits(['undo', 'redo'])
</script>