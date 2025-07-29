use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct CreateRequest {
    #[serde(rename = "test")]
    pub test: String
}