use std::sync::Arc;

use axum::{routing::post, Router};

use crate::{controllers::image_controller::check_image, services::image_service::ImageServiceImpl, states::app_state::AppState};

pub fn set_route() -> Router {
    let image_service = Arc::new(ImageServiceImpl::new());
    let app_state = Arc::new(AppState{image_service: image_service.clone()});
    Router::new()
        .route("/image", post(check_image))
        .with_state(app_state)
}