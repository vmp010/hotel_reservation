// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['bootstrap/dist/css/bootstrap.min.css'],
  vite: {
    define: {
      'process.env.DEBUG': false,
    },
  }
})
