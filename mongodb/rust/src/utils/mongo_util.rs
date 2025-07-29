use chrono::Local;
use mongodb::{Client, Database};

pub trait MongoUtil {
    async fn get_database(&self) -> Database;
}

#[derive(Debug)]
pub struct MongoUtilImpl {
    database: Database
}

impl MongoUtilImpl {
    pub async fn new() -> MongoUtilImpl {
        println!("{} postgres: connecting to localhost:27017", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        let uri = format!("mongodb://root:12345@localhost:27017/test1?minPoolSize=5&maxPoolSize=20");
        let client = Client::with_uri_str(&uri).await.expect("cannot connect to mongodb");
        let database = client.database("test1");
        println!("{} postgres: connected to localhost:27017", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string());
        MongoUtilImpl {
            database
        }
    }
}

impl MongoUtil for MongoUtilImpl {
    async fn get_database(&self) -> Database {
        self.database.clone()
    }
}