# TIMEOUT

## library
```
go get github.com/labstack/echo/v4
go get github.com/go-playground/validator/v10
go get github.com/google/uuid
go get github.com/jmoiron/sqlx
go get github.com/lib/pq
go get github.com/stretchr/testify
go get github.com/redis/go-redis/v9
```  

## postgres
```
docker run --name note-postgres -e POSTGRES_PASSWORD=12345 -e POSTGRES_DB=note_test -p 5432:5432 -d postgres:8
```

## env
```
export ECHO_HOST=:80
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USERNAME=postgres
export POSTGRES_PASSWORD=12345
export POSTGRES_DATABASE=test1
export POSTGRES_APPLICATION_NAME=test1
export POSTGRES_MAX_OPEN_CONNECTION=10
export POSTGRES_MAX_IDLE_CONNECTION=10
export POSTGRES_CONNECTION_MAX_IDLETIME=10 # in minutes
export POSTGRES_CONNECTION_MAX_LIFETIME=10 # in minutes
export REDIS_HOST=localhost
export REDIS_PORT=6380
export REDIS_DATABASE=0
export ACCESS_TOKEN_EXPIRED=900 # in seconds
export REFRESH_TOKEN_EXPIRED=31536000 # in seconds
```