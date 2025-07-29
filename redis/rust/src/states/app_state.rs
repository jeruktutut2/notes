use std::sync::Arc;
use tokio::sync::Mutex;
use crate::services::test1_service::Test1ServiceImpl;

pub struct AppState {
    pub test1_service: Arc<Mutex<Test1ServiceImpl>>
}