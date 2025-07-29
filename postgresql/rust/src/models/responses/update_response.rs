use serde::Serialize;

use crate::models::entities::test1::Test1;

#[derive(Debug, Serialize)]
pub struct UpdateResponse {
    #[serde(rename = "id")]
    pub id: i32,

    #[serde(rename = "test")]
    pub test: String
}

impl UpdateResponse {
    pub fn set_update_response(test1: Test1) -> Self {
        Self { 
            id: test1.id, 
            test: test1.test 
        }
    }
}