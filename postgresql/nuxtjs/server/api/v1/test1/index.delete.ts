import { DeleteRequest } from "~/server/modles/requests/delete-request"
import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const deleteRequest = await readBody<DeleteRequest>(event)
    const response = await Test1Service.delete(deleteRequest)
    setResponseStatus(event, response.httpStatusCode)
    return response.httpStatusCode
})