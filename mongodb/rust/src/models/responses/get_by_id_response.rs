use mongodb::bson::oid::ObjectId;
use serde::Serialize;

use crate::models::entities::test1::Test1;

#[derive(Debug, Serialize)]
pub struct GetByIdResponse {
    #[serde(rename = "id")]
    pub id: String,

    #[serde(rename = "test")]
    pub test: String
}

impl GetByIdResponse {
    pub fn set_get_by_id_response(test1: Test1) -> Self {
        Self { id: test1.id.to_hex(), test: test1.test }
    }
}