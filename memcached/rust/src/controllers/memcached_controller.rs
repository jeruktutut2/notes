use std::sync::Arc;

use axum::{extract::{Path, State}, http::StatusCode, response::IntoResponse, Json};

use crate::{models::requests::{delete_request::DeleteRequest, set_request::SetRequest}, services::memcached_service::MemcachedService, states::app_state::AppState};

pub async fn set_handler(
    State(state): State<Arc<AppState>>,
    Json(set_request): Json<SetRequest>
) -> impl IntoResponse {
    let response = state.memcached_service.set(set_request.message).await;
    (StatusCode::OK, response)
}

pub async fn get_handler(
    State(state): State<Arc<AppState>>,
    Path(id): Path<String>
) -> impl IntoResponse {
    let response = state.memcached_service.get(id).await;
    (StatusCode::OK, response)
}

pub async fn delete_handler(
    State(state): State<Arc<AppState>>,
    Json(delete_request): Json<DeleteRequest>
) -> impl IntoResponse {
    let response = state.memcached_service.delete(delete_request.id).await;
    (StatusCode::OK, response)
}

pub async fn flush_handler(
    State(state): State<Arc<AppState>>
) -> impl IntoResponse {
    let response = state.memcached_service.flush().await;
    (StatusCode::OK, response)
}