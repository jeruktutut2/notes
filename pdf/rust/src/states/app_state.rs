use std::sync::Arc;

use crate::services::pdf_service::PdfServiceImpl;

pub struct AppState {
    pub pdf_service: Arc<PdfServiceImpl>
}