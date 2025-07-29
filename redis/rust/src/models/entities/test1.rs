use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Test1 {
    pub id: String,
    pub test: String
}