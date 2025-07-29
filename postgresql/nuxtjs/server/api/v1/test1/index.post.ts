import { CreateRequest } from "~/server/modles/requests/create-request"
import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const createRequest = await readBody<CreateRequest>(event)
    const response = await Test1Service.create(createRequest)
    setResponseStatus(event, response.httpStatusCode)
    return response.BodyResponse
})