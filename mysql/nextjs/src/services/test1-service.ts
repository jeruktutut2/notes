import { Test1 } from "@/models/entities/test1";
import { MessageResponse, Response, setCreatedResponse, setInternalServerErrorResponse, setNoContentResponse, setOkResponse } from "@/models/responses/response";
import { pool } from "@/utils/mysql-util";
import { Test1Repository } from "../repositories/test1-repository"
import { Test1CreateRequest, Test1DeleteRequest, Test1UpdateRequest } from "@/models/requests/test1-request";
import { PoolConnection } from "mysql2/promise";

export class Test1Service {
    static async getById(id: number): Promise<Response<Test1 | null>> {
        try {
            const test1 = await Test1Repository.getById(pool, id)
            return setOkResponse(test1)
        } catch(e) {
            console.log(e)
            return setInternalServerErrorResponse()
        }
    }

    static async create(test1CreateRequest: Test1CreateRequest): Promise<Response<Test1 | null>> {
        let connection: PoolConnection | null = null
        try {
            connection = await pool.getConnection()
            await connection.beginTransaction()
            const test1: Test1 = {
                test: test1CreateRequest.test
            }
            const result = await Test1Repository.create(connection, test1)
            if (result.affectedRows !== 1) {
                return setInternalServerErrorResponse()
            }
            test1.id = result.insertId
            await connection.commit()
            return setCreatedResponse(test1)
        } catch(e) {
            console.log("e:", e)
            if (connection) {
                await connection.rollback()
            }
            return setInternalServerErrorResponse()
        } finally {
            if (connection) {
                connection.release()
            }
        }
    }

    static async update(test1UpdateRequest: Test1UpdateRequest): Promise<Response<Test1 | null>> {
        let connection: PoolConnection | null = null
        try {
            connection = await pool.getConnection()
            await connection.beginTransaction()
            const test1: Test1 = {
                id: test1UpdateRequest.id,
                test: test1UpdateRequest.test
            }
            const result = await Test1Repository.update(connection, test1)
            if (result.affectedRows !== 1) {
                return setInternalServerErrorResponse()
            }
            await connection.commit()
            return setOkResponse(test1)
        } catch(e) {
            console.log(e)
            if (connection) {
                await connection.rollback()
            }
            return setInternalServerErrorResponse()
        } finally {
            if (connection) {
                connection.release()
            }
        }
    }

    static async delete(test1DeleteRequest: Test1DeleteRequest): Promise<Response<MessageResponse | null>> {
        let connection: PoolConnection | null = null;
        try {
            connection = await pool.getConnection()
            await connection.beginTransaction()
            const result = await Test1Repository.delete(connection, test1DeleteRequest.id)
            if (result.affectedRows !== 1) {
                return setInternalServerErrorResponse()
            }
            await connection.commit()
            return setNoContentResponse("successfully delete test 1")
        } catch(e) {
            console.log(e)
            if (connection) {
                await connection.rollback()
            }
            return setInternalServerErrorResponse()
        } finally {
            if (connection) {
                connection.release()
            }
        }
    }
}