// components/ui/notification/ToastContainer.vue
<template>
  <div>
    <div v-for="position in positions" :key="position">
      <TransitionGroup
        tag="div"
        class="fixed z-50 w-full max-w-sm pointer-events-none"
        :class="getPositionClasses(position)"
        enter-active-class="transition ease-out duration-300"
        enter-from-class="transform translate-y-2 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform translate-y-2 opacity-0"
      >
        <Toast
          v-for="notification in getNotificationsByPosition(position)"
          :key="notification.id"
          v-bind="notification"
          class="pointer-events-auto mb-2"
        />
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useNotification } from '~/composables/useNotification'
import Toast from './Toast.vue'

const { notifications } = useNotification()

const positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right']

const getPositionClasses = (position) => {
  switch (position) {
    case 'top-left':
      return 'top-4 left-4'
    case 'top-right':
      return 'top-4 right-4'
    case 'bottom-left':
      return 'bottom-4 left-4'
    case 'bottom-right':
      return 'bottom-4 right-4'
    default:
      return 'bottom-4 right-4'
  }
}

const getNotificationsByPosition = (position) => {
  return notifications.value.filter(n => n.position === position || (!n.position && position === 'bottom-right'))
}
</script>