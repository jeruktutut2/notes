use std::sync::Arc;

use axum::{extract::State, http::{HeaderMap, HeaderValue, StatusCode}, response::{IntoResponse, Response}};

use crate::{services::pdf_service::PdfService, states::app_state::AppState};

pub async fn generate_pdf(
    State(state): State<Arc<AppState>>
) -> Response {
    match state.pdf_service.generate_pdf_from_string().await {
        Ok(pdf_bytes) => {
            let mut headers = HeaderMap::new();
            headers.insert("Content-Type", HeaderValue::from_static("application/pdf"));
            headers.insert("Content-Disposition", HeaderValue::from_static("attachment; filename=\"output.pdf\""));
            (headers, pdf_bytes).into_response()
        }
        Err(err) => {
            eprintln!("PDF generation error: {:?}", err);
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                "Failed to generate pdf"
            ).into_response()
        }
    }
}