use std::sync::Arc;

use axum::{extract::{Request, State}, http::StatusCode, response::IntoResponse};
use tokio::select;

use crate::{middlewares::cancellation_token_middleware::{HttpCloseConnectionToken, TimeoutToken}, services::test1_service::Test1Service, states::app_state::AppState};

pub async fn timeout_without_tx_handler(
    State(app_state): State<Arc<AppState>>,
    request: Request
) -> impl IntoResponse {
    let timeout_token = request.extensions().get::<TimeoutToken>().expect("timeout token not found").0.clone();
    let http_closed_connection_token = request.extensions().get::<HttpCloseConnectionToken>().expect("http closed connection token not found").0.clone();
    let response = app_state.test1_service.create_without_tx().await;
    // let response = select! {
    //     response = app_state.test1_service.create_without_tx() => response,

    //     _ = timeout_token.cancelled() => {
    //         println!("Request cancelled: Timeout occurred");
    //         "Request cancelled: Timeout occurred".to_string()
    //     },
    //     _ = http_closed_connection_token.cancelled() => {
    //         println!("Request cancelled: HTTP connection closed");
    //         "Request cancelled: HTTP connection closed".to_string()
    //     }
    // };
    
    (StatusCode::OK, response)
}

pub async fn timeout_with_tx_handler(
    State(app_state): State<Arc<AppState>>
) -> impl IntoResponse {
    let response = app_state.test1_service.create_with_tx().await;
    (StatusCode::OK, response)
}

pub async fn change_timeout_handler(
    State(app_state): State<Arc<AppState>>
) -> impl IntoResponse {
    let response = app_state.test1_service.create_with_tx().await;
    (StatusCode::OK, response)
}