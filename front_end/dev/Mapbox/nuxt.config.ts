// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	compatibilityDate: "2024-11-01",
	devtools: { enabled: true },
	modules: ["nuxt-mapbox"],
	mapbox: {
    accessToken: process.env.NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN
  },
	css: [
		"mapbox-gl/dist/mapbox-gl.css", // Add this line
		"assets/css/main.css"
	],
});