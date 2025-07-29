use sqlx::{Postgres, Transaction};

use crate::models::entities::test1::Test1;

pub trait PostgresRepository {
    async fn create(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<i32, sqlx::Error>;
    async fn get_by_id(&self, pool: &sqlx::PgPool, id: i32) -> Result<Test1, sqlx::Error>;
    async fn update(&self, tx: &mut Transaction<'_, Postgres>, test: &Test1) -> Result<u64, sqlx::Error>;
    async fn delete(&self, tx: &mut Transaction<'_, Postgres>, id: i32) -> Result<u64, sqlx::Error>;
}

pub struct PostgresRepositoryImpl{}

impl PostgresRepositoryImpl {
    pub fn new() -> PostgresRepositoryImpl {
        PostgresRepositoryImpl {  }
    }
}

impl PostgresRepository for PostgresRepositoryImpl {
    async fn create(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<i32, sqlx::Error> {
        let result: (i32,) = sqlx::query_as("INSERT INTO test1(test) VALUES($1) RETURNING id;")
            .bind(&test1.test)
            .fetch_one(&mut **tx)
            .await?;
        Ok(result.0)
    }

    async fn get_by_id(&self, pool: &sqlx::PgPool, id: i32) -> Result<Test1, sqlx::Error> {
        let test1 = sqlx::query_as::<_, Test1>("SELECT id, test FROM test1 WHERE id = $1;")
            .bind(id)
            .fetch_one(pool)
            .await?;
        Ok(test1)
    }

    async fn update(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<u64, sqlx::Error> {
        let result = sqlx::query("UPDATE test1 SET test = $1 WHERE id = $2;")
            .bind(&test1.test)
            .bind(&test1.id)
            .execute(&mut **tx)
            .await?;
        Ok(result.rows_affected())
    }

    async fn delete(&self, tx: &mut Transaction<'_, Postgres>, id: i32) -> Result<u64, sqlx::Error> {
        let result = sqlx::query("DELETE FROM test1 WHERE id = $1;")
            .bind(id)
            .execute(&mut **tx)
            .await?;
        Ok(result.rows_affected())
    }
}