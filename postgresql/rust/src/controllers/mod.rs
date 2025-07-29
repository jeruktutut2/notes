pub mod postgres_controller;

// use std::sync::Arc;

// use axum::{extract::{Path, State}, http::StatusCode, response::IntoResponse, Json};

// use crate::{models::requests::{create_request::CreateRequest, delete_request::{self, DeleteRequest}, update_request::UpdateRequest}, services::postgres_service::PostgresService, states::app_state::AppState};

// pub async fn create(
//     State(state): State<Arc<AppState>>,
//     Json(create_request): Json<CreateRequest>
// ) -> impl IntoResponse{
//     let response = state.postgres_service.create(create_request).await;
//     (response.http_status_code, Json(response.body_response))
// }

// pub async fn get_by_id(
//     State(state): State<Arc<AppState>>,
//     Path(id): Path<i32>
// ) -> impl IntoResponse {
//     let response = state.postgres_service.get_by_id(id).await;
//     (response.http_status_code, Json(response.body_response))
// }

// pub async fn update(
//     State(state): State<Arc<AppState>>,
//     Json(update_request): Json<UpdateRequest>
// ) -> impl IntoResponse {
//     let response = state.postgres_service.update(update_request).await;
//     (response.http_status_code, Json(response.body_response))
// }

// pub async fn delete(
//     State(state): State<Arc<AppState>>,
//     Json(delete_request): Json<DeleteRequest>
// ) -> impl IntoResponse {
//     let response = state.postgres_service.delete(delete_request).await;
//     (response.http_status_code, Json(response.body_response))
// }