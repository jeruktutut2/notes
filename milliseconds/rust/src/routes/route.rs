use std::sync::Arc;

use axum::{routing::get, Router};

use crate::{controllers::millisecond_controller::{get_by_gmmt_plus8, get_by_gmt_minus8}, services::millisecond_service::MillisecondServiceImpl, states::app_state::AppState};

pub fn set_route() -> Router {
    let millisecond_service = Arc::new(MillisecondServiceImpl::new());
    let app_state = Arc::new(AppState{millisecond_service: millisecond_service.clone()});
    Router::new()
        .route("/millisecond/plus8", get(get_by_gmmt_plus8))
        .route("/millisecond/minus8", get(get_by_gmt_minus8))
        .with_state(app_state)
}