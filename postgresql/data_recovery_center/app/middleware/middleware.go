package middleware

import (
	"log"
	"time"

	"github.com/labstack/echo/v5"
)

func Logger() echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			start := time.Now()

			err := next(c)

			req := c.Request()
			res := c.Response()

			log.Printf("[HTTP] %s %s %d %v",
				req.Method,
				req.RequestURI,
				res.Status,
				time.Since(start),
			)

			return err
		}
	}
}
