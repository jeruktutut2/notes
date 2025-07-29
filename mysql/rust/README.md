# MYSQL

## library
    cargo add axum
    cargo add tokio
    cargo add serde --features=derive
    cargo add serde_json
    cargo add chrono
    cargo add sqlx

## env
    export AXUM_HOST=0.0.0.0:8080
    export MYSQL_HOST=localhost
    export MYSQL_USERNAME=root
    export MYSQL_PASSWORD=12345
    export MYSQL_PORT=3309
    export MYSQL_DATABASE=project_test
    export MYSQL_IDLE_TIMEOUT=30
    export MYSQL_MAX_CONNECTION=10
    export MYSQL_MAX_LIFETIME=300
    export MYSQL_MIN_CONNECTION=1

## docker
    docker exec -it project-mysql bash
    mysql -h localhost -u root -p12345
    CREATE DATABASE project_test;

## create table test1
    CREATE TABLE test1 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        test VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

## curl
    curl http://localhost:8080/

    curl -X POST "http://localhost:8080/" \
     -H "Content-Type: application/json" \
     -d '{"name": "name", "address": "address"}'