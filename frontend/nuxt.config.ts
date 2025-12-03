// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['bootstrap/dist/css/bootstrap.min.css','bootstrap-icons/font/bootstrap-icons.css'],
  // 🚨 2. 新增這段：引入 Bootstrap 的 JavaScript (負責功能)
  app: {
    head: {
      script: [
        {
          // 這裡使用 CDN 連結，這是最簡單讓 Navbar 動起來的方法
          src: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
          // 設定 bodyClose 確保在 HTML 元素載入後才執行 JS，避免找不到元素
          tagPosition: 'bodyClose' 
        }
      ]
    }
  },
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
