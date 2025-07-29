use chrono::{DateTime, Duration, FixedOffset, NaiveDate, TimeZone};

use crate::models::{requests::millisecond_request::MillisecondRequest, responses::millisecond_response::MillisecondResponse};

pub trait MillisecondService {
    async fn get_by_gmt_plus8(&self, millisecond_request: MillisecondRequest) -> MillisecondResponse;
    async fn get_by_gmt_minus8(&self, millisecond_request: MillisecondRequest) -> MillisecondResponse;
}

pub struct MillisecondServiceImpl {

}

impl MillisecondServiceImpl {
    pub fn new() -> MillisecondServiceImpl {
        MillisecondServiceImpl {  }
    }
}

impl MillisecondService for MillisecondServiceImpl {
    async fn get_by_gmt_plus8(&self, millisecond_request: MillisecondRequest) -> MillisecondResponse {
        let offset_plus8 = FixedOffset::east_opt(8 * 60 * 60).unwrap();
        let naive_dt = NaiveDate::from_ymd_opt(millisecond_request.year, millisecond_request.month, millisecond_request.date).unwrap().and_hms_opt(millisecond_request.hour, millisecond_request.minute, millisecond_request.second).unwrap();
        let dt_plus8: DateTime<FixedOffset> = offset_plus8.from_local_datetime(&naive_dt).unwrap();
        let dt_plus8_add1_hour = dt_plus8 + Duration::hours(1);
        MillisecondResponse::set_millisecond_response(dt_plus8.to_string(), dt_plus8.timestamp_millis(), dt_plus8_add1_hour.to_string(), dt_plus8_add1_hour.timestamp_millis())
    }

    async fn get_by_gmt_minus8(&self, millisecond_request: MillisecondRequest) -> MillisecondResponse {
        let offset_minus8 = FixedOffset::west_opt(8 * 60 * 60).unwrap();
        let naive_dt = NaiveDate::from_ymd_opt(millisecond_request.year, millisecond_request.month, millisecond_request.date).unwrap().and_hms_opt(millisecond_request.hour, millisecond_request.minute, millisecond_request.second).unwrap();
        let dt_plus8: DateTime<FixedOffset> = offset_minus8.from_local_datetime(&naive_dt).unwrap();
        let dt_minus8_add1_hour = dt_plus8 + Duration::hours(1);
        MillisecondResponse::set_millisecond_response(dt_plus8.to_string(), dt_plus8.timestamp_millis(), dt_minus8_add1_hour.to_string(), dt_minus8_add1_hour.timestamp_millis())
    }
}