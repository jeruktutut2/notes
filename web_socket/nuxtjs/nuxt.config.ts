// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  nitro: {
    routeRules: {
      "/ws": {
        proxy: "ws://localhost:8080/ws"
      },
      "/send-message": {
        proxy: "ws://localhost:8080/send-message"
      }
    }
  }
})
