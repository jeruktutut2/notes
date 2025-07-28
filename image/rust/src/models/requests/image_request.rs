use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct ImageRequest {
    #[serde(rename = "image")]
    pub image: String
}