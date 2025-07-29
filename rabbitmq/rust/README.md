# RABBITMQ

## library
    cargo add axum --features "json macros ws"
    cargo add tokio --features full
    cargo add serde  --features derive
    cargo add chrono
    cargo add serde_json
    cargo add rabbitmq-stream-client
    cargo add futures

## link
    https://www.rabbitmq.com/tutorials/tutorial-one-rust-stream

## rabbitmq stream
    to activate rabbitmq stream
    rabbitmq-plugins enable rabbitmq_stream: to activate plugin
    rabbitmqctl stop
    rabbitmq-server start
    docker exec rabbitmq rabbitmq-plugins list or rabbitmq-plugins list: to check is plugin active or not