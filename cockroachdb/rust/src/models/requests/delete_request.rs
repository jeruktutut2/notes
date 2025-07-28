use serde::Deserialize;
use uuid::Uuid;

#[derive(Debug, Deserialize)]
pub struct DeleteRequest {
    #[serde(rename = "id")]
    pub id: Uuid
}