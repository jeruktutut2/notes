use std::sync::Arc;

use axum::{routing::{delete, get, post, put}, Router};

use crate::{
    controllers::mysql_controller::{create, del, get_by_id, update}, 
    repositories:: mysql_repository::MysqlRepositoryImpl, 
    services::mysql_service::MysqlServiceImpl, states::app_state::AppState, utils::mysql_util::MysqlUtilImpl
};

pub fn set_route(mysql_util: Arc<MysqlUtilImpl>) -> Router {
    let mysql_repository = Arc::new(MysqlRepositoryImpl::new());
    let mysql_service = Arc::new(MysqlServiceImpl::new(mysql_util, mysql_repository.clone()));
    let app_state = Arc::new(AppState{mysql_service: mysql_service.clone()});
    Router::new()
        .route("/", post(create))
        .route("/{id}", get(get_by_id))
        .route("/", put(update))
        .route("/", delete(del))
        .with_state(app_state)
}