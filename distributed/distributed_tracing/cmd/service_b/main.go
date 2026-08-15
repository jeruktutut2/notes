package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"distributed_tracing/internal/tracing"

	"github.com/labstack/echo/v4"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
)

func main() {
	// Inisialisasi Tracer untuk Service B
	tp, err := tracing.InitTracer("service_b", "localhost:4318")
	if err != nil {
		log.Fatalf("Gagal inisialisasi tracer: %v", err)
	}
	defer func() {
		if err := tp.Shutdown(context.Background()); err != nil {
			log.Printf("Error shutdown tracer: %v", err)
		}
	}()

	e := echo.New()
	tracer := otel.Tracer("service_b_tracer")

	e.Use(func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			// *** KUNCI PENTING ***
			// Mengekstrak TraceID dari HTTP Header yang dikirim oleh Service A
			// agar jejaknya nyambung menjadi satu Trace utuh.
			ctx := otel.GetTextMapPropagator().Extract(
				c.Request().Context(),
				propagation.HeaderCarrier(c.Request().Header),
			)
			
			// Lanjutkan trace menggunakan context yang sudah disuntik TraceID sebelumnya
			ctx, span := tracer.Start(ctx, c.Request().URL.Path)
			defer span.End()

			c.SetRequest(c.Request().WithContext(ctx))
			return next(c)
		}
	})

	e.GET("/proses", func(c echo.Context) error {
		ctx := c.Request().Context()

		_, spanB1 := tracer.Start(ctx, "Query_Database_B")
		time.Sleep(200 * time.Millisecond) // pura-pura query ke database B
		spanB1.End()

		return c.JSON(http.StatusOK, map[string]string{
			"status": "Service B selesai memproses!",
		})
	})

	fmt.Println("🚀 Service B berjalan di port 8082")
	e.Start(":8082")
}
