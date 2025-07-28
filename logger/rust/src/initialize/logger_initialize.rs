use std::io::Write;
use std::thread;
use chrono::Utc;
use env_logger::Builder;
use env_logger::fmt::Formatter;
use log::Record;
use regex::Regex;
use serde_json::json;

fn json_formatter(buf: &mut Formatter, record: &Record) -> std::io::Result<()> {
    let thread_name = thread::current().name().unwrap_or("unknown").to_string();
    let message = record.args().to_string();
    let request_id_message = Regex::new(r"requestId=([\w\d-]+)").unwrap();
    let request_id = request_id_message.captures(&message)
        .and_then(|cap| cap.get(1))
        .map_or("unknown", |m| m.as_str());
    let stacktrace_message = Regex::new(r"stacktrace=([\w\d-]+)").unwrap();
    let stacktrace = stacktrace_message.captures(&message)
        .and_then(|cap| cap.get(1))
        .map_or("unknown", |m| m.as_str());
    let log_entry = json!({
        "timestamp": Utc::now().to_rfc3339(), 
        "level": record.level().to_string(),
        "message": record.args().to_string(),
        "target": record.target(),
        "file": record.file().unwrap_or("unknown"),
        "line": record.line().unwrap_or(0),
        "module": record.module_path().unwrap_or("unknown"),
        "thread": thread_name,
        "request_id": request_id,
        "stacktrace": stacktrace
    });
    let json_string = log_entry.to_string();
    buf.write_all(json_string.as_bytes())?;
    buf.write_all(b"\n")?;
    Ok(())
}

pub fn set_logger() {
    Builder::new()
        .format(json_formatter)
        .filter_level(log::LevelFilter::Debug)
        .init();
}