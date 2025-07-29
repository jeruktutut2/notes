use axum::response::sse::{Event, Sse};
use tokio_stream::StreamExt;
use tokio_stream::wrappers::ReceiverStream;
use std::{convert::Infallible};

use crate::services::stream_service::stream_service;

pub async fn stream_data() -> Sse<impl tokio_stream::Stream<Item = Result<Event, Infallible>>> {
    let rx = stream_service();

    let stream = ReceiverStream::new(rx)
        .map(|msg| Ok(Event::default().data(msg)));

        Sse::new(stream)
}