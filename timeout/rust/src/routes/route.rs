use std::{sync::Arc, time::Duration};
use tower_http::timeout::TimeoutLayer;

use axum::{routing::get, Router};

use crate::{controllers::timeout_controller::{timeout_with_tx_handler, timeout_without_tx_handler}, repositories::test1_repository::Test1RepositoryImpl, services::test1_service::Test1ServiceImpl, states::app_state::AppState, utils::postgres_util::PostgresUtilImpl};

pub fn set_route(postgres_util: Arc<PostgresUtilImpl>) -> Router {
    let test1_repository = Arc::new(Test1RepositoryImpl::new());
    let test1_service = Arc::new(Test1ServiceImpl::new(postgres_util, test1_repository));
    let state = Arc::new(AppState{test1_service: test1_service.clone()});
    Router::new()
        .route("/timeout/without-tx", get(timeout_without_tx_handler))
        .route("/timeout/with-tx", get(timeout_with_tx_handler))
        .route("/timeout/change-timeout", get(timeout_with_tx_handler).layer(TimeoutLayer::new(Duration::from_secs(3))))
        // .route("/timeout/change-timeout", get(timeout_with_tx_handler))
        .with_state(state)
}