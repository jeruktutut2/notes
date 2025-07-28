use std::sync::Arc;

use axum::Router;
use chrono::Local;
use routes::route::set_route;
use tokio::net::TcpListener;
use tokio::signal;
use utils::cockroachdb_util::{CockroachDbUtil, CockroachDbUtilImpl};

mod utils;
mod models;
mod services;
mod repositories;
mod controllers;
mod states;
mod routes;

#[tokio::main]
async fn main() {
    let cockroachdb_util = Arc::new(CockroachDbUtilImpl::new().await);
    let app = Router::new().merge(set_route(cockroachdb_util.clone()));
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("{} axum: connected to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "0.0.0.0", "8080");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
    cockroachdb_util.close().await
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