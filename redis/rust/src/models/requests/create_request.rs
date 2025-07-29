use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct CreateRequest {
    pub test: String
}