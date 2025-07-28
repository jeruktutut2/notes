# COCKROACHDB

## library
    go get github.com/labstack/echo/v4
    go get github.com/jackc/pgx/v5
    go get github.com/jackc/pgx
    go get github.com/google/uuid
    github.com/jackc/pgx/v5/pgxpool need this by go mod tidy after downloading go get github.com/jackc/pgx or go get github.com/jackc/pgx/v5

## docker
    docker-compose up -d
    init first: docker exec -it cockroach1 ./cockroach init --insecure
    if you use non oss (enterprise version), you will get a warning: This cluster will require a license key by April 19th, 2025 or the cluster will be throttled.