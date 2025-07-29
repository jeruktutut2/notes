use std::process;
use chrono::Local;
use redis::{AsyncCommands, Client, RedisResult};
use redis::aio::MultiplexedConnection;

pub trait RedisUtil {
    async fn set(&mut self, key: &str, value: &str) -> RedisResult<()>;
    async fn get(&mut self, key: &str) -> RedisResult<Option<String>>;
    async fn del(&mut self, key: &str) -> RedisResult<()>;
}

#[derive(Debug)]
pub struct RedisUtilImpl {
    connection: MultiplexedConnection,
}

impl RedisUtilImpl {
    pub async fn new() -> RedisUtilImpl {
        println!("{} redis: connecting to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "localhost", "6379");
        let client = match Client::open("redis://localhost:6380/") {
            Ok(client) => client,
            Err(err) => {
                println!("err: {}", err);
                process::exit(1);
            }
        };
        let mut connection = match client.get_multiplexed_async_connection().await {
            Ok(connection) => connection,
            Err(err) => {
                println!("err: {}", err);
                process::exit(1);
            }
        };
        println!("{} redis: connected to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "localhost", "6379");

        println!("{} redis: pinging to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "localhost", "6379");
        match redis::cmd("PING").query_async::<String>(&mut connection).await {
            Ok(pong) => {
                println!("pong: {}", pong)
            },
            Err(err) => {
                println!("err: {}", err);
                process::exit(1);
            }
        }
        println!("{} redis: pinged to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "localhost", "6379");

        RedisUtilImpl {
            connection
        }
    }
}

impl RedisUtil for RedisUtilImpl {
    async fn set(&mut self, key: &str, value: &str) -> RedisResult<()> {
        let _: () = self.connection.set(key, value).await?;
        Ok(())
    }

    async fn get(&mut self, key: &str) -> RedisResult<Option<String>> {
        let result = self.connection.get(key).await?;
        Ok(result)
    }

    async fn del(&mut self, key: &str) -> RedisResult<()> {
        let _: () = self.connection.del(key).await?;
        Ok(())
    }
}