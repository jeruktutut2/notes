use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct CreateResponse {
    pub email: String,
    pub username: String,
    pub phone_number: String,
    pub password: String,
}

impl CreateResponse {
    pub fn new(email: String, username: String, phone_number: String, password: String) -> Self {
        Self {
            email,
            username,
            phone_number,
            password,
        }
    }
}