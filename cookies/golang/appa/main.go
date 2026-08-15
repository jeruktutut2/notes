package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func main() {
	// fmt.Println("Hello World")
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, World! appa")
	})
	e.Logger.Fatal(e.Start("appa.local:8081"))
}
