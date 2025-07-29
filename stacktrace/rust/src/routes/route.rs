use std::sync::Arc;

use axum::{routing::get, Router};

use crate::{controllers::stacktrace_controller::printStacktrace, services::stacktrace_service::StacktraceServiceImpl, states::app_state::AppState};

pub fn set_route() -> Router {
    let stacktrace_service = Arc::new(StacktraceServiceImpl::new());
    let app_state = Arc::new(AppState{stacktrace_service: stacktrace_service.clone()});
    Router::new()
        .route("/", get(printStacktrace))
        .with_state(app_state)
}