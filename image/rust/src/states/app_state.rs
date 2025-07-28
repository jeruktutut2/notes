use std::sync::Arc;

use crate::services::image_service::ImageServiceImpl;

pub struct AppState {
    pub image_service: Arc<ImageServiceImpl>
}