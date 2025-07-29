use std::sync::Arc;

use axum::{routing::get, Router};

use crate::{controllers::pdf_controller::generate_pdf, services::pdf_service::PdfServiceImpl, states::app_state::AppState};

pub fn set_route() -> Router {
    let pdf_service = Arc::new(PdfServiceImpl::new());
    let app_state = Arc::new(AppState{pdf_service: pdf_service.clone()});
    Router::new()
        .route("/pdf", get(generate_pdf))
        .with_state(app_state)
}