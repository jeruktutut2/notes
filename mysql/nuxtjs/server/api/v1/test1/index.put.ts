import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const test1UpdateRequest = await readBody<Test1UpdateRequest>(event)
    const httpResponse = await Test1Service.update(test1UpdateRequest)
    setResponseStatus(event, httpResponse.httpStatusCode)
    return httpResponse
})