use std::sync::Arc;

use axum::{routing::{post, get, put, delete}, Router};
use mongodb::Collection;

use crate::{controllers::test1_controller::{create, delete_by_id, get_by_id, update_by_id}, models::entities::test1::Test1, repositories::test1_repository::Test1RepositoryImpl, services::test1_service::Test1ServiceImpl, states::app_state::AppState, utils::mongo_util::{self, MongoUtilImpl}};

pub fn set_route(collection: Arc<Collection<Test1>>) -> Router {
    let test1_repository = Arc::new(Test1RepositoryImpl::new(collection));
    let test1_service = Arc::new(Test1ServiceImpl::new(test1_repository.clone()));
    let state = Arc::new(AppState{test1_service: test1_service.clone()});
    Router::new()
        .route("/api/v1/test1", post(create))
        .route("/api/v1/test1/{id}", get(get_by_id))
        .route("/api/v1/test1", put(update_by_id))
        .route("/api/v1/test1", delete(delete_by_id))
        .with_state(state)
}