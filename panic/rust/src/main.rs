use axum::Router;
use chrono::Local;
use routes::route::set_route;
use tokio::{net::TcpListener, signal};
use tower::ServiceBuilder;
use tower_http::catch_panic::CatchPanicLayer;

mod services;
mod states;
mod controllers;
mod routes;
mod middlewares;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .merge(set_route())
        .layer(
            ServiceBuilder::new()
                .layer(CatchPanicLayer::new())
        );
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
