use std::sync::Arc;

use axum::{routing::get, Router};
use rabbitmq_stream_client::{NoDedup, Producer};

use crate::{controllers::rabbitmq_controller::send_message, services::rabbitmq_service::RabbitMQServiceImpl, states::app_state::AppState};

pub fn set_route(producer: Producer<NoDedup>) -> Router {
    let rabbitmq_service = Arc::new(RabbitMQServiceImpl::new(producer));
    let state = Arc::new(AppState{rabbitmq_service: rabbitmq_service.clone()});
    Router::new()
        .route("/rabbitmq/send-message/{message}", get(send_message))
        .with_state(state)
}