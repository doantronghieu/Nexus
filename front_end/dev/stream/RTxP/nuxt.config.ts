// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: true },

  modules: [
    '@nuxtjs/tailwindcss'
  ],

  app: {
    head: {
      title: 'Camera Stream',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      wsPath: process.env.WS_PATH || 'ws://localhost:3000'
    }
  },

  nitro: {
    devProxy: {
      '/api/': {
        target: 'http://localhost:3000/api',
        changeOrigin: true,
        prependPath: true
      }
    }
  },

  compatibilityDate: '2025-01-06'
})