use std::sync::Arc;

use crate::services::stacktrace_service::StacktraceServiceImpl;

pub struct AppState {
    pub stacktrace_service: Arc<StacktraceServiceImpl>
}