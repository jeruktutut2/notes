use std::sync::Arc;

use crate::services::panic_service::PanicServiceImpl;

pub struct AppState {
    pub panic_service: Arc<PanicServiceImpl>
}