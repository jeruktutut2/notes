import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const test1 = await Test1Service.getById(1)
    setResponseStatus(event, test1.httpStatusCode)
    return {
        "test1": test1
    }
})