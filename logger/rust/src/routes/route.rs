use std::sync::Arc;
use axum::Router;
use axum::routing::get;
use crate::controllers::logger_controller::check_logger;
use crate::services::logger_service::LoggerServiceImpl;
use crate::states::app_state::AppState;

pub fn set_route() -> Router {
    let logger_service = Arc::new(LoggerServiceImpl::new());
    let app_state = Arc::new(AppState{logger_service: logger_service.clone()});
    Router::new()
        .route("/logger", get(check_logger))
        .with_state(app_state)
}