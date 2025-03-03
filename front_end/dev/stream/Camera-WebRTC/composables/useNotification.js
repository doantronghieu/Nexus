// composables/useNotification.js
import { ref, markRaw } from 'vue'

const notifications = ref([])
let notificationId = 0

export function useNotification() {
  const show = ({
    message,
    type = 'info',
    duration = 3000,
    position = 'bottom-right',
    dismissible = true
  }) => {
    const id = ++notificationId
    
    notifications.value.push({
      id,
      message,
      type,
      duration,
      position,
      dismissible
    })

    return id
  }

  const dismiss = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const success = (message, options = {}) => {
    return show({ message, type: 'success', ...options })
  }

  const error = (message, options = {}) => {
    return show({ message, type: 'error', ...options })
  }

  const info = (message, options = {}) => {
    return show({ message, type: 'info', ...options })
  }

  const warning = (message, options = {}) => {
    return show({ message, type: 'warning', ...options })
  }

  return {
    notifications,
    show,
    dismiss,
    success,
    error,
    info,
    warning
  }
}