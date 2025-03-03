import { useConfig } from "~/composables/useConfig";

/**
 * Handles frame upload to FastAPI server
 * @param {FormData} formData - The frame data
 * @param {string} clientId - Client identifier
 * @returns {Promise} Upload response
 */
async function handleFrameUpload(formData, clientId = "default") {
	const { getFramesEndpoint } = useConfig();

	try {
		if (!formData) {
			throw createError({
				statusCode: 400,
				message: "No form data received",
			});
		}

		const response = await fetch(getFramesEndpoint(clientId), {
			method: "POST",
			body: formData,
		});

		if (!response.ok) {
			throw new Error(`FastAPI responded with status: ${response.status}`);
		}

		const data = await response.json();
		console.log(`Frame uploaded successfully for client: ${clientId}`);
		return data;
	} catch (error) {
		console.error(`Frame upload failed for client ${clientId}:`, error);
		throw createError({
			statusCode: error instanceof Error ? 500 : 400,
			message:
				error instanceof Error ? error.message : "Unknown error occurred",
		});
	}
}

// Route handlers
export const GET = defineEventHandler(async (event) => {
	const url = event.path;

	if (url === "/api/fastapi-camera/devices") {
		return { status: "This will be handled client-side" };
	}

	throw createError({
		statusCode: 404,
		statusMessage: "Not Found",
	});
});

export const POST = defineEventHandler(async (event) => {
	const url = event.path;

	if (url === "/api/fastapi-camera/frame") {
		const formData = await readMultipartFormData(event);
		const clientId = event.headers.get("x-client-id") || "default";
		return await handleFrameUpload(formData, clientId);
	}

	throw createError({
		statusCode: 404,
		statusMessage: "Not Found",
	});
});
