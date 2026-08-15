package main

import (
	"fmt"
	"net/http"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
)

func main() {
	fmt.Println("Hello World")
	e := echo.New()
	e.Use(middleware.RequestLogger())

	e.GET("/", func(c *echo.Context) error {
		return c.String(http.StatusOK, "Hello, World!")
	})
	e.GET("/resource", func(c *echo.Context) error {
		// return c.String(http.StatusOK, "Resource")
		cookie, err := c.Cookie("appone")
		if err != nil {
			return c.Redirect(http.StatusFound, "http:/localhost:8080/oauth/authorize")
		}
		if cookie.Value == "" {
			return c.Redirect(http.StatusFound, "http:/localhost:8080/oauth/authorize")
		}

		return c.JSON(http.StatusOK, map[string]string{
			"message": "Resource",
			"cookie":  cookie.String(),
		})
	})

	if err := e.Start(":1323"); err != nil {
		e.Logger.Error("failed to start server", "error", err)
	}
}
