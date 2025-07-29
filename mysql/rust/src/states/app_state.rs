use std::sync::Arc;

use crate::services::mysql_service::MysqlServiceImpl;

#[derive(Clone)]
pub struct AppState {
    pub mysql_service: Arc<MysqlServiceImpl>,
}