use std::time::Duration;

use chrono::Local;
use sqlx::{mysql::MySqlPoolOptions, MySql, Pool, Transaction};

pub trait MysqlUtil {
    async fn get_pool(&self) -> &Pool<MySql>;
    async fn begin(&self) -> Result<Transaction<'static, MySql>, sqlx::Error>;
    async fn commit(&self, tx: Transaction<'static, MySql>) -> Result<(), sqlx::Error>;
    async fn rollback(&self, tx: Transaction<'static, MySql>) -> Result<(), sqlx::Error>;
    async fn close(&self);
}

#[derive(Debug)]
pub struct MysqlUtilImpl {
    pool: Pool<MySql>
}

impl MysqlUtilImpl {
    pub async fn new() -> MysqlUtilImpl {
        // let mysql_host = env::var("MYSQL_HOST").expect( format!("{} mysql: couldn't find host", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_username = env::var("MYSQL_USERNAME").expect( format!("{} mysql: couldn't find username", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_password = env::var("MYSQL_PASSWORD").expect( format!("{} mysql: couldn't find password", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_port = env::var("MYSQL_PORT").expect( format!("{} mysql: couldn't find port", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_database = env::var("MYSQL_DATABASE").expect( format!("{} mysql: couldn't find database", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_idle_timeout_env = env::var("MYSQL_IDLE_TIMEOUT").expect( format!("{} mysql: couldn't find max idle timeout", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_idle_timeout = mysql_idle_timeout_env.parse().expect(format!("{} mysql: couldn't parse idle timeout", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_max_connection_env = env::var("MYSQL_MAX_CONNECTION").expect( format!("{} mysql: couldn't find max connection", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_max_connection = mysql_max_connection_env.parse().expect(format!("{} mysql: couldn't parse max connection", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_max_lifetime_env = env::var("MYSQL_MAX_LIFETIME").expect( format!("{} mysql: couldn't find max lifetime", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_max_lifetime = mysql_max_lifetime_env.parse().expect(format!("{} mysql: couldn't parse max lifetime", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_min_connection_env = env::var("MYSQL_MIN_CONNECTION").expect( format!("{} mysql: couldn't find max lifetime", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());
        // let mysql_min_connection = mysql_min_connection_env.parse().expect(format!("{} mysql: couldn't parse max lifetime", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string()).as_str());

        // println!("{} mysql: connecting to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), mysql_host, mysql_port);
        println!("{} mysql: connecting to localhost:3309", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        // mysql_username, mysql_password, mysql_host, mysql_port, mysql_database
        let mysql_url = format!("mysql://root:12345@localhost:3309/test1");
        let pool = MySqlPoolOptions::new()
            .idle_timeout(Some(Duration::from_secs(10)))
            .max_connections(10)
            .max_lifetime(Some(Duration::from_secs(10)))
            .min_connections(10)
            .connect(&mysql_url).await.expect("cannot connect postgres database");
        println!("{} mysql: connected to localhost:3309", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        return MysqlUtilImpl {
            pool: pool
        };
    }
}

impl MysqlUtil for MysqlUtilImpl {
    async fn get_pool(&self) -> &Pool<MySql> {
        &self.pool
    }

    async fn begin(&self) -> Result<Transaction<'static, MySql>, sqlx::Error>{
        self.pool.begin().await
    }

    async fn commit(&self, tx: Transaction<'static, MySql>) -> Result<(), sqlx::Error> {
        tx.commit().await
    }

    async fn rollback(&self, tx: Transaction<'static, MySql>) -> Result<(), sqlx::Error> {
        tx.rollback().await
    }

    async fn close(&self) {
        println!("{} mysql: closing to localhost:3309", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        self.pool.close().await;
        println!("{} mysql: closed to localhost:3309", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string())
    }
}