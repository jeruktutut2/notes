use serde::Deserialize;
use uuid::Uuid;

#[derive(Debug, Deserialize)]
pub struct UpdateRequest {
    #[serde(rename = "id")]
    pub id: Uuid,

    #[serde(rename = "test")]
    pub test: String
}