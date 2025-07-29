# PDF
Generate pdf from many small pdf, merge it and make it one pdf

## library
    go get github.com/labstack/echo/v4
    go get github.com/jung-kurt/gofpdf
    go get github.com/pdfcpu/pdfcpu/pkg/api

## curl test
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/file/show-pdf
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/file/download-pdf
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/file/stream-pdf