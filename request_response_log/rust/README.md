# REQUEST RESPONSE LOG

## create project
    cargo new <project name>

## library
    cargo add axum
    cargo add tokio
    cargo add serde_json
    cargo add chrono
    cargo add uuid
    cargo add http-body-util

## curl
    curl http://localhost:8080/

    curl -X POST "http://localhost:8080/" \
     -H "Content-Type: application/json" \
     -d '{"name": "name", "address": "address"}'

## link
    https://stackoverflow.com/questions/76180158/axum-middleware-to-log-the-response-body
    https://github.com/tokio-rs/axum/blob/main/examples/print-request-response/src/main.rs