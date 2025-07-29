use std::sync::Arc;

use axum::Router;
use chrono::Local;
use models::entities::test1::Test1;
use mongodb::Collection;
use routes::route::set_route;
use tokio::{net::TcpListener, signal};
use utils::mongo_util::{MongoUtil, MongoUtilImpl};

mod utils;
mod models;
mod repositories;
mod services;
mod controllers;
mod states;
mod routes;

#[tokio::main]
async fn main() {
    let mongo_util = MongoUtilImpl::new().await;
    let test1_collection: Collection<Test1> = mongo_util.get_database().await.collection("test1");
    let collection = Arc::new(test1_collection);

    let app = Router::new().merge(set_route(collection.clone()));
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