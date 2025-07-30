use std::{sync::Arc, time::Duration};

use axum::{middleware::from_fn, Router};
use chrono::Local;
use middlewares::cancellation_token_middleware::set_cancellation_token_middleware;
use routes::route::set_route;
use tokio::{net::TcpListener, signal};
use tower_http::timeout::TimeoutLayer;
use utils::postgres_util::{PostgresUtil, PostgresUtilImpl};

mod utils;
mod repositories;
mod models;
mod controllers;
mod services;
mod states;
mod routes;
mod middlewares;

#[tokio::main]
async fn main() {
    let postgres_util = Arc::new(PostgresUtilImpl::new().await);
    let app = Router::new()
        .merge(set_route(postgres_util.clone()))
        .layer(from_fn(set_cancellation_token_middleware))
        .layer(TimeoutLayer::new(Duration::from_secs(10)));
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("{} axum: connected to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "0.0.0.0", "8080");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
    postgres_util.close().await;
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