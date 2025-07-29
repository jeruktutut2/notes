use std::sync::Arc;

use axum::{routing::{get, post}, Router};

use crate::{controllers::file_controller::{check_file_handler, merge_handler, upload_and_merge, upload_handler}, services::file_service::FileServiceImpl, states::app_state::AppState};

pub fn set_route() -> Router {
    let file_service = Arc::new(FileServiceImpl::new());
    let state = Arc::new(AppState{file_service: file_service.clone()});
    Router::new()
        .route("/file/upload", post(upload_handler))
        .route("/file/merge", post(merge_handler))
        .route("/file/check-file/{file_id}", get(check_file_handler))
        .route("/file/upload-merge", post(upload_and_merge))
        .with_state(state)
}