use mongodb::bson::oid::ObjectId;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Test1 {
    #[serde(rename = "_id")]
    pub id: ObjectId,
    pub test: String
}