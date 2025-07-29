# NOTE GOLANG REDIS

## library
    go get github.com/labstack/echo/v4
    go get github.com/redis/go-redis/v9

## env
    export REDIS_HOST=localhost
    export REDIS_PORT=6380
    export REDIS_DATABASE=0

## docker
    docker run --name project-redis -p 6380:6379 -d redis:latest
    docker exec -it project-redis bash
    redis-cli
    redis-cli -n 2 to change database
    SELECT 0
    SELECT 1
    SELECT 2
    SET anotherkey "will expire in a minute" EX 60
    GET key
    FLUSHDB [ASYNC | SYNC]