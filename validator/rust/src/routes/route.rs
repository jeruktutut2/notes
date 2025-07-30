use std::sync::Arc;
use axum::Router;
use axum::routing::post;
use crate::controllers::test1_controller::create_handler;
use crate::services::test1_service::Test1ServiceImpl;
use crate::states::app_state::AppState;

pub fn set_route() -> Router {
    let app_state = Arc::new(AppState {test1_service: Arc::new(Test1ServiceImpl::new())});
    Router::new()
        .route("/", post(create_handler))
        .with_state(app_state)
}