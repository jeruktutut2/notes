use std::sync::Arc;

use crate::services::rabbitmq_service::RabbitMQServiceImpl;

pub struct AppState {
    pub rabbitmq_service: Arc<RabbitMQServiceImpl>
}