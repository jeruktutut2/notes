use std::sync::Arc;
use axum::extract::rejection::JsonRejection;
use axum::extract::State;
use axum::response::IntoResponse;
use axum::response::Json;
use crate::models::requests::create_request::CreateRequest;
use crate::models::responses::response::Response;
use crate::services::test1_service::Test1Service;
use crate::states::app_state::AppState;

pub async fn create_handler(State(state): State<Arc<AppState>>, create_request_result: Result<Json<CreateRequest>, JsonRejection>) -> impl IntoResponse {
    let create_request = match create_request_result {
        Ok(Json(create_request)) => create_request,
        Err(e) => {
            println!("error: {}", e);
            let error_message = match e {
                JsonRejection::JsonDataError(err) => {format!("JSON Data is not correct: {}", err)}
                JsonRejection::JsonSyntaxError(_) => {"Format JSON salah.".to_string()}
                JsonRejection::MissingJsonContentType(_) => {"Content-Type must an `application/json`.".to_string()}
                JsonRejection::BytesRejection(err) => {format!("Failed when Deserializing: {}", err)}
                _ => "Error happened when processing JSON body .".to_string(),
            };
            let response = Response::set_bad_request_response(error_message);
            return (response.http_status_code, Json(response.body_response));
        }
    };
    let response = state.test1_service.create(create_request).await;
    (response.http_status_code, Json(response.body_response))
}