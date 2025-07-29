use sqlx::prelude::FromRow;
use serde::{Serialize, Deserialize};

#[derive(Debug, FromRow, Serialize, Deserialize)]
pub struct Test1 {
    #[serde(rename = "id")]
    pub id: i32,

    #[serde(rename = "test")]
    pub test: String
}