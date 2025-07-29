# MONGODB

## Docker
    docker run --name project-mongo -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=12345 -p 27017:27017 -d mongo:latest
    docker exec -it project-mongo bash
    mongo -u root -p 12345 --authenticationDatabase admin
    mongosh -u root -p 12345 --authenticationDatabase admin
    show dbs
    use test1
    use admin
    db.getUsers()
    mongodb://root:12345@localhost:27017/test1?authSource=admin

    use test1
    db.createUser({
        user: "root",
        pwd: "12345",
        roles: [{ role: "dbOwner", db: "test1" }]
    })
    mongodb://root:12345@localhost:27017/test1?authSource=test1

    CREATE COLLECTION test1
    db.createCollection("users", {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["_id", "test"],
                properties: {
                    "_id": {
                        bsonType: "string",
                        description: "_id is required and must be a string"
                    },
                    "test": {
                        bsonType: "string",
                        description: "test is required and must be a string"
                    }
                }
            }
        }
    })
    <!-- db.test1.createIndex({ email: 1 }, { unique: true }) -->
    db.test1.findOne({"_id":"id"})
    show collections

## curl test
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1/insert-one
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1/insert-many
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/api/v1/test1/find-one/1
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/api/v1/test1/find
    curl -i -X PUT \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1/update-one
    curl -i -X PUT \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1/update-by-id/7
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1/delete-one/7
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1/delete-many
    
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/67d7e03bd8713e2040fd2107
    curl -i -X PUT \
        -H "Content-Type: application/json" \
        -d '{"id": "67d7e03bd8713e2040fd2107", "test": "test put 67d7e03bd8713e2040fd2107"}' \
        http://localhost:8080
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"id": "67d7e03bd8713e2040fd2107"}' \
        http://localhost:8080

## wrk test
    wrk -t1 -c1 -d60s http://localhost:8080/67d7e357fd886f1ba40fe51d