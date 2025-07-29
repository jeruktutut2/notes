use std::sync::Arc;

use axum::{routing::get, Router};

use crate::{controllers::mqtt_controller::send_message, producers::mqtt_producer::MqttProducerImpl, services::mqtt_service::MqttServiceImpl, states::app_state::AppState};

pub fn set_route(mqtt_producer: Arc<MqttProducerImpl>) -> Router {
    let mqtt_service = Arc::new(MqttServiceImpl::new(mqtt_producer));
    let app_state = Arc::new(AppState{mqtt_service: mqtt_service.clone()});
    Router::new()
        .route("/mqtt/send-message/{message}", get(send_message))
        .with_state(app_state)
}