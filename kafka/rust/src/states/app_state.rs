use std::sync::Arc;

use crate::services::kafka_service::KafkaServiceImpl;

pub struct AppState {
    pub kafka_service: Arc<KafkaServiceImpl>
}