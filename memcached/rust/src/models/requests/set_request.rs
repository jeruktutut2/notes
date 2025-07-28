use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct SetRequest {
    #[serde(rename = "message")]
    pub message: String
}