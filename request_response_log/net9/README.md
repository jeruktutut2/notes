# REQUEST RESPONSE LOG MIDDLEWARE

## run project
    dotnet run

## change port
    launchSettings.json -> applicationUrl

## curl test
    curl -X GET -H "Content-Type: application/json" http://localhost:8080/test1
    curl -X POST -H "Content-Type: application/json" http://localhost:8080/test1
    curl -X POST http://localhost:8080/test1 -H "Content-Type: application/json" -d '{"username":"xyz","password":"xyz"}'