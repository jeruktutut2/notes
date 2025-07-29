use std::sync::Arc;

use axum::{ body::Body, extract::Request, http::StatusCode, middleware::Next, response::{IntoResponse, Response}, Json};
use chrono::Utc;
use serde_json::{json, Value};
use http_body_util::BodyExt;

use crate::middlewares::model_middleware;

pub async fn set_request_response_log(
    request: Request,
    next: Next,
) -> Response {
    println!("request");

    let data = match request.extensions().get::<Arc<model_middleware::ModelMiddleware>>() {
        Some(data) => data.clone(),
        None => {
            let body: Value = json!({"foo": "bar"});
            return (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response();
        }
    };
    
    let mut host = "";
    let headers = request.headers().clone();
    if let Some(host_header) = headers.get("host") {
        if let Ok(host_str) = host_header.to_str() {
            host = host_str
        }
    }

    let protocol = headers.get("x-forwarded-proto")
        .and_then(|v|v.to_str().ok())
        .unwrap_or("http");
    let method = request.method().clone();
    let request_uri = request.uri().clone();
    let url_path = request_uri.path();
    let query_param = request_uri.query().unwrap_or("");

    // request cannot be clone, so ne to clone it in each function, for example: request.method().clone(), request.uri().clone()
    let (parts, body) = request.into_parts();
    // please import use http_body_util::BodyExt; to use collect() below
    let bytes = match body.collect().await {
        Ok(collected) => collected.to_bytes(),
        Err(err) => {
            let body: Value = json!({"foo": "bar", "error": err.to_string()});
            return (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response();
        }
    };
    let byte_clone = bytes.clone();
    let request_body = match std::str::from_utf8(&byte_clone) {
        Ok(body) => body,
        Err(err) => {
            let body: Value = json!({"foo": "bar", "error": err.to_string()});
            return (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response();
        }
    };
    let request = Request::from_parts(parts, Body::from(bytes));

    // {"requestTime": "` + datetimeNowRequest.String() + `", "app": "project-backend", "method": "` + requestMethod + `","requestId":"` + requestId + `","host": "` + host + `","urlPath":"` + urlPath + `","protocol":"` + protocol + `","body": ` + requestBody + `, "userAgent": "` + userAgent + `", "remoteAddr": "` + remoteAddr + `", "forwardedFor": "` + forwardedFor + `"}
    println!("requestTime: {}, app: {}, method: {}, requestId: {}, host: {}, urlPath: {}, queryParam: {}, protocol: {}, body: {}", 
        Utc::now().format("%Y-%m-%d %H:%M:%S%.3f UTC").to_string(), 
        "project-backend", 
        method,
        data.request_id,
        host,
        url_path,
        query_param,
        protocol,
        request_body
    );

    let response = next.run(request).await;

    let response_status = response.status().clone();
    let (parts, body) = response.into_parts();
    let bytes = match body.collect().await {
        Ok(collected) => collected.to_bytes(),
        Err(err) => {
            let body: Value = json!({"foo": "bar", "error": err.to_string()});
            return (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response();
        }
    };
    let byte_clone = bytes.clone();
    let request_body = match std::str::from_utf8(&byte_clone) {
        Ok(body) => body,
        Err(err) => {
            let body: Value = json!({"foo": "bar", "error": err.to_string()});
            return (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response();
        }
    };
    println!("responseTime: {}, app: {}, requestId: {}, responseStatus: {}, response: {}",
        Utc::now().format("%Y-%m-%d %H:%M:%S%.3f UTC").to_string(),
        "project-backend",
        data.request_id,
        response_status,
        request_body
    );
    let response = Response::from_parts(parts, Body::from(bytes));
    
    response
}