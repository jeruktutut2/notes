use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct UpdateRequest {
    #[serde(rename = "id")]
    pub id: i32,

    #[serde(rename = "test")]
    pub test: String
}