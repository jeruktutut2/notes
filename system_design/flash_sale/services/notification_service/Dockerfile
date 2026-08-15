FROM rust:alpine AS builder

RUN apk add --no-cache musl-dev pkgconfig openssl-dev

WORKDIR /app
COPY Cargo.toml ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
COPY src ./src
RUN touch src/main.rs
RUN cargo build --release

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/target/release/notification_service .
EXPOSE 8086
CMD ["./notification_service"]
