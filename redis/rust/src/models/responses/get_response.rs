use serde::Serialize;
use crate::models::entities::test1::Test1;

#[derive(Debug, Serialize)]
pub struct GetResponse {
    pub id: String,
    pub test: String,
}

impl GetResponse {
    pub fn set_get_response(test1: Test1) -> Self {
        Self {
            id: test1.id,
            test: test1.test,
        }
    }
}