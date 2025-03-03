// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true,
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/tailwindcss",
    "@pinia/nuxt",
  ],
  nitro: {
    preset: "node-server",
  },
  app: {
    baseURL: "/ui/",
    buildAssetsDir: "/_nuxt/",
    head: {
      script: [],
    },
  },
  pinia: {
    autoImports: ['defineStore', 'storeToRefs'],
  },
});