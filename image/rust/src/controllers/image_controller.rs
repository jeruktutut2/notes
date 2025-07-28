use std::sync::Arc;

use axum::{extract::State, http::StatusCode, response::IntoResponse, Json};

use crate::{models::requests::image_request::ImageRequest, services::image_service::ImageService, states::app_state::AppState};

pub async fn check_image(
    State(state): State<Arc<AppState>>,
    Json(image_request): Json<ImageRequest>
) -> impl IntoResponse {
    let response = state.image_service.check_image(image_request).await;
    (StatusCode::OK, response)
}