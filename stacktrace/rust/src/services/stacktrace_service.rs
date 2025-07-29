use std::backtrace::Backtrace;

pub trait StacktraceService {
    async fn printStacktrace(&self) -> String;
}

pub struct StacktraceServiceImpl {

}

impl StacktraceServiceImpl {
    pub fn new() -> StacktraceServiceImpl {
        StacktraceServiceImpl{

        }
    }
}

impl StacktraceService for StacktraceServiceImpl {
    async fn printStacktrace(&self) -> String {
        let bt = Backtrace::capture();
        println!("{}", bt);
        "ok".to_string()
    }
}