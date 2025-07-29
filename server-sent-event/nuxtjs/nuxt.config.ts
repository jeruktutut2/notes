// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  // runtimeConfig: {
  //   public: {
  //     sseBase: "http://localhost:8080"
  //   }
  // },
  nitro: {
    routeRules: {
      "/sse/**": {
        proxy: "http://localhost:8080/sse/**"
      }
    }
  }
})
