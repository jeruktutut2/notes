use std::sync::Arc;
use crate::services::logger_service::LoggerServiceImpl;

pub struct AppState {
    pub logger_service: Arc<LoggerServiceImpl>
}