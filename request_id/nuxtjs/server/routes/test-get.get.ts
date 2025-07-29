export default defineEventHandler(async (event) => {
    return {
        "test": event.context.uuid
    }
})