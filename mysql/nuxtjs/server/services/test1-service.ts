// import { PoolConnection } from "mysql2"
import { Test1Repository } from "../repositories/test1-repository"
import { pool } from "../utils/mysql_util"
import { Response, MessageResponse, setCreatedResponse, setInternalServerErrorResponse, setNoContentResponse, setOkResponse } from "../models/responses/response"
import { PoolConnection } from "mysql2/promise"

export class Test1Service {
    static async getById(id: Number): Promise<Response<Test1 | null>> {
        try {
            const test1 = await Test1Repository.getById(pool, id)
            return setOkResponse(test1)
        } catch(e) {
            return setInternalServerErrorResponse()
        }
    }

    static async create(test1Request: Test1Request): Promise<Response<Test1 | null>> {
        // let connection: PoolConnection | null = null;
        // try {
        //     connection = await pool.getConnection()

        //     // const test1 = 
        //     // await Test1Repository.create(connection, )
        // } catch(e) {
        //     return setInternalServerErrorHttpResponse()
        // }

        let connection: PoolConnection | null = null;
        try {
            connection = await pool.getConnection();
            await connection.beginTransaction();
            const test1: Test1 = {
                // id: 0,
                test: test1Request.test
            }
            const result = await Test1Repository.create(connection, test1)
            // console.log("result:", result.affectedRows, result.insertId)
            if (result.affectedRows !== 1) {
                return setInternalServerErrorResponse()
            }
            test1.id = result.insertId
            await connection.commit();
            return setCreatedResponse(test1)
        } catch(e) {
            console.log("e", e)
            if (connection) {
                await connection.rollback(); // Rollback jika ada error
            }
            return setInternalServerErrorResponse()
        } finally {
            if (connection) {
                connection.release(); // Selalu release koneksi kembali ke pool
            }
        }
    }

    static async update(test1UpdateRequest: Test1UpdateRequest): Promise<Response<Test1 | null>> {
        let connection: PoolConnection | null = null;
        try {
            connection = await pool.getConnection();
            await connection.beginTransaction();
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
            console.log("e", e)
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
            connection = await pool.getConnection();
            await connection.beginTransaction();
            const result = await Test1Repository.delete(connection, test1DeleteRequest.id)
            if (result.affectedRows !== 1) {
                return setInternalServerErrorResponse()
            }
            await connection.commit()
            return setNoContentResponse("successfully delete test 1")
        } catch(e) {
            console.log("e", e)
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
