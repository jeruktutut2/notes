use sqlx::{Postgres, Transaction};

use crate::models::entities::test1::Test1;

pub trait Test1Repository {
    async fn create_without_tx(&self, pool: &sqlx::PgPool, test1: &Test1) -> Result<(), sqlx::Error>;
    async fn sleep_without_tx(&self, pool: &sqlx::PgPool) -> Result<(), sqlx::Error>;
    async fn create_with_tx(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<(), sqlx::Error>;
    async fn sleep_with_tx(&self, tx: &mut Transaction<'_, Postgres>) -> Result<(), sqlx::Error>;
}

pub struct Test1RepositoryImpl{}

impl Test1RepositoryImpl {
    pub fn new() -> Test1RepositoryImpl {
        Test1RepositoryImpl {  }
    }
}

impl Test1Repository for Test1RepositoryImpl {
    async fn create_without_tx(&self, pool: &sqlx::PgPool, test1: &Test1) -> Result<(), sqlx::Error> {
        let _ = sqlx::query("INSERT INTO test1(test) VALUES($1);")
            .bind(&test1.test)
            .execute(pool)
            .await?;
        Ok(())
    }

    async fn sleep_without_tx(&self, pool: &sqlx::PgPool) -> Result<(), sqlx::Error> {
        let _ = sqlx::query("SELECT pg_sleep(3);")
            .execute(pool)
            .await?;
        Ok(())
    }

    async fn create_with_tx(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<(), sqlx::Error> {
        let _ = sqlx::query("INSERT INTO test1(test) VALUES($1);")
        .bind(&test1.test)
        .execute(&mut **tx)
        .await?;
        Ok(())
    }

    async fn sleep_with_tx(&self, tx: &mut Transaction<'_, Postgres>) -> Result<(), sqlx::Error> {
        let _ = sqlx::query("SELECT pg_sleep(3);")
        .execute(&mut **tx)
        .await?;
        Ok(())
    }
}