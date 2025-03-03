// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	compatibilityDate: '2024-11-01',
	devtools: { enabled: true },
	modules: ['@nuxtjs/tailwindcss', 'nuxt-mapbox'],
	css: [
	  'mapbox-gl/dist/mapbox-gl.css'
	],
	runtimeConfig: {
	  public: {
		mapboxAccessToken: process.env.NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN
	  }
	},
	mapbox: {
	  accessToken: process.env.NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN
	}
  })