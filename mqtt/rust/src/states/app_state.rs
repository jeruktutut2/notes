use std::sync::Arc;

use crate::services::mqtt_service::MqttServiceImpl;

pub struct AppState {
    pub mqtt_service: Arc<MqttServiceImpl>
}