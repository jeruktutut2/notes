use std::backtrace::Backtrace;
use log::{debug, error, info, trace, warn};

pub trait LoggerService {
    async fn check_logger(&self) -> String;
}

pub struct LoggerServiceImpl {

}

impl LoggerServiceImpl {
    pub fn new() -> LoggerServiceImpl {
        LoggerServiceImpl {}
    }
}

impl LoggerService for LoggerServiceImpl {
    async fn check_logger(&self) -> String {
        let bt = Backtrace::capture();
        trace!("Ini log TRACE, requestId={}, stacktrace={}", "requestId123", bt.to_string().replace("\n", "").replace("\r", "").replace("\t", ""));
        debug!("Ini log DEBUG, requestId={}, stacktrace={}", "requestId123", bt.to_string().replace("\n", "").replace("\r", "").replace("\t", ""));
        info!("Ini log INFO, requestId={}, stacktrace={}", "requestId123", bt.to_string().replace("\n", "").replace("\r", "").replace("\t", ""));
        warn!("Ini log WARNING, requestId={}, stacktrace={}", "requestId123", bt.to_string().replace("\n", "").replace("\r", "").replace("\t", ""));
        error!("Ini log ERROR, requestId={}, stacktrace={}", "requestId123", bt.to_string().replace("\n", "").replace("\r", "").replace("\t", ""));
        "ok".to_string()
    }
}