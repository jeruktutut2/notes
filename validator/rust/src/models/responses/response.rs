use std::collections::HashMap;
use axum::http::StatusCode;
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct MessageResponse {
    #[serde(rename = "message")]
    pub message: String
}

#[derive(Debug, Serialize)]
pub struct BodyResponse<T> {
    #[serde(rename = "data")]
    pub data: Option<T>,

    #[serde(rename = "errors")]
    pub errors: Option<HashMap<String, String>>
}

#[derive(Debug)]
pub struct Response<T> {
    pub http_status_code: StatusCode,
    pub body_response: BodyResponse<T>
}

impl <T>Response<T> {
    pub fn set_created_response(data: T) -> Self {
        Self {
            http_status_code: StatusCode::CREATED,
            body_response: BodyResponse {
                data: Some(data),
                errors: None
            }
        }
    }

    pub fn set_bad_request_response(message: String) -> Self {
        let mut error_message = HashMap::new();
        error_message.insert("message".to_string(), message);
        Self {
            http_status_code: StatusCode::BAD_REQUEST,
            body_response: BodyResponse {
                data: None,
                errors: Some(error_message)
            }
        }
    }

    pub fn set_validation_error(validation_error: HashMap<String, String>) -> Self {
        Self {
            http_status_code: StatusCode::BAD_REQUEST,
            body_response: BodyResponse {
                data: None,
                errors: Some(validation_error)
            }
        }
    }

    pub fn set_internal_server_error_response() -> Self {
        let mut error_message = HashMap::new();
        error_message.insert("message".to_string(), "internal server error".to_string());
        Self {
            http_status_code: StatusCode::INTERNAL_SERVER_ERROR,
            body_response: BodyResponse {
                data: None,
                errors: Some(error_message)
            }
        }
    }
}