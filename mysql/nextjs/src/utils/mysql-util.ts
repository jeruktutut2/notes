import mysql from 'mysql2/promise';

export const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '12345',
    port: '3309',
    database: 'test1',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
})