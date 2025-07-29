use serde::{Serialize, Deserialize};
use sqlx::FromRow;

#[derive(FromRow, Debug, Default, Serialize, Deserialize)]
pub struct Test1 {
    #[serde(rename = "id")]
    pub id: i32,
    #[serde(rename = "test")]
    pub test: String
}