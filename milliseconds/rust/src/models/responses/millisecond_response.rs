use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct MillisecondResponse {
    #[serde(rename = "datetime")]
    pub datetime: String,
    #[serde(rename = "millisecond")]
    pub millisecond: i64,
    #[serde(rename = "add1Hour")]
    pub add1_hour: String,
    #[serde(rename = "add1HourMillisecond")]
    pub add1_hour_millisecond: i64
}

impl MillisecondResponse {
    pub fn set_millisecond_response(datetime: String, millisecond: i64, add1_hour: String, add1_hour_millisecond: i64) -> MillisecondResponse {
        MillisecondResponse { datetime:datetime, millisecond: millisecond, add1_hour: add1_hour, add1_hour_millisecond: add1_hour_millisecond }
    }
}