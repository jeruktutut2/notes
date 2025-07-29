# SERVER SENT EVENT

## curl test
    curl -i -N -X GET http://localhost:8080/sse
    curl -i -N -X POST http://localhost:8080/sse/message1

    curl -i -N -X GET http://localhost:8080/sse-manual
    curl -i -N -X POST http://localhost:8080/sse-manual/message-manual1