# TWO WEB SERVER

## library
    go get github.com/labstack/echo/v4
    go get github.com/julienschmidt/httprouter

## curl test
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/httprouter/landing-page
    curl -i -X POST -H "Content-Type: application/json" http://localhost:8080/httprouter/landing-page
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/echo/landing-page
    curl -i -X POST -H "Content-Type: application/json" http://localhost:8080/echo/landing-page