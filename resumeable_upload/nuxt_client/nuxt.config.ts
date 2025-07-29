// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  nitro: {
    devProxy: {
      '/file/upload': {
        target: 'http://localhost:8080/file/upload',
        changeOrigin: true,
        prependPath: true,
      },
      '/file/merge': {
        target: 'http://localhost:8080/file/merge',
        changeOrigin: true,
        prependPath: true,
      },
      '/file/check-file': {
        target: 'http://localhost:8080/file/check-file',
        changeOrigin: true,
        prependPath: true,
      },
      '/file/upload-merge': {
        target: 'http://localhost:8080/file/upload-merge',
        changeOrigin: true,
        prependPath: true,
      },
    }
  }
})
