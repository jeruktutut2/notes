import pkg from 'pg';
const { Pool } = pkg;

export const pool = new Pool({
    host: "localhost",
    port: 5432,
    user: "postgres",
    password: "12345",
    database: "test1",
    max: 10, // max 10 pool connection
    idleTimeoutMillis: 30000, // 30 seconds idle time
    connectionTimeoutMillis: 2000, // 2 second timeout for getting new connection
});