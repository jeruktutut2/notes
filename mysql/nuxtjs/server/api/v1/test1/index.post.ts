import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const test1Request = await readBody<Test1Request>(event)
    const httpResponse = await Test1Service.create(test1Request)
    setResponseStatus(event, httpResponse.httpStatusCode)
    return httpResponse
})