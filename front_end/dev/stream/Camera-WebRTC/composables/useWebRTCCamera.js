import { ref, reactive } from "vue";
import { useConfig } from "./useConfig";

/**
 * Handles camera frame capture and upload functionality
 * @returns {Object} Camera frame controls and state
 */
export function useWebRTCCamera() {
	const { getFramesEndpoint } = useConfig();
	const error = ref(null);

	// Reactive state for camera operations
	const state = reactive({
		isUploading: false,
		lastUploadTime: 0,
		uploadCount: 0,
		quality: 0.8,
		maxWidth: 1280,
		maxHeight: 720,
		totalUploaded: 0,
	});

	// Frame capture queue
	let uploadQueue = [];
	let isProcessingQueue = false;
	let lastFrameTime = 0;
	const MIN_FRAME_INTERVAL = 100; // Minimum time between frames (ms)

	/**
	 * Processes the upload queue with rate limiting
	 */
	async function processUploadQueue() {
		if (isProcessingQueue || uploadQueue.length === 0) return;

		isProcessingQueue = true;

		try {
			while (uploadQueue.length > 0) {
				const { blob, clientId, resolve, reject } = uploadQueue[0];

				// Rate limiting check
				const now = Date.now();
				const timeSinceLastUpload = now - state.lastUploadTime;

				if (timeSinceLastUpload < 1000) {
					// Within the same second
					if (state.uploadCount >= 30) {
						// Max 30 fps
						await new Promise((resolve) =>
							setTimeout(resolve, 1000 - timeSinceLastUpload)
						);
						continue;
					}
					state.uploadCount++;
				} else {
					state.uploadCount = 1;
					state.lastUploadTime = now;
				}

				try {
					const result = await performUpload(blob, clientId);
					state.totalUploaded++;
					resolve(result);
				} catch (err) {
					reject(err);
				}

				uploadQueue.shift(); // Remove processed item
			}
		} finally {
			isProcessingQueue = false;
		}
	}

	/**
	 * Performs the actual frame upload
	 * @param {Blob} blob - Frame data
	 * @param {string} clientId - Client identifier
	 * @returns {Promise} Upload response
	 */
	async function performUpload(blob, clientId) {
		try {
			const formData = new FormData();
			formData.append("frame", blob, "frame.jpg");

			const response = await fetch("/api/fastapi-camera/frame", {
				method: "POST",
				body: formData,
				headers: {
					"X-Client-ID": clientId,
				},
			});

			if (!response.ok) {
				throw new Error(`Failed to upload frame: ${response.statusText}`);
			}

			return await response.json();
		} catch (err) {
			error.value = err.message || "Failed to upload frame";
			throw err;
		}
	}

	/**
	 * Captures and optimizes a video frame
	 * @param {HTMLVideoElement} videoElement - Source video element
	 * @returns {Promise<Blob>} Optimized frame blob
	 */
	async function captureOptimizedFrame(videoElement) {
		const canvas = document.createElement("canvas");
		const ctx = canvas.getContext("2d");

		// Calculate optimal dimensions
		let width = videoElement.videoWidth;
		let height = videoElement.videoHeight;
		const aspectRatio = width / height;

		if (width > state.maxWidth) {
			width = state.maxWidth;
			height = width / aspectRatio;
		}
		if (height > state.maxHeight) {
			height = state.maxHeight;
			width = height * aspectRatio;
		}

		canvas.width = width;
		canvas.height = height;

		// Draw and optimize
		ctx.drawImage(videoElement, 0, 0, width, height);

		// Adaptive quality based on upload success rate
		if (state.totalUploaded > 0 && error.value) {
			state.quality = Math.max(0.5, state.quality - 0.1); // Reduce quality if errors
		} else if (state.totalUploaded % 10 === 0) {
			state.quality = Math.min(0.9, state.quality + 0.1); // Gradually improve quality
		}

		return new Promise((resolve) => {
			canvas.toBlob((blob) => resolve(blob), "image/jpeg", state.quality);
		});
	}

	/**
	 * Queues a frame for upload with debouncing
	 * @param {Blob} frame - Frame data to upload
	 * @param {string} clientId - Client identifier
	 * @returns {Promise} Upload result
	 */
	async function uploadFrame(frame, clientId) {
		const now = Date.now();
		if (now - lastFrameTime < MIN_FRAME_INTERVAL) {
			return null; // Skip frame if too soon
		}
		lastFrameTime = now;

		return new Promise((resolve, reject) => {
			uploadQueue.push({ blob: frame, clientId, resolve, reject });
			processUploadQueue();
		});
	}

	/**
	 * Cleans up resources
	 */
	function cleanup() {
		uploadQueue = [];
		state.isUploading = false;
		state.uploadCount = 0;
		error.value = null;
	}

	return {
		uploadFrame,
		captureOptimizedFrame,
		cleanup,
		error,
		state,
		isUploading: computed(() => state.isUploading),
	};
}
