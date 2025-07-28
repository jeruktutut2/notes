use std::sync::Arc;

use axum::{routing::{delete, get, post}, Router};

use crate::{controllers::memcached_controller::{delete_handler, flush_handler, get_handler, set_handler}, services::memcached_service::MemcachedServiceImpl, states::app_state::AppState, utils::memcached_util::MemcachedUtilImpl};

pub fn set_route(memcached_util: Arc<MemcachedUtilImpl>) -> Router {
    let memcached_service = Arc::new(MemcachedServiceImpl::new(memcached_util));
    let state = Arc::new(AppState{memcached_service: memcached_service.clone()});
    Router::new()
        .route("/memcached", post(set_handler))
        .route("/memcached/{id}", get(get_handler))
        .route("/memcached", delete(delete_handler))
        .route("/memcached/flush", post(flush_handler))
        .with_state(state)
}