use axum::{http::StatusCode, middleware, response::IntoResponse, routing::post, Json, Router};
use serde_json::{json, Value};
use tokio::{net::TcpListener, signal};

mod middlewares;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", post(test))
        .layer(middleware::from_fn(middlewares::request_response_log::set_request_response_log))
        .layer(middleware::from_fn(middlewares::request_id_middleware::set_request_id));
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn test() -> impl IntoResponse {
    let body: Value = json!({"foo": "bar"});
    (StatusCode::OK, Json(body))
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