# NOTE POSTGRESQL

## library
    go get github.com/labstack/echo/v4
    go get github.com/jmoiron/sqlx
    go get github.com/lib/pq
    go get github.com/stretchr/testify

## docker
    docker pull postgres
    docker pull postgres:13.16
    docker run --name project-postgres -e POSTGRES_PASSWORD=12345 -e POSTGRES_DB=project_users -p 5432:5432 -d postgres:13.16
    docker exdc -it project-postgres bash