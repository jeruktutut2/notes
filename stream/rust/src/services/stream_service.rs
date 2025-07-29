use std::time::Duration;

use serde_json::json;
use tokio::sync::mpsc;
use tokio::time::sleep;

pub fn stream_service() -> mpsc::Receiver<String> {
    let (tx, rx) = mpsc::channel::<String>(10);
    tokio::spawn(async move {
        let stream1 = json!({ "response": "stream1" }).to_string();
        let _ = tx.send(stream1).await;

        sleep(Duration::from_secs(2)).await;

        let stream2 = json!({ "response": "stream2" }).to_string();
        let _ = tx.send(stream2).await;

        sleep(Duration::from_secs(2)).await;

        return; // to force process to get out from task tokio::spawn

        let stream3 = json!({ "response": "stream3" }).to_string();
        let _ = tx.send(stream3).await;
    });

    rx
}