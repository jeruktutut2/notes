use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use axum::extract::ws::{Message, WebSocket};
use axum::extract::{Path, State, WebSocketUpgrade};
use axum::response::IntoResponse;
use axum::routing::get;
use axum::Router;
use chrono::Local;
use futures::{SinkExt, StreamExt};
use tokio::net::TcpListener;
use tokio::signal;
use tokio::sync::mpsc::{self, UnboundedSender};
use tokio::sync::{broadcast, Mutex};

#[derive(Debug, Clone)]
struct AppState {
    clients: Arc<Mutex<HashMap<String, UnboundedSender<Message>>>>
    // sender: broadcast::Sender<String>
}

#[tokio::main]
async fn main() {
    // println!("Hello, world!");
    // let (sender, _receiver) = broadcast::channel(100);
    let app_state = AppState{
        clients: Arc::new(Mutex::new(HashMap::new()))
        // sender
    };
    let app = Router::new()
        .route("/ws/chat/connect/{clientId}", get(handler))
        .with_state(app_state);
    let listener = TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("{} axum: connected to {} {}", Local::now().format("%Y-%m-%d %H:%M:%S%.3f").to_string(), "0.0.0.0", "8080");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

// async fn test_handler() -> impl IntoResponse{}

async fn handler(ws: WebSocketUpgrade, State(state): State<AppState>, Path(client_id): Path<String>) -> impl IntoResponse {
    ws.on_upgrade(move |socket| websocket_handler(socket, state.clone(), client_id.clone()))
}

// websocket_handler(Arc::new(socket), state, client_id)

// async fn method() {}

async fn websocket_handler(web_socket: WebSocket, state: AppState, client_id: String) {
    // let mut receiver = state.sender.subscribe();
    // let arc_web_socket = Arc::new(ws);
    // state.clients.lock().await.insert(client_id.clone());
    println!("New client connected: {}", client_id.clone());

    let (mut ws_sender, mut ws_receiver) = web_socket.split();
    let (tx, mut rx) = mpsc::unbounded_channel::<Message>();
    state.clients.lock().await.insert(client_id.clone(), tx);

    tokio::spawn(async move {
        while let Some(message) = rx.recv().await {
            if ws_sender.send(message).await.is_err() {
                break;
            }
        }
    });

    while let Some(Ok(message)) = ws_receiver.next().await {
        match message {
            Message::Text(text) => {
                // let parts: Vec<&str> = text.split(":").collect();
                // match state.clients.lock().await.get(parts[0]) {
                //     Some(client) => {
                //         let _ = state.sender.send(parts[1].to_string());
                //     },
                //     None => {
                //         println!("Client not found: {}", parts[0]);
                //         break
                //     }
                // };
                if let Some((target_id, message)) = text.split_once(":") {
                    match state.clients.lock().await.get(target_id) {
                        Some(target_tx) => {
                            let composed_message = format!("client id: {} message: {}", client_id.clone(), message).into();
                            let _ = target_tx.send(Message::Text(composed_message));
                        },
                        _ => {
                            break;
                        }
                    };
                }
            },
            Message::Close(_) => {
                break;
            },
            _ => {
                break
            }
        }
    }

    state.clients.lock().await.remove(&client_id);
    println!("Client disconnected: {}", client_id);
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

// async fn handler(ws: WebSocketUpgrade) -> impl IntoResponse {
//     ws.on_upgrade(move |web_socket| handle_web_socket(web_socket))
// }

// async fn handle_web_socket(web_socket: WebSocket)