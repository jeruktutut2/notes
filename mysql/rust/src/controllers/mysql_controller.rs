use std::sync::Arc;

use axum::{extract::{Path, State}, response::IntoResponse, Json};

use crate::{
    models::requests::{create_request::CreateRequest, delete_request::DeleteRequest, update_request::UpdateRequest}, 
    services::mysql_service::MysqlService, states::app_state::AppState
};

pub async fn create(
    State(state): State<Arc<AppState>>,
    Json(create_request): Json<CreateRequest>
) -> impl IntoResponse {
    // let http_response = match state.mysql_service.create(create_request).await {
        
    // };
    // (StatusCode::OK, "mantap")
    // Response::builder()
    //     .status(StatusCode::OK)
    //     .body(Body::from(Json(vec!["foo".to_owned()])))
    //     .unwrap()
    let response = state.mysql_service.create(create_request).await;
    (
        response.http_status_code, 
        Json(response.body_response)
    )
}

pub async fn get_by_id(
    State(state): State<Arc<AppState>>,
    Path(id): Path<i32>
) -> impl IntoResponse {
    let response = state.mysql_service.get_by_id(id).await;
    // (StatusCode::OK, Json(vec!["foo".to_owned()]))
    // return (response.http_status_code, response.response)

    (
        response.http_status_code,
        Json(response.body_response)
    )
}

pub async fn update(
    State(state): State<Arc<AppState>>,
    Json(update_request): Json<UpdateRequest>
) -> impl IntoResponse {
    let response = state.mysql_service.update(update_request).await;
    (response.http_status_code, Json(response.body_response))
}

pub async fn del(
    State(state): State<Arc<AppState>>, 
    Json(delete_request): Json<DeleteRequest>
) -> impl IntoResponse {
    let response = state.mysql_service.delete(delete_request).await;
    (response.http_status_code, Json(()))
}