use serde::Serialize;

use crate::models::entities::test1::Test1;

#[derive(Debug, Serialize)]
pub struct CreateResponse {
    #[serde(rename = "id")]
    pub id: i32,

    #[serde(rename = "test")]
    pub test: String
}

impl CreateResponse {
    pub fn set_craeate_response(test1: Test1) -> Self {
        Self { id: test1.id, test: test1.test }
    }
}