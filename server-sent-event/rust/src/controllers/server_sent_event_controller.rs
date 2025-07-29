use axum::{extract::State, response::sse::{Event, KeepAlive, Sse}, Router};
use std::{convert::Infallible};
use std::sync::{Arc, Mutex};
use std::time::Duration;
use axum::extract::Path;
use axum::routing::{get, post};
use tokio::sync::broadcast;
use tokio_stream::wrappers::{BroadcastStream, ReceiverStream};
use tokio_stream::{Stream, StreamExt};
use tokio::sync::mpsc;

async fn sse_handler(
    State(tx): State<broadcast::Sender<String>>,
) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let rx = tx.subscribe();

    let stream = BroadcastStream::new(rx)
        .map(|msg| match msg {
            Ok(msg) => Ok(Event::default().data(msg)),
            Err(_) => Ok(Event::default().data("Error receiving message")),
        });
    
    // needs to send something (:) in some interval to keep connection establish
    Sse::new(stream).keep_alive(KeepAlive::new().interval(Duration::from_secs(30)))
}

async fn sse_send_message(
    State(tx): State<broadcast::Sender<String>>,
    Path( message): Path<String>,
) -> &'static str {
    if let Err(e) = tx.send(message) {
        println!("Gagal mengirim pesan: {:?}", e);
        return "Gagal mengirim pesan";
    }
    "Pesan dikirim!"
}

pub fn sse() -> Router {
    let (tx, _rx) = broadcast::channel(100);
    Router::new()
        .route("/sse", get(sse_handler))
        .route("/sse/{message}", post(sse_send_message))
        .with_state(tx)
}

async fn sse_manual_handler(
    State(clients): State<Arc<Mutex<Vec<mpsc::Sender<String>>>>>,
) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let (tx, rx) = mpsc::channel::<String>(10);

    {
        let mut clients = clients.lock().unwrap();
        clients.push(tx);
        println!("Klien baru terhubung! Total klien: {}", clients.len());
    }

    let stream = ReceiverStream::new(rx).map(|msg| Ok(Event::default().data(msg)));

    Sse::new(stream).keep_alive(KeepAlive::default())
}

async fn sse_manual_send_message(
    State(clients): State<Arc<Mutex<Vec<mpsc::Sender<String>>>>>,
    Path(message): Path<String>,
) -> &'static str {
    let clients = clients.lock().unwrap();
    for client in clients.iter() {
        if let Err(_) = client.try_send(message.clone()) {
            println!("cannot sent message");
        }
    }
    "Pesan dikirim!"
}

pub fn sse_manual() -> Router {
    type Clients = Arc<Mutex<Vec<mpsc::Sender<String>>>>;
    let clients: Clients = Arc::new(Mutex::new(Vec::new()));
    Router::new()
        .route("/sse-manual", get(sse_manual_handler))
        .route("/sse-manual/{message}", post(sse_manual_send_message))
        .with_state(clients.clone())
}