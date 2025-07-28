use sqlx::{Postgres, Transaction};
use uuid::Uuid;

use crate::models::entities::test1::Test1;

pub trait Test1Repository {
    async fn create(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<u64, sqlx::Error>;
    async fn get_by_id(&self, pool: &sqlx::PgPool, id: Uuid) -> Result<Test1, sqlx::Error>;
    async fn get_all(&self, pool: &sqlx::PgPool) -> Result<Vec<Test1>, sqlx::Error>;
    async fn update(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<u64, sqlx::Error>;
    async fn delete(&self, tx: &mut Transaction<'_, Postgres>, id: Uuid) -> Result<u64, sqlx::Error>;
}

pub struct Test1RepositoryImpl{}

impl Test1RepositoryImpl {
    pub fn new() -> Test1RepositoryImpl {
        Test1RepositoryImpl {  }
    }
}

impl Test1Repository for Test1RepositoryImpl {
    async fn create(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<u64, sqlx::Error> {
        let result = sqlx::query("INSERT INTO test1(id, test) VALUES($1, $2);")
            .bind(&test1.id)
            .bind(&test1.test)
            .execute(&mut **tx)
            .await?;
        Ok(result.rows_affected())
    }

    async fn get_by_id(&self, pool: &sqlx::PgPool, id: Uuid) -> Result<Test1, sqlx::Error> {
        let test1 = sqlx::query_as::<_, Test1>("SELECT id, test FROM test1 WHERE id = $1;")
            .bind(id)
            .fetch_one(pool)
            .await?;
        Ok(test1)
    }

    async fn get_all(&self, pool: &sqlx::PgPool) -> Result<Vec<Test1>, sqlx::Error> {
        let test1s:Vec<Test1> = sqlx::query_as::<_, Test1>("SELECT id, test FROM test1;")
        .fetch_all(pool)
        .await?;
        Ok(test1s)
    }

    async fn update(&self, tx: &mut Transaction<'_, Postgres>, test1: &Test1) -> Result<u64, sqlx::Error> {
        let result = sqlx::query("UPDATE test1 SET test = $1 WHERE id = $2;")
            .bind(&test1.test)
            .bind(&test1.id)
            .execute(&mut **tx)
            .await?;
        Ok(result.rows_affected())
    }

    async fn delete(&self, tx: &mut Transaction<'_, Postgres>, id: Uuid) -> Result<u64, sqlx::Error> {
        let result = sqlx::query("DELETE FROM test1 WHERE id = $1;")
            .bind(id)
            .execute(&mut **tx)
            .await?;
        Ok(result.rows_affected())
    }
}