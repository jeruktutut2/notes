import { Test1Service } from "~/server/services/test1-service"

export default defineEventHandler(async (event) => {
    const id = parseInt(event.context.params.id) as number
    if (!Number.isInteger(id)) {
        setResponseStatus(event, 400)
        return {data: null, errors: {message: "id is not a number"}}
    }
    const response = await Test1Service.getById(id)
    setResponseStatus(event, response.httpStatusCode)
    return response.BodyResponse
})