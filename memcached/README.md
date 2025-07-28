# MEMCACHED

## curl test
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/memcached
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/api/v1/test1/memcached/1
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/memcached
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"message": "test post message"}' \
        http://localhost:8080/memcached
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/memcached/f794b6c3-849d-45b0-b5d5-4df0f2462caf
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"id": "f794b6c3-849d-45b0-b5d5-4df0f2462caf"}' \
        http://localhost:8080/memcached
    curl -i -X POST \
        -H "Content-Type: application/json" \
        http://localhost:8080/memcached/flush

## docker
    docker run --name project-memcached -p 11211:11211 -d memcached
    docker run -d --name memcached-container -p 11211:11211 memcached memcached -m 64 -vv
    -m 64: limiting memory to 64 MB.
    -vv: using verbose logging.

    docker exec -it -u root project-memcached bash
    connect to memcached using telnet 127.0.0.1 11211 or if it doesn't connect, install below tools
    apt-get update && apt-get install -y telnet