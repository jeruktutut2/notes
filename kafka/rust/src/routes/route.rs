use std::sync::Arc;

use axum::{routing::get, Router};

use crate::{controllers::kafka_controller::send_message, producers::kafka_producer::KafkaProducerImpl, services::kafka_service::KafkaServiceImpl, states::app_state::AppState};

pub fn set_route(kafka_producer: Arc<KafkaProducerImpl>) -> Router {
    let kafka_service = Arc::new(KafkaServiceImpl::new(kafka_producer));
    let state = Arc::new(AppState{kafka_service: kafka_service.clone()});
    Router::new()
        .route("/kafka/send-message/{message}", get(send_message))
        .with_state(state)
}