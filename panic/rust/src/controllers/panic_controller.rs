use std::sync::Arc;

use axum::{extract::State, http::StatusCode, response::IntoResponse};

use crate::{services::panic_service::PanicService, states::app_state::AppState};

pub async fn check_panic(
    State(state): State<Arc<AppState>>
) -> impl IntoResponse {
    let response = state.panic_service.check_panic().await;
    (StatusCode::OK, response)
}