use std::sync::Arc;

use axum::{routing::{delete, get, post, put}, Router};

use crate::{controllers::test1_controller::{create_handler, delete_handler, get_all_handler, get_by_id_handler, update_handler}, repositories::test1_repository::Test1RepositoryImpl, services::test1_service::Test1ServiceImpl, states::app_state::AppState, utils::cockroachdb_util::CockroachDbUtilImpl};

pub fn set_route(cockroachdb_util: Arc<CockroachDbUtilImpl>) -> Router {
    let test1_repository = Arc::new(Test1RepositoryImpl::new());
    let test1_service = Arc::new(Test1ServiceImpl::new(cockroachdb_util, test1_repository.clone()));
    let app_state = Arc::new(AppState{test1_service: test1_service.clone()});
    Router::new()
        .route("/test1", post(create_handler))
        .route("/test1/{id}", get(get_by_id_handler))
        .route("/test1", get(get_all_handler))
        .route("/test1", put(update_handler))
        .route("/test1", delete(delete_handler))
        .with_state(app_state)
}