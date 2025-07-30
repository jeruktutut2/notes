use axum::{extract::Request, middleware::Next, response::Response};
use tokio_util::sync::CancellationToken;

// couldn't found yet, how to get information (log), when timeout happen and or http connection is closed
// however, without those, app run well, means timeout and http connection closed (database manipulation) run well
#[derive(Clone)]
pub struct TimeoutToken(pub CancellationToken);

#[derive(Clone)]
pub struct HttpCloseConnectionToken(pub CancellationToken);

pub async fn set_cancellation_token_middleware(
    mut request: Request,
    next: Next
) -> Response {
    let timeout_token = TimeoutToken(CancellationToken::new());
    request.extensions_mut().insert(timeout_token.clone());
    let http_closed_connection_token = HttpCloseConnectionToken(CancellationToken::new());
    request.extensions_mut().insert(http_closed_connection_token.clone());
    next.run(request).await
}