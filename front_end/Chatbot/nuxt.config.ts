export default defineNuxtConfig({
	compatibilityDate: "2024-04-03",
	devtools: { enabled: true },
	modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt"],
	runtimeConfig: {
		public: {
			OPENAI_API_KEY: process.env.NUXT_PUBLIC_OPENAI_API_KEY || "",
			PORT_FAST_API: process.env.NUXT_PUBLIC_PORT_FAST_API || "8765",
		},
		OPENAI_API_KEY: process.env.NUXT_OPENAI_API_KEY,
		PORT_FAST_API: process.env.NUXT_PORT_FAST_API,
	},
	css: ["~/assets/css/main.css"],
	build: {
		transpile: ["marked"],
	},
	plugins: [
		"~/plugins/openai.js",
		"~/plugins/ivyedge.js",
		"~/plugins/pinia-persist.js",
	],
});