import { ref, onUnmounted } from "vue";

/**
 * Handles camera device access and control
 * @returns {Object} Camera controls and state
 */
export function useCamera() {
	const stream = ref(null);
	const devices = ref([]);
	const currentDevice = ref(null);
	const error = ref(null);

	/**
	 * Enumerates available camera devices
	 */
	async function getCameraDevices() {
		try {
			// Request initial camera access to get permissions
			const tempStream = await navigator.mediaDevices.getUserMedia({
				video: true,
			});
			tempStream.getTracks().forEach((track) => track.stop());

			const deviceList = await navigator.mediaDevices.enumerateDevices();
			devices.value = deviceList.filter(
				(device) => device.kind === "videoinput"
			);

			if (devices.value.length > 0) {
				currentDevice.value = devices.value[0].deviceId;
			}
		} catch (err) {
			error.value = "Failed to get camera devices";
			console.error(err);
		}
	}

	/**
	 * Starts the camera stream
	 * @param {string} deviceId - Optional device ID to use
	 */
	async function startCamera(deviceId) {
		try {
			const constraints = {
				video: {
					deviceId: deviceId ? { exact: deviceId } : undefined,
					width: { ideal: 1280 },
					height: { ideal: 720 },
				},
				audio: true,
			};

			stream.value = await navigator.mediaDevices.getUserMedia(constraints);
			currentDevice.value = deviceId || null;
			error.value = null;
		} catch (err) {
			error.value = "Failed to start camera";
			console.error(err);
		}
	}

	/**
	 * Switches to a different camera device
	 * @param {string} deviceId - The ID of the device to switch to
	 */
	async function switchCamera(deviceId) {
		if (stream.value) {
			stream.value.getTracks().forEach((track) => track.stop());
		}
		await startCamera(deviceId);
	}

	/**
	 * Stops the camera stream
	 */
	function stopCamera() {
		if (stream.value) {
			stream.value.getTracks().forEach((track) => track.stop());
			stream.value = null;
		}
	}

	onUnmounted(() => {
		stopCamera();
	});

	return {
		stream,
		devices,
		currentDevice,
		error,
		getCameraDevices,
		startCamera,
		switchCamera,
		stopCamera,
	};
}
