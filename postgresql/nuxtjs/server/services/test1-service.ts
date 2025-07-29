import { Test1 } from "../modles/entities/test1";
import { CreateRequest } from "../modles/requests/create-request";
import { DeleteRequest } from "../modles/requests/delete-request";
import { UpdateRequest } from "../modles/requests/update-request";
import { CreateResponse } from "../modles/responses/create-response";
import { GetByIdResponse } from "../modles/responses/get-by-id-response";
import { MessageResponse, Response, setInternalServerErrorResponse, setNoContentResponse, setNotFoundResponse, setOkResponse } from "../modles/responses/response";
import { UpdateResponse } from "../modles/responses/update-response";
import { Test1Repository } from "../repositories/test1-repository";
import { pool } from "../utils/postgres-util";

export class Test1Service {
    static async create(createRequest: CreateRequest): Promise<Response<CreateResponse | null>> {
        let client = await pool.connect()
        try {
            await client.query("BEGIN")
            let test1: Test1 = {
                test: createRequest.test
            }
            let result = await Test1Repository.create(client, test1)
            if (result.rowCount != 1) {
                return setInternalServerErrorResponse()
            }
            test1.id = result.rows[0].id
            await client.query("COMMIT")
            let createResponse: CreateResponse = {
                id: test1.id,
                test: test1.test
            }
            return setOkResponse(createResponse)
        } catch(e) {
            await client.query("ROLLBACK")
            console.log("error:", e);
            return setInternalServerErrorResponse()
        } finally {
            if (client) {
                client.release()
            }
        }
    }

    static async getById(id: number): Promise<Response<GetByIdResponse | null>> {
        try {
            const client = await pool.connect()
            const result = await Test1Repository.getById(client, id)
            if (result.rowCount === 0) {
                return setNotFoundResponse("cannot find test1 with id: " + id)
            }
            const getByIdResponse: GetByIdResponse = {
                id: result.rows[0].id,
                test: result.rows[0].test
            }
            return setOkResponse(getByIdResponse)
        } catch(e) {
            console.log("errror:", e)
            return setInternalServerErrorResponse()
        }
    }

    static async update(updateRequest: UpdateRequest): Promise<Response<UpdateResponse | null>> {
        let client = await pool.connect()
        try {
            await client.query("BEGIN")
            const test1: Test1 = {
                id: updateRequest.id,
                test: updateRequest.test
            }
            const result = await Test1Repository.update(client, test1)
            if (result.rowCount != 1) {
                return setInternalServerErrorResponse()
            }
            await client.query("COMMIT")
            const updateResponse: UpdateResponse = {
                id: test1.id,
                test: test1.test
            }
            return setOkResponse(updateResponse)
        } catch(e) {
            await client.query("ROLLBACK")
            console.log("error:", e)
            return setInternalServerErrorResponse()
        } finally {
            if (client) {
                client.release()
            }
        }
    }

    static async delete(deleteRequest: DeleteRequest): Promise<Response<MessageResponse | null>> {
        let client = await pool.connect()
        try {
            await client.query("BEGIN")
            const result = await Test1Repository.delete(client, deleteRequest.id)
            if (result.rowCount != 1) {
                return setInternalServerErrorResponse()
            }
            await client.query("COMMIT")
            return setNoContentResponse(null)
        } catch(e) {
            await client.query("ROLLBACK")
            console.log("error:",e)
            return setInternalServerErrorResponse()
        } finally {
            if (client) {
                client.release()
            }
        }
    }
}