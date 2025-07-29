import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const test1DeleteRequest = await readBody<Test1DeleteRequest>(event)
    const httpResponse = await Test1Service.delete(test1DeleteRequest)
    setResponseStatus(event, httpResponse.httpStatusCode)
    return httpResponse
})