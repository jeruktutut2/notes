use std::sync::Arc;

use axum::{extract::{Path, State}, http::StatusCode, response::IntoResponse};

use crate::{services::rabbitmq_service::RabbitMQService, states::app_state::AppState};

pub async fn send_message(
    State(state): State<Arc<AppState>>,
    Path(message): Path<String>,
) -> impl IntoResponse {
    let response = state.rabbitmq_service.send_message(message).await;
    (StatusCode::OK, response)
}