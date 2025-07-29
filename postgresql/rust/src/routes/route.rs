use std::sync::Arc;

use axum::{routing::{delete, get, post, put}, Router};

use crate::{controllers::{postgres_controller::{create, del, get_by_id, update}}, repositories::postgres_repository::PostgresRepositoryImpl, services::postgres_service::PostgresServiceImpl, states::app_state::AppState, utils::postgres_util::PostgresUtilImpl};

pub fn set_route(postgres_util: Arc<PostgresUtilImpl>) -> Router {
    let postgres_repository =Arc::new(PostgresRepositoryImpl::new());
    let postgres_service = Arc::new(PostgresServiceImpl::new(postgres_util, postgres_repository.clone()));
    let app_state = Arc::new(AppState{postgres_service: postgres_service.clone()});
    Router::new()
    .route("/", post(create))
    .route("/{id}", get(get_by_id))
    .route("/", put(update))
    .route("/", delete(del))
    .with_state(app_state)
}