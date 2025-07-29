use std::process;

use axum::Router;
use chrono::Local;
use routes::route::set_route;
use tokio::net::TcpListener;
use tokio::signal;
use utils::rabbitmq_util::{RabbitMQUtil, RabbitMQUtilImpl};

mod utils;
mod services;
mod states;
mod controllers;
mod routes;

#[tokio::main]
async fn main() {
    let rabbitmq_util = RabbitMQUtilImpl::new().await;
    let consumer = rabbitmq_util.set_consumer().await;
    let producer = rabbitmq_util.set_producer().await;

    let app = Router::new().merge(set_route(producer.clone()));
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("{} axum: connected to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "0.0.0.0", "8080");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();

    match consumer.close().await {
        Ok(_) => (),
        Err(err) => {
            print!("error: {}", err);
            process::exit(1);
        }
    };

    match producer.close().await {
        Ok(_) => (),
        Err(err) => {
            println!("error: {}", err);
            process::exit(1);
        }
    }
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