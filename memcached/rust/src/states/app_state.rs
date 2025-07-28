use std::sync::Arc;

use crate::services::memcached_service::MemcachedServiceImpl;

pub struct AppState {
    pub memcached_service: Arc<MemcachedServiceImpl>
}