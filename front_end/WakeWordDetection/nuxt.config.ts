export default defineNuxtConfig({
	modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt"],

	runtimeConfig: {
		public: {
			apiHost: process.env.NUXT_PUBLIC_API_HOST || "jarvis-clone.servebeer.com",
			apiPort: process.env.NUXT_PUBLIC_API_PORT || "5000",
			wsProtocol: process.env.NUXT_PUBLIC_WS_PROTOCOL || "ws",
			httpProtocol: process.env.NUXT_PUBLIC_HTTP_PROTOCOL || "http",
		},
	},

	// Auto-import components
	components: {
		dirs: ["~/components"],
	},

	app: {
		head: {
			title: "Wake Word Detection",
			meta: [
				{ charset: "utf-8" },
				{ name: "viewport", content: "width=device-width, initial-scale=1" },
			],
		},
	},
});