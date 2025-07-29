use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct DeleteRequest {
    pub id: String,
}