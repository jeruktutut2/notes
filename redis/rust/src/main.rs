use std::sync::Arc;
use axum::Router;
use chrono::Local;
use tokio::{net::TcpListener, signal};
use tokio::sync::Mutex;
use crate::routes::route::set_routes;
use crate::utils::redis_util::RedisUtilImpl;

mod models;
mod services;
mod utils;
mod controllers;
mod states;
mod routes;

#[tokio::main]
async fn main() {
    let redis_util = Arc::new(Mutex::new(RedisUtilImpl::new().await));
    let app = Router::new().merge(set_routes(redis_util.clone()));
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("{} axum: connected to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "0.0.0.0", "8080");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();

    // actually this is unnecessary, cause rust will drop any variable that out of scope, this just to make it explicit (for me)
    drop(redis_util);
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