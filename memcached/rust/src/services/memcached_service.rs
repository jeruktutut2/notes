use std::sync::Arc;

use chrono::Utc;

use crate::utils::memcached_util::{MemcachedUtil, MemcachedUtilImpl};

pub trait MemcachedService {
    async fn set(&self, value: String) -> String;
    async fn get(&self, key: String) -> String;
    async fn delete(&self, key: String) -> String;
    async fn flush(&self) -> String;
}

pub struct MemcachedServiceImpl {
    memcached_util: Arc<MemcachedUtilImpl>
}

impl MemcachedServiceImpl {
    pub fn new(memcached_util: Arc<MemcachedUtilImpl>) -> MemcachedServiceImpl {
        MemcachedServiceImpl {
            memcached_util
        }
    }
}

impl MemcachedService for MemcachedServiceImpl {
    async fn set(&self, value: String) -> String {
        let key_string = Utc::now().timestamp_millis().to_string();
        let key = key_string.as_str();
        match self.memcached_util.set(key, value.as_str(), 0).await {
            Ok(_)=> (),
            Err(err) => {
                println!("error: {}", err);

            }
        }
        println!("key: {}", key);
        "ok".to_string()
    }

    async fn get(&self, key: String) -> String {
        let key_str = key.as_str();
        let result = match self.memcached_util.get(key_str).await {
            Ok(result) => result,
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string();
            }
        };
        println!("result: {:?}", result);
        "ok".to_string()
    }

    async fn delete(&self, key: String) -> String {
        let key_str = key.as_str();
        let is_deleted = match self.memcached_util.delete(key_str).await {
            Ok(is_deleted) => is_deleted,
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string()
            }
        };
        println!("is_deleted: {}", is_deleted);
        "ok".to_string()
    }

    async fn flush(&self) -> String {
        match self.memcached_util.flush().await {
            Ok(_) => (),
            Err(err) => {
                println!("error: {}", err);
                return "error".to_string()
            }
        };
        
        "ok".to_string()
    }
}