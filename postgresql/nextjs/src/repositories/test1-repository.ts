import { PoolClient } from 'pg';
import { Test1 } from '../models/entities/test1';

export class Test1Repository {
    static async create(client: PoolClient, test1: Test1) {
        const result = await client.query("INSERT INTO test1(test) VALUES($1) RETURNING id;", [test1.test])
        return result
    }

    static async getById(client: PoolClient, id: number) {
        const result = await client.query("SELECT id, test FROM test1 WHERE id = $1;", [id])
        return result
    }

    static async update(client: PoolClient, test1: Test1) {
        const result = await client.query("UPDATE test1 SET test = $1 WHERE id = $2;", [test1.test, test1.id])
        return result
    }

    static async delete(client: PoolClient, id: number) {
        const result = await client.query("DELETE FROM test1 WHERE id = $1;", [id])
        return result
    }
}