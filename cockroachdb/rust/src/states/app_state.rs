use std::sync::Arc;

use crate::services::test1_service::Test1ServiceImpl;

pub struct AppState {
    pub test1_service: Arc<Test1ServiceImpl>
}