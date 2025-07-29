use serde::{Serialize, Deserialize};
use sqlx::FromRow;

#[derive(FromRow, Debug, Default, Serialize, Deserialize)]
pub struct CreateRequest {
    #[serde(rename = "test")]
    pub test: String
}