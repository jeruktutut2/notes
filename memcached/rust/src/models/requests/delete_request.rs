use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct DeleteRequest {
    #[serde(rename = "id")]
    pub id: String
}