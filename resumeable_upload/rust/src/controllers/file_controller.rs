use std::sync::Arc;

use axum::{extract::{Path, State}, http::{HeaderMap, StatusCode}, response::IntoResponse, Json};
use axum_extra::extract::Multipart;
use bytes::Bytes;
use serde_json::json;

use crate::{services::file_service::FileService, states::app_state::AppState};

pub async fn upload_handler(
    headers: HeaderMap,
    State(state): State<Arc<AppState>>,
    chunk: Bytes,
) -> impl IntoResponse {
    let file_id = match headers.get("X-File-Id") {
        Some(header_value) => {
            match header_value.to_str() {
                Ok(file_id) => file_id,
                Err(err) => {
                    println!("error: {}", err);
                    return (StatusCode::INTERNAL_SERVER_ERROR, Json(err.to_string()));
                }
            }
        },
        None => {
            println!("cannot find X-File-Id header");
            return (StatusCode::INTERNAL_SERVER_ERROR, Json("cannot find X-File-Id header".to_string()));
        }
    };
    let chunk_index = match headers.get("X-Chunk-Index") {
        Some(header_value) => {
            match header_value.to_str() {
                Ok(chunk_index) => chunk_index,
                Err(err) => {
                    println!("error: {}", err);
                    return (StatusCode::INTERNAL_SERVER_ERROR, Json(err.to_string()));
                }
            }
        },
        None => {
            println!("cannot find X-File-Id header");
            return (StatusCode::INTERNAL_SERVER_ERROR, Json("cannot find X-File-Id header".to_string()));
        }
    };
    // different ways to get header
    // let file_id = headers.get("X-File-Id").and_then(|v| v.to_str().ok()).unwrap_or("");
    // let chunk_index = headers.get("X-Chunk-Index").and_then(|v| v.to_str().ok()).and_then(|s| s.parse::<usize>().ok()).unwrap_or(0);
    let response = state.file_service.upload(file_id, chunk_index, chunk).await;
    return (StatusCode::OK, Json(response));
}

pub async fn merge_handler(
    headers: HeaderMap,
    State(state): State<Arc<AppState>>,
) -> impl IntoResponse {
    let file_id = headers.get("X-File-Id").and_then(|v| v.to_str().ok()).unwrap_or("");
    let total_chunks = headers.get("X-Total-Chunks").and_then(|v| v.to_str().ok()).unwrap_or("");
    let response = state.file_service.merge(file_id, total_chunks).await;
    return (StatusCode::OK, Json(response))
}

pub async fn check_file_handler(
    State(state): State<Arc<AppState>>,
    Path(file_id): Path<String>,
) -> impl IntoResponse {
    let response = state.file_service.check_file(file_id.as_str()).await;
    let data = json!({"response": response.0});
    return (StatusCode::OK, Json(data))
}

pub async fn upload_and_merge(
    State(state): State<Arc<AppState>>,
    mut multipart: Multipart,
) -> impl IntoResponse {
    let mut file_id: String = String::new();
    let mut chunk_index: String = String::new();
    let mut last_chunk_index: String = String::new();
    let mut chunk: Bytes = Bytes::new();

    while let Some(field) = multipart.next_field().await.unwrap() {
        let name = field.name().unwrap().to_string();

        match name.as_str() {
            "fieldId" => {
                file_id = field.text().await.unwrap();
            }
            "chunkIndex" => {
                chunk_index = field.text().await.unwrap();
            }
            "lastChunkIndex" => {
                last_chunk_index = field.text().await.unwrap();
            }
            "chunk" => {
                // let data = field.bytes().await.unwrap();
                chunk = field.bytes().await.unwrap();
            }
            _ => {}
        }
    }

    let response = state.file_service.upload_and_merge(file_id, chunk_index, last_chunk_index, chunk).await;
    return (StatusCode::OK, Json(response));
}