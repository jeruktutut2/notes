# TIMEOUT

## library
    go get github.com/gofiber/fiber/v3
    go get github.com/gofiber/fiber/v3@v3.0.0-beta.5

## postgres
    docker exec -it project-postgres bash
    psql -h localhost -d test1 -U postgres -W
    \list \l

    select * from test1 order by id desc limit 10;
    select * from test2 order by id desc limit 10;
    select * from test3 order by id desc limit 10;

## test
    curl -i -X POST \
        -H "Content-Type: application/json" \
        http://localhost:8080/test1-with-tx