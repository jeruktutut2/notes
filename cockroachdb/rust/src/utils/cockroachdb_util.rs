use std::{sync::{atomic::AtomicUsize, Arc}, time::Duration};

use chrono::Local;
use sqlx::{postgres::PgPoolOptions, Pool, Postgres, Transaction};

pub trait CockroachDbUtil {
    async fn get_pool(&self) -> &Pool<Postgres>;
    async fn begin(&self) -> Result<Transaction<'static, Postgres>, sqlx::Error>;
    async fn commit(&self, tx: Transaction<'static, Postgres>) -> Result<(), sqlx::Error>;
    async fn rollback(&self, tx: Transaction<'static, Postgres>) -> Result<(), sqlx::Error>;
    async fn close(&self);
}

pub struct CockroachDbUtilImpl {
    pool: Pool<Postgres>
}

impl CockroachDbUtilImpl {
    pub async  fn new() -> CockroachDbUtilImpl {
        println!("{} postgres: connecting to localhost:26260", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        let cockroachdb_url = format!("postgres://root:@localhost:26260/test1?application_name=test1");
        let active_conns = Arc::new(AtomicUsize::new(0));
        let counter = active_conns.clone();
        let pool = PgPoolOptions::new()
            .after_connect(move |_conn, _meta| {
                let counter = counter.clone();
                Box::pin(async move {
                    counter.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                    Ok(())
                })
            })
            .max_connections(10)
            .min_connections(5)
            .acquire_timeout(Duration::from_secs(10))
            .max_lifetime(Duration::from_secs(600))
            .idle_timeout(Duration::from_secs(300))
            .connect(&cockroachdb_url)
            .await.expect("cannot connect to localhost:26260");
        println!("{} postgres: connected to localhost:5432", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        
        CockroachDbUtilImpl {
            pool: pool
        }
    }
}

impl CockroachDbUtil for CockroachDbUtilImpl {
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
        println!("{} postgres: closing to localhost:26260", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        self.pool.close().await;
        println!("{} postgres: closed to localhost:26260", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
    }
}