use std::sync::Arc;

use axum::Router;
use chrono::Local;
use consumers::mqtt_consumer::MqttConsumerImpl;
use producers::mqtt_producer::MqttProducerImpl;
use routes::route::set_route;
use tokio::net::TcpListener;
use tokio::signal;
use utils::mqtt_util::MqttUtilImpl;

mod consumers;
mod producers;
mod services;
mod states;
mod controllers;
mod routes;
mod utils;

#[tokio::main]
async fn main() {
    let mqtt_util = Arc::new(MqttUtilImpl::new());
    MqttConsumerImpl::new(mqtt_util.clone()).await;
    let mqtt_producer = Arc::new(MqttProducerImpl::new(mqtt_util.clone()));
    let app = Router::new().merge(set_route(mqtt_producer.clone()));
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("{} axum: connected to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "0.0.0.0", "8080");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {
            println!("in ctrl c");
        },
        _ = terminate => {
            println!("in terminate");
        },
    }
}