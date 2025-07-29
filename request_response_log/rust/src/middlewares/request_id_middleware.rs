use std::sync::Arc;

use axum::{extract::Request, middleware::Next, response::Response};
use uuid::Uuid;

use super::model_middleware;

pub async fn set_request_id(
    mut request: Request,
    next: Next,
) -> Response {
    let data = model_middleware::ModelMiddleware {
        request_id: Uuid::new_v4().to_string(),
    };
    request.extensions_mut().insert(Arc::new(data));
    let response = next.run(request).await;
    response
}