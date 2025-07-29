use axum::{middleware, routing::get, Router};

use crate::{controllers::request_id_controller, middlewares};
pub fn set_test_route() -> Router {
    Router::new()
        .route("/test", get(request_id_controller::get_test))
        .layer(middleware::from_fn(middlewares::request_id_middleware::set_request_id))
}