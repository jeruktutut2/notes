package middlewares

import (
	"fmt"

	"github.com/labstack/echo/v4"
)

func EchoExampleMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		fmt.Println(">> Echo Route Middleware")
		return next(c)
	}
}

func EchoGlobalExampleMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		fmt.Println(">> Echo Global Route Middleware")
		return next(c)
	}
}
