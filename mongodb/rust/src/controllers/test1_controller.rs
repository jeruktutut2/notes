use std::sync::Arc;

use axum::{extract::{Path, State}, response::IntoResponse, Json};

use crate::{models::requests::{create_request::CreateRequest, delete_request::{self, DeleteRequest}, update_request::UpdateRequest}, services::test1_service::Test1Service, states::app_state::AppState};

pub async fn create(
    State(state): State<Arc<AppState>>,
    Json(create_request): Json<CreateRequest>
) -> impl IntoResponse {
    let response = state.test1_service.create(create_request).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn get_by_id(
    State(state): State<Arc<AppState>>,
    Path(id): Path<String>
) -> impl IntoResponse {
    let response = state.test1_service.get_by_id(id).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn update_by_id(
    State(state): State<Arc<AppState>>,
    Json(update_request): Json<UpdateRequest>
) -> impl IntoResponse {
    let response = state.test1_service.update_by_id(update_request).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn delete_by_id(
    State(state): State<Arc<AppState>>,
    Json(delete_request): Json<DeleteRequest>
) -> impl IntoResponse {
    let response = state.test1_service.delete_by_id(delete_request).await;
    (response.http_status_code, Json(response.body_response))
}