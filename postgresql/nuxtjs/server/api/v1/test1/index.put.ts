import { UpdateRequest } from "~/server/modles/requests/update-request"
import { UpdateResponse } from "~/server/modles/responses/update-response"
import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const updateRequest = await readBody<UpdateRequest>(event)
    const response = await Test1Service.update(updateRequest)
    setResponseStatus(event, response.httpStatusCode)
    return response.BodyResponse
})