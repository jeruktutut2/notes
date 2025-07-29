use std::sync::Arc;

use crate::services::millisecond_service::{MillisecondService, MillisecondServiceImpl};

pub struct AppState {
    pub millisecond_service: Arc<MillisecondServiceImpl>
}