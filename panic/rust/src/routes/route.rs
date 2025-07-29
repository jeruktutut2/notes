use std::sync::Arc;

use axum::{routing::get, Router};

use crate::{controllers::panic_controller::check_panic, services::panic_service::PanicServiceImpl, states::app_state::AppState};

pub fn set_route() -> Router {
    let panic_service = Arc::new(PanicServiceImpl::new());
    let state = Arc::new(AppState{panic_service: panic_service.clone()});
    Router::new()
        .route("/", get(check_panic))
        .with_state(state)
}