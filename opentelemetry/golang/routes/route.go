package routes

import (
	"golang-note-open-telemetry/controllers"
	"golang-note-open-telemetry/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	otelService := services.NewOtelService()
	otelController := controllers.NewOtelController(otelService)
	e.POST("/otel/set-span", otelController.SetSpan)
}

// func SetupMetrics(e *echo.Echo) {
// 	exporter, err := prometheus.New()
// 	if err != nil {
// 		log.Fatalf("failed to initialize prometheus exporter %v", err)
// 	}
// 	meterProvider := metric.NewMeterProvider(metric.WithReader(exporter))
// 	otel.SetMeterProvider(meterProvider)
// 	e.GET("/metrics", echo.WrapHandler())
// }
