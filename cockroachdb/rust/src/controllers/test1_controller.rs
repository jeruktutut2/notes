use std::sync::Arc;

use axum::{extract::{Path, State}, response::IntoResponse, Json};
use uuid::Uuid;

use crate::{models::requests::{create_request::CreateRequest, delete_request::DeleteRequest, update_request::UpdateRequest}, services::test1_service::Test1Service, states::app_state::AppState};

pub async fn create_handler(
    State(state): State<Arc<AppState>>,
    Json(create_request): Json<CreateRequest>
) -> impl IntoResponse {
    let response = state.test1_service.create(create_request).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn get_by_id_handler(
    State(state): State<Arc<AppState>>,
    Path(id): Path<Uuid>
) -> impl IntoResponse {
    let response = state.test1_service.get_by_id(id).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn get_all_handler(
    State(state): State<Arc<AppState>>
) -> impl IntoResponse {
    let response = state.test1_service.get_all().await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn update_handler(
    State(state): State<Arc<AppState>>,
    Json(update_request): Json<UpdateRequest>
) -> impl IntoResponse {
    let response = state.test1_service.update(update_request).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn delete_handler(
    State(state): State<Arc<AppState>>,
    Json(delete_request): Json<DeleteRequest>
) -> impl IntoResponse {
    let response = state.test1_service.delete(delete_request).await;
    (response.http_status_code, Json(response.body_response))
}