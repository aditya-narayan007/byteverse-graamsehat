import pg from 'pg';
import dotenv from 'dotenv';

dotenv.config();

if (!process.env.DATABASE_URL) {
  throw new Error('[DB] DATABASE_URL is not defined in environment variables');
}

const { Pool } = pg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production'
    ? { rejectUnauthorized: false }
    : false,
  max: 10,
  idleTimeoutMillis:     30_000,
  connectionTimeoutMillis: 5_000,
  statement_timeout:     15_000,
  query_timeout:         15_000,
});

pool.on('error', (err) => {
  console.error('[DB] Unexpected pool client error:', err.message);
});

export const query = async (text, params) => {
  try {
    return await pool.query(text, params);
  } catch (err) {
    console.error('[DB QUERY ERROR]', err.message);
    console.error('Query:', text);
    throw err;
  }
};
export const getClient = () => pool.connect();
export default pool;

export async function checkDbConnection() {
  try {
    const client = await pool.connect();
    await client.query('SELECT 1');
    client.release();
    console.log('[DB] Connection healthy');
  } catch (err) {
    console.error('[DB] Connection failed:', err.message);
    throw err;
  }
}