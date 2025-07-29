use std::sync::Arc;

use crate::services::file_service::FileServiceImpl;

pub struct AppState {
    pub file_service: Arc<FileServiceImpl>
}