# TIMEOUT

## library
    go get github.com/gofiber/fiber/v2
    go get github.com/jmoiron/sqlx
    go get github.com/lib/pq

## explanation why fiber cannot get the http close connection
    https://github.com/gofiber/fiber/issues/805
    The problem is that *fiber.Ctx is returned to the sync.Pool when you return from the handler. So c.Context().Done() becomes non-existent. It is better to handle the request in a separate thread while waiting for the context to be done.

## curl test
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/timeout/with-tx
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/timeout/without-tx
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/timeout/context-done