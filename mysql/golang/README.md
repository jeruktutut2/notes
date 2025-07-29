# MYSQL

## library
    go get github.com/labstack/echo/v4
    go get -u github.com/go-sql-driver/mysql
    go get github.com/jmoiron/sqlx

## mysql
    docker run --name project-mysql -e MYSQL_ROOT_PASSWORD=12345 -e MYSQL_DATABASE=golang_note -p 3308:3306 -d mysql:8.1.0
    mysql -h localhost -u root -p12345
    docker run --name project-mysql -e MYSQL_ROOT_PASSWORD=12345 -p 3309:3306 -d mysql:8.1.0