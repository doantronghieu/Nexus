// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	compatibilityDate: "2024-11-01",
	devtools: { enabled: true },

	// Build modules
	modules: ["@nuxtjs/tailwindcss"],
	// Server configuration for HTTPS
	server: {
		host: "0.0.0.0", // Allow external access
		port: 3000, // Nuxt server port
		https: {
			key: "./certs/key.pem", // SSL key for Nuxt server
			cert: "./certs/cert.pem", // SSL certificate for Nuxt server
		},
	},

	// Development server configuration (same as above but specific to dev mode)
	devServer: {
		host: "0.0.0.0",
		port: 3000,
		https: {
			key: "./certs/key.pem",
			cert: "./certs/cert.pem",
		},
	},

	// Add this to ensure client-side only rendering for camera component
	ssr: false,

	vite: {
		server: {
			https: true,
			host: true, // needed for mobile access
			hmr: {
				protocol: "wss",
			},
		},
	},

	app: {
		head: {
			title: "WebRTC Camera Demo",
			meta: [
				{ charset: "utf-8" },
				{ name: "viewport", content: "width=device-width, initial-scale=1" },
      ],
      
		},
	},

	// Build configuration
	build: {
		transpile: ["vue-websocket"],
	},
});