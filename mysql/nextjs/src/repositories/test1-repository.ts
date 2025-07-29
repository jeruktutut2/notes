import { Test1 } from "@/models/entities/test1"
import { Pool, PoolConnection } from 'mysql2/promise';
import { ResultSetHeader, RowDataPacket } from 'mysql2';

export class Test1Repository {
    static async getById(pool: Pool, id: number): Promise<Test1 | null> {
        const [rows] = await pool.query<Test1[] & RowDataPacket[]>("SELECT id, test FROM test1 WHERE id = ?;", [id])
        return rows.length > 0 ? rows[0] : null
    }

    static async create(connection: PoolConnection, test1: Test1):Promise<ResultSetHeader> {
        const [result] = await connection.query<ResultSetHeader>("INSERT INTO test1(test) VALUES(?);", [test1.test])
        return result
    }

    static async update(connection: PoolConnection, test1: Test1):Promise<ResultSetHeader> {
        const [result] = await connection.query<ResultSetHeader>("UPDATE test1 SET test = ? WHERE id = ?;", [test1.test, test1.id])
        return result
    }

    static async delete(connection: PoolConnection, id: number):Promise<ResultSetHeader> {
        const [result] = await connection.query<ResultSetHeader>("DELETE FROM test1 WHERE id = ?;", [id])
        return result
    }
}