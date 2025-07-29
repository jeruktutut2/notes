use std::sync::Arc;

use axum::{extract::State, http::StatusCode, response::IntoResponse};

use crate::{services::stacktrace_service::{StacktraceService, StacktraceServiceImpl}, states::app_state::AppState};

pub async fn printStacktrace(
    State(state): State<Arc<AppState>>
) -> impl IntoResponse {
    let response = state.stacktrace_service.printStacktrace().await;
    (StatusCode::OK, response)
}