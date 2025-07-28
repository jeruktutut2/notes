use std::process;

use memcache::{Client, MemcacheError};

pub trait MemcachedUtil {
    async fn set(&self, key: &str, value: &str, expiration: u32) -> Result<(), MemcacheError>;
    async fn get(&self, key: &str) -> Result<Option<String>, MemcacheError>;
    async fn delete(&self, key: &str) -> Result<bool, MemcacheError>;
    async fn flush(&self) -> Result<(), MemcacheError>;
}

pub struct MemcachedUtilImpl {
    client: Client
}

impl MemcachedUtilImpl {
    pub async fn new() -> MemcachedUtilImpl {
        let client = match Client::connect("memcache://127.0.0.1:11211") {
            Ok(client) => client,
            Err(err) => {
                println!("error: {}", err);
                process::exit(1);
            }
        };
        
        MemcachedUtilImpl {
            client
        }
    }
}

impl MemcachedUtil for MemcachedUtilImpl {
    async fn set(&self, key: &str, value: &str, expiration: u32) -> Result<(), MemcacheError> {
        self.client.set(key, value, expiration)
    }

    async fn get(&self, key: &str) -> Result<Option<String>, MemcacheError> {
        self.client.get(key)
    }

    async fn delete(&self, key: &str) -> Result<bool, MemcacheError> {
        self.client.delete(key)
    }

    async fn flush(&self) -> Result<(), MemcacheError> {
        self.client.flush()
    }
}