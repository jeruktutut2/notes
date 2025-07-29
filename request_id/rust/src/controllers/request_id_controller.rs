use std::sync::Arc;

use axum::{http::StatusCode, response::IntoResponse, Extension, Json};
use serde_json::{json, Value};

use crate::middlewares;

pub async fn get_test(Extension(data): Extension<Arc<middlewares::model_middleware::ModelMiddleware>>) -> impl IntoResponse {
    let body: Value = json!({"foo": "bar", "requestId": data.request_id});
    (StatusCode::OK, Json(body))
}