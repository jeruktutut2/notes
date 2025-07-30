# VALIDATOR

## library
    go get github.com/labstack/echo/v4
    go get github.com/go-playground/validator/v10

## curl
    curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"email": "", "username":"","password":""}' \
    http://localhost:8080/test

    curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"email": "a", "username":"a","password":"a"}' \
    http://localhost:8080/test