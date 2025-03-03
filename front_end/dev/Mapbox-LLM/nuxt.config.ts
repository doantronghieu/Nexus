// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	compatibilityDate: "2024-11-01",
	devtools: { enabled: true },
	modules: ["nuxt-mapbox", "@nuxtjs/google-fonts"],
	mapbox: {
		accessToken: process.env.NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN,
	},
	css: [
		"mapbox-gl/dist/mapbox-gl.css", // Add this line
		"assets/css/main.css",
	],
	runtimeConfig: {
		public: {
			apiBaseUrl: "http://localhost:6001",
			mapboxAccessToken: process.env.NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN,
		},
	},
	nitro: {
		devProxy: {
			"/api": {
				target: "http://localhost:6001",
				changeOrigin: true,
			},
		},
	},
	googleFonts: {
		families: {
			Inter: [300, 400, 500, 600, 700],
			"Space+Grotesk": [300, 400, 500, 600, 700],
			'Outfit': [300, 400, 500, 600, 700],
			'JetBrains+Mono': [300, 400, 500, 600, 700],
			"Material+Icons": true,
		},
	},
	app: {
		head: {
			link: [
				{
					rel: "stylesheet",
					href: "https://fonts.googleapis.com/icon?family=Material+Icons",
				},
			],
		},
	},
});