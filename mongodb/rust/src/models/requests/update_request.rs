use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct UpdateRequest {
    #[serde(rename = "id")]
    pub id: String,

    #[serde(rename = "test")]
    pub test: String
}