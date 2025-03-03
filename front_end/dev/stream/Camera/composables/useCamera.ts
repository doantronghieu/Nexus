import { ref, onUnmounted } from 'vue'

/**
 * Composable for managing camera device access and stream control
 */
export function useCamera() {
  const stream = ref<MediaStream | null>(null)
  const devices = ref<MediaDeviceInfo[]>([])
  const currentDevice = ref<string | null>(null)
  const error = ref<string | null>(null)

  /**
   * Get list of available camera devices
   */
  async function getCameraDevices() {
    try {
      // Request initial camera access to get permissions
      const tempStream = await navigator.mediaDevices.getUserMedia({ video: true })
      tempStream.getTracks().forEach(track => track.stop())

      const deviceList = await navigator.mediaDevices.enumerateDevices()
      devices.value = deviceList.filter(device => device.kind === 'videoinput')

      if (devices.value.length > 0) {
        currentDevice.value = devices.value[0].deviceId
      }
    } catch (err) {
      error.value = 'Failed to get camera devices'
      console.error('Error getting camera devices:', err)
    }
  }

  /**
   * Start camera stream
   * @param deviceId - Optional specific device ID to use
   */
  async function startCamera(deviceId?: string) {
    try {
      const constraints = {
        video: {
          deviceId: deviceId ? { exact: deviceId } : undefined,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      }

      stream.value = await navigator.mediaDevices.getUserMedia(constraints)
      currentDevice.value = deviceId || null
      error.value = null
    } catch (err) {
      error.value = 'Failed to start camera'
      console.error('Error starting camera:', err)
    }
  }

  /**
   * Switch to a different camera device
   * @param deviceId - ID of the device to switch to
   */
  async function switchCamera(deviceId: string) {
    if (stream.value) {
      stream.value.getTracks().forEach(track => track.stop())
    }
    await startCamera(deviceId)
  }

  /**
   * Stop the camera stream
   */
  function stopCamera() {
    if (stream.value) {
      stream.value.getTracks().forEach(track => track.stop())
      stream.value = null
    }
  }

  onUnmounted(() => {
    stopCamera()
  })

  return {
    stream,
    devices,
    currentDevice,
    error,
    getCameraDevices,
    startCamera,
    switchCamera,
    stopCamera
  }
}