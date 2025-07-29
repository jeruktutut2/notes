// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  nitro: {
    devProxy: {
      '/file/stream-audio': {
        target: 'http://localhost:8080/file/stream-audio',
        changeOrigin: true,
        prependPath: true,
      },
    }
  }
})
