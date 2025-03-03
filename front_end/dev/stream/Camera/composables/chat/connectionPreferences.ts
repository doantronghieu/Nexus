import { ref } from 'vue'
import type { NameSelectionMode } from '../types'

const predefinedNames = [
  'Observer_1',
  'Observer_2',
  'Guest_A',
  'Guest_B',
  'Viewer_X',
  'Viewer_Y',
  'User_Alpha',
  'User_Beta'
]

export const useConnectionPreferences = () => {
  const nameSelectionMode = ref<NameSelectionMode>('server')
  const selectedPresetName = ref('')
  const customName = ref('')
  const showValidation = ref(false)

  const getSelectedName = () => {
    switch (nameSelectionMode.value) {
      case 'preset':
        return selectedPresetName.value || null
      case 'custom':
        return customName.value.trim() || null
      case 'server':
      default:
        return null
    }
  }

  const validateInput = () => {
    showValidation.value = true
    
    if (nameSelectionMode.value === 'custom' && !customName.value.trim()) {
      return false
    }
    
    if (nameSelectionMode.value === 'preset' && !selectedPresetName.value) {
      return false
    }
    
    return true
  }

  const resetValidation = () => {
    showValidation.value = false
  }

  const resetPreferences = () => {
    nameSelectionMode.value = 'server'
    selectedPresetName.value = ''
    customName.value = ''
    showValidation.value = false
  }

  return {
    // State
    nameSelectionMode,
    selectedPresetName,
    customName,
    showValidation,
    predefinedNames,

    // Methods
    getSelectedName,
    validateInput,
    resetValidation,
    resetPreferences
  }
}