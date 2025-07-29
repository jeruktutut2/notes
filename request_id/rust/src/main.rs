use std::time::Duration;

use tokio::net::TcpListener;
use tokio::signal;
use axum::{routing::get, Router};
use tokio::time::sleep;

mod controllers;
mod routes;
mod middlewares;

#[tokio::main]
async fn main() {
    let app = Router::new()
    .route("/slow", get(|| sleep(Duration::from_secs(5))))
    .merge(routes::route::set_test_route());

    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
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