use std::sync::Arc;

use axum::{extract::State, http::StatusCode, response::IntoResponse, Json};

use crate::{models::requests::millisecond_request::MillisecondRequest, services::millisecond_service::MillisecondService, states::app_state::AppState};

pub async fn get_by_gmmt_plus8(
    State(state): State<Arc<AppState>>,
    Json(millisecond_request): Json<MillisecondRequest>
) -> impl IntoResponse {
    let response = state.millisecond_service.get_by_gmt_plus8(millisecond_request).await;
    (StatusCode::OK, Json(response))
}

pub async fn get_by_gmt_minus8(
    State(state): State<Arc<AppState>>,
    Json(millisecond_request): Json<MillisecondRequest>
) -> impl IntoResponse {
    let response = state.millisecond_service.get_by_gmt_minus8(millisecond_request).await;
    (StatusCode::OK, Json(response))
}