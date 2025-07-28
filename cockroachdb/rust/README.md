# COCKROACHDB

## library
    cargo add axum --features "json macros ws"
    cargo add sqlx --features "postgres runtime-tokio macros uuid chrono runtime-tokio-rustls"
    cargo add tokio --features full
    cargo add serde  --features derive
    cargo add chrono
    cargo add serde_json
    cargo add uuid --features "arbitrary atomic borsh bytemuck fast-rng js macro-diagnostics md5 rng rng-getrandom rng-rand serde sha1 slog uuid-rng-internal-lib v1 v3 v4 v5 v6 v7 v8 zerocopy"
    cargo add uuid --features "v4 v7 serde"