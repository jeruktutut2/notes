package server

import (
	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"

	otelMw "github.com/example/modular-monolith/internal/shared/middleware"
)

// NewServer creates and configures a new Echo v5 instance with global middleware.
func NewServer() *echo.Echo {
	e := echo.New()

	// Global middleware stack
	e.Use(middleware.Recover())
	e.Use(middleware.RequestID())
	e.Use(middleware.RequestLogger())
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"},
		AllowHeaders: []string{"Accept", "Authorization", "Content-Type", "X-Request-ID"},
	}))

	// OpenTelemetry tracing middleware
	e.Use(otelMw.OtelTracing("modular-monolith"))

	// Health check
	e.GET("/health", healthHandler)

	return e
}

func healthHandler(c *echo.Context) error {
	return c.JSON(200, map[string]string{
		"status": "ok",
	})
}
