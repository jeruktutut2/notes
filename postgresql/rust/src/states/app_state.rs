use std::sync::Arc;

use crate::services::postgres_service::PostgresServiceImpl;

pub struct AppState {
    pub postgres_service: Arc<PostgresServiceImpl>
}