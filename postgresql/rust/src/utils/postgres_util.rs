use std::time::Duration;

use chrono::Local;
use sqlx::{postgres::PgPoolOptions, Pool, Postgres, Transaction};

pub trait PostgresUtil {
    async fn get_pool(&self) -> &Pool<Postgres>;
    async fn begin(&self) -> Result<Transaction<'static, Postgres>, sqlx::Error>;
    async fn commit(&self, tx: Transaction<'static, Postgres>) -> Result<(), sqlx::Error>;
    async fn rollback(&self, tx: Transaction<'static, Postgres>) -> Result<(), sqlx::Error>;
    async fn close(&self);
}

#[derive(Debug)]
pub struct PostgresUtilImpl {
    pool: Pool<Postgres>
}

impl PostgresUtilImpl {
    pub async fn new() -> PostgresUtilImpl {
        println!("{} postgres: connecting to localhost:5432", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        let postgres_url = format!("postgres://postgres:12345@localhost:5432/test1?application_name=test1");
        let pool = PgPoolOptions::new()
            .max_connections(10)
            .min_connections(5)
            .acquire_timeout(Duration::from_secs(10))
            .max_lifetime(Duration::from_secs(600))
            .idle_timeout(Duration::from_secs(300))
            .connect(&postgres_url)
            .await.expect("cannot connect to localhost:5432");
        println!("{} postgres: connected to localhost:5432", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        PostgresUtilImpl {
            pool: pool
        }

    }
}

impl PostgresUtil for PostgresUtilImpl {
    async fn get_pool(&self) -> &Pool<Postgres> {
        &self.pool
    }

    async fn begin(&self) -> Result<Transaction<'static, Postgres>, sqlx::Error> {
        self.pool.begin().await
    }

    async fn commit(&self, tx: Transaction<'static, Postgres>) -> Result<(), sqlx::Error> {
        tx.commit().await
    }

    async fn rollback(&self, tx: Transaction<'static, Postgres>) -> Result<(), sqlx::Error> {
        tx.rollback().await
    }

    async fn close(&self) {
        println!("{} postgres: closing to localhost:5432", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        self.pool.close().await;
        println!("{} postgres: closed to localhost:5432", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
    }
}