import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const id = parseInt(event.context.params.id) as number
    if (!Number.isInteger(id)) {
        throw createError({
            statusCode: 400,
            statusMessage: 'ID should be an integer',
        })
    }
    const httpResponse = await Test1Service.getById(id)
    setResponseStatus(event, httpResponse.httpStatusCode)
    return httpResponse.response
})