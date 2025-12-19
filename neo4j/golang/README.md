# GOLANG NEO4j

## library
    go get github.com/labstack/echo/v4
    go get github.com/neo4j/neo4j-go-driver/v5

## curl
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"name": "name1", "friendName": "friendName1"}' \
        http://localhost:8080/person
    curl -i -X GET \
        -H "Content-Type: application/json" \
        http://localhost:8080/person
    curl -i -X PUT \
        -H "Content-Type: application/json" \
        http://localhost:8080/person
    curl -i -X PUT \
        -H "Content-Type: application/json" \
        http://localhost:8080/person/relationship
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        http://localhost:8080/person/relationship
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        http://localhost:8080/person/node
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        http://localhost:8080/person/node-relationship