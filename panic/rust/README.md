# PANIC

## library
    cargo add axum --features "json macros ws"
    cargo add tokio --features full
    cargo add chrono
    cargo add tower-http --features full
    cargo add tower --features full

## run app
    RUST_BACKTRACE=full cargo run