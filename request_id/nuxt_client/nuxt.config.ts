// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  nitro: {
    devProxy: {
      '/request-id': {
        target: 'http://localhost:8080/request-id',
        changeOrigin: true,
        prependPath: true,
      },
    }
  }
})