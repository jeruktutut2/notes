// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  nitro: {
    devProxy: {
      '/file/stat': {
        target: 'http://localhost:8080/file/stat',
        changeOrigin: true,
        prependPath: true,
      },
      '/file/download': {
        target: 'http://localhost:8080/file/download',
        changeOrigin: true,
        prependPath: true,
      },
    }
  },

  modules: ['@nuxtjs/tailwindcss']
})