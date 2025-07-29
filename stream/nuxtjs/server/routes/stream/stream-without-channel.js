export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const targetUrl = `${config.public.streamBase}/stream/stream-without-channel`
    return await proxyRequest(event, targetUrl)
})