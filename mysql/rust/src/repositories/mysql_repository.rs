use sqlx::{MySql, Transaction};

use crate::models::entities::test1::Test1;

pub trait MysqlRepository {
    async fn create(&self, tx : &mut Transaction<'_, MySql>, test1: &Test1) -> Result<(u64, u64), sqlx::Error>;
    async fn get_by_id(&self, pool: &sqlx::MySqlPool, id: i32) -> Result<Test1, sqlx::Error>;
    async fn update(&self, tx : &mut Transaction<'_, MySql>, test1: &Test1) -> Result<u64, sqlx::Error>;
    async fn delete(&self, tx: &mut Transaction<'_, MySql>, id: i32) -> Result<u64, sqlx::Error>;
}

#[derive(Debug, Clone)]
pub struct MysqlRepositoryImpl{}

impl MysqlRepositoryImpl {
    pub fn new() -> MysqlRepositoryImpl {
        MysqlRepositoryImpl {  }
    }
}

impl MysqlRepository for MysqlRepositoryImpl {
    async fn create(&self, tx : &mut Transaction<'_, MySql>, test1: &Test1) -> Result<(u64, u64), sqlx::Error> {
        let result = sqlx::query("INSERT INTO test1(test) VALUES(?)")
            .bind(&test1.test)
            .execute(&mut **tx)
            .await?;
        Ok((result.rows_affected(), result.last_insert_id()))
    }

    async fn get_by_id(&self, pool: &sqlx::MySqlPool, id: i32) -> Result<Test1, sqlx::Error> {
        let test1= sqlx::query_as::<_, Test1>("SELECT id, test FROM test1 WHERE id = ?;")
            .bind(id)
            .fetch_one(pool)
            .await?;
        Ok(test1)
    }

    async fn update(&self, tx : &mut Transaction<'_, MySql>, test1: &Test1) -> Result<u64, sqlx::Error> {
        let result = sqlx::query("UPDATE test1 SET test = ? WHERE id = ?;")
            .bind(&test1.test)
            .bind(&test1.id)
            .execute(&mut **tx)
            .await?;
        Ok(result.rows_affected())
    }

    async fn delete(&self, tx: &mut Transaction<'_, MySql>, id: i32) -> Result<u64, sqlx::Error> {
        let result = sqlx::query("DELETE FROM test1 WHERE id = ?;")
            .bind(id)
            .execute(&mut **tx)
            .await?;
        Ok(result.rows_affected())
    }
}