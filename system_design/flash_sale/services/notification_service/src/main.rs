use axum::{
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::env;
use std::net::SocketAddr;
use std::sync::{Arc, Mutex};
use tower_http::cors::CorsLayer;

#[derive(Serialize, Deserialize, Clone)]
struct NotificationEvent {
    id: String,
    user_id: String,
    event_type: String, // "ORDER_CREATED", "PAYMENT_SUCCESS", "PAYMENT_FAILED", "STOCK_RESTORED"
    message: String,
    timestamp: String,
}

#[derive(Deserialize)]
struct PushNotificationRequest {
    user_id: String,
    event_type: String,
    message: String,
}

struct AppState {
    logs: Mutex<Vec<NotificationEvent>>,
}

#[tokio::main]
async fn main() {
    let state = Arc::new(AppState {
        logs: Mutex::new(vec![
            NotificationEvent {
                id: "notif-001".to_string(),
                user_id: "22222222-2222-2222-2222-222222222222".to_string(),
                event_type: "SYSTEM_INIT".to_string(),
                message: "Flash Sale platform notification service initialized.".to_string(),
                timestamp: chrono::Utc::now().to_rfc3339(),
            }
        ]),
    });

    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/v1/notifications/events", get(get_events))
        .route("/api/v1/notifications/push", post(push_notification))
        .with_state(state)
        .layer(CorsLayer::permissive());

    let port: u16 = env::var("PORT")
        .unwrap_or_else(|_| "8086".to_string())
        .parse()
        .expect("PORT must be a number");

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("Rust Notification Service (Axum) running on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn health_check() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "UP",
        "service": "notification_service",
        "framework": "Axum (Rust)"
    }))
}

async fn get_events(
    axum::extract::State(state): axum::extract::State<Arc<AppState>>,
) -> Json<Vec<NotificationEvent>> {
    let logs = state.logs.lock().unwrap();
    Json(logs.clone())
}

async fn push_notification(
    axum::extract::State(state): axum::extract::State<Arc<AppState>>,
    Json(payload): Json<PushNotificationRequest>,
) -> Json<NotificationEvent> {
    let new_event = NotificationEvent {
        id: format!("notif-{}", chrono::Utc::now().timestamp_millis()),
        user_id: payload.user_id,
        event_type: payload.event_type,
        message: payload.message,
        timestamp: chrono::Utc::now().to_rfc3339(),
    };

    {
        let mut logs = state.logs.lock().unwrap();
        logs.push(new_event.clone());
    }

    Json(new_event)
}
