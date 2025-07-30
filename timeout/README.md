# TIMEOUT

## curl test
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/timeout/without-tx
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/timeout/with-tx
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/timeout/change-timeout