use serde::Serialize;

use crate::models::entities::test1::Test1;

#[derive(Debug, Serialize)]
pub struct GetAllResponse {
    #[serde(rename = "id")]
    pub id: String,

    #[serde(rename = "test")]
    pub test: String
}

impl GetAllResponse {
    pub fn set_get_all_response(test1s: Vec<Test1>) -> Vec<GetAllResponse> {
        let mut get_all_responses: Vec<GetAllResponse> = Vec::new();
        for test1 in test1s {
            get_all_responses.push(GetAllResponse { id: test1.id.to_string(), test: test1.test });
        }
        get_all_responses
    }
}