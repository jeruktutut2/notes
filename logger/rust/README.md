# LOGGER

## library
    cargo add axum --features "json macros ws"
    cargo add tokio --features full
    cargo add chrono
    cargo add log
    cargo add env_logger
    cargo add serde  --features derive
    cargo add serde_json
    cargo add regex

## run app
    RUST_BACKTRACE=full cargo run
    RUST_BACKTRACE=1 cargo run