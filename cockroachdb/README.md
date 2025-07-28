# COCKROACHDB

## curl test
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test 1"}' \
        http://localhost:8080/test1
    curl -i -X GET \
        -H "Content-Type: application/json" \
        http://localhost:8080/test1/0196444f-fad0-745c-bd77-fc119d414f2a
    curl -i -X GET \
        -H "Content-Type: application/json" \
        http://localhost:8080/test1
    curl -i -X PUT \
        -H "Content-Type: application/json" \
        -d '{"id": "0196444f-fad0-745c-bd77-fc119d414f2a", "test": "test 2 1"}' \
        http://localhost:8080/test1
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"id": "0196444f-fad0-745c-bd77-fc119d414f2a"}' \
        http://localhost:8080/test1