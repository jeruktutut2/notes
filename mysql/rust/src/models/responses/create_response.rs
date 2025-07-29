use serde::{Serialize, Deserialize};
use sqlx::FromRow;

#[derive(FromRow, Debug, Default, Serialize, Deserialize)]
pub struct CreateResponse {
    #[serde(rename = "id")]
    pub id: i32,
    #[serde(rename = "test")]
    pub test: String
}

// #[derive(FromRow, Debug, Default, Serialize, Deserialize)]
// pub struct GetByIdResponse {
//     #[serde(rename = "id")]
//     pub id: i32,
//     #[serde(rename = "test")]
//     pub test: String
// }