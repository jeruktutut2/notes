use std::sync::Arc;
use axum::extract::{Path, State};
use axum::Json;
use axum::response::IntoResponse;
use crate::models::requests::create_request::CreateRequest;
use crate::models::requests::delete_request::DeleteRequest;
use crate::services::test1_service::Test1Service;
use crate::states::app_state::AppState;

pub async fn create_handler(State(state): State<Arc<AppState>>, Json(create_request): Json<CreateRequest>) -> impl IntoResponse {
    let response = state.test1_service.lock().await.create(create_request).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn get_handler(State(state): State<Arc<AppState>>, Path(id): Path<String>) -> impl IntoResponse {
    let response = state.test1_service.lock().await.get(&id).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn delete_handler(State(state): State<Arc<AppState>>, Json(delete_request): Json<DeleteRequest>) -> impl IntoResponse {
    let response = state.test1_service.lock().await.delete(delete_request).await;
    (response.http_status_code, Json(response.body_response))
}