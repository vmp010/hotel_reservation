// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['bootstrap/dist/css/bootstrap.min.css'],
  runtimeConfig: {
    public: {
      // Default API base; override at runtime via env var NUXT_PUBLIC_API_BASE
      apiBase: 'http://localhost:8000'
    }
  },
  vite: {
    define: {
      'process.env.DEBUG': false,
    },
  }
})
