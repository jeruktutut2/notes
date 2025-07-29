use serde::{Serialize, Deserialize};
use sqlx::FromRow;

#[derive(FromRow, Debug, Default, Serialize, Deserialize)]
pub struct DeleteRequest {
    #[serde(rename = "id")]
    pub id: i32
}