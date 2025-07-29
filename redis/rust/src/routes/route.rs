use std::sync::Arc;
use axum::Router;
use axum::routing::{delete, get, post};
use tokio::sync::Mutex;
use crate::controllers::test1_controller::{create_handler, delete_handler, get_handler};
use crate::services::test1_service::Test1ServiceImpl;
use crate::states::app_state::AppState;
use crate::utils::redis_util::RedisUtilImpl;

pub fn set_routes(redis_util: Arc<Mutex<RedisUtilImpl>>) -> Router {
    let test1_service = Arc::new(Mutex::new(Test1ServiceImpl::new(redis_util)));
    let app_state = Arc::new(AppState {test1_service: test1_service.clone()});
    Router::new()
        .route("/api/v1/test1", post(create_handler))
        .route("/api/v1/test1/{id}", get(get_handler))
        .route("/api/v1/test1", delete(delete_handler))
        .with_state(app_state)
}