use std::sync::Arc;
use axum::extract::State;
use axum::http::StatusCode;
use axum::response::IntoResponse;
use crate::services::logger_service::LoggerService;
use crate::states::app_state::AppState;

pub async fn check_logger(
    State(state): State<Arc<AppState>>
) -> impl IntoResponse {
    let response = state.logger_service.check_logger().await;
    (StatusCode::OK, response)
}