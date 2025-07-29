use serde::Deserialize;


#[derive(Debug, Deserialize)]
pub struct MillisecondRequest {
    #[serde(rename = "year")]
    pub year: i32,
    #[serde(rename = "month")]
    pub month: u32,
    #[serde(rename = "date")]
    pub date: u32,
    #[serde(rename = "hour")]
    pub hour: u32,
    #[serde(rename = "minute")]
    pub minute: u32,
    #[serde(rename = "second")]
    pub second: u32
}