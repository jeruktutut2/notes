# REDIS

## curl test
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/api/v1/redis/724b8591-b5ff-4d65-9dc2-4b025747f3e8
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/redis
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/redis
    
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"id": "724b8591-b5ff-4d65-9dc2-4b025747f3e8"}' \                     
        http://localhost:8080/api/v1/redis
    
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/api/v1/test1/c28f0fa8-ec91-4ef5-bfa9-d75eb2768ef4
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"id": "c28f0fa8-ec91-4ef5-bfa9-d75eb2768ef4"}' \
        http://localhost:8080/api/v1/test1

## wrk test
    wrk -t1 -c1 -d60s http://localhost:8080/api/v1/redis/27391356-b280-4f3a-9108-0fcbc32c56e3