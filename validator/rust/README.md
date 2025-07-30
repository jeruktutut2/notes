# VALIDATOR

## library
    cargo add axum --features "json macros ws"
    cargo add tokio --features full
    cargo add serde  --features derive
    cargo add chrono
    cargo add serde_json
    cargo add validator --features derive
    cargo add regex

## curl test
    curl -i -X POST \
    -H "Content-Type: application/json" \
    -d '{"email": "", "username": "", "phone_number": "", "password": ""}' \
    http://localhost:8080