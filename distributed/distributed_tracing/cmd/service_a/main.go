package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"

	"distributed_tracing/internal/tracing"

	"github.com/labstack/echo/v4"
	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
)

func main() {
	// Inisialisasi Tracer
	tp, err := tracing.InitTracer("service_a", "localhost:4318")
	if err != nil {
		log.Fatalf("Gagal inisialisasi tracer: %v", err)
	}
	defer func() {
		if err := tp.Shutdown(context.Background()); err != nil {
			log.Printf("Error shutdown tracer: %v", err)
		}
	}()

	e := echo.New()
	tracer := otel.Tracer("service_a_tracer")

	// Middleware Echo sederhana untuk Tracer
	e.Use(func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			ctx := c.Request().Context()
			// Mulai rentang waktu (Span) untuk HTTP Request ini
			ctx, span := tracer.Start(ctx, c.Request().URL.Path)
			defer span.End()

			// Set atribut/tag pada span
			span.SetAttributes(attribute.String("http.method", c.Request().Method))
			
			// Pasang ctx baru ke request
			c.SetRequest(c.Request().WithContext(ctx))
			return next(c)
		}
	})

	e.GET("/pesan", func(c echo.Context) error {
		ctx := c.Request().Context()

		// --- BAGIAN 1: Proses internal Service A ---
		ctx, spanA := tracer.Start(ctx, "ProsesInternal_A")
		time.Sleep(100 * time.Millisecond) // Simulasi kerja lambat
		spanA.End()

		// --- BAGIAN 2: Memanggil Service B ---
		_, spanB := tracer.Start(ctx, "Panggil_Service_B")
		defer spanB.End()

		// Gunakan otelhttp.NewTransport agar TraceID otomatis disuntikkan ke HTTP Header
		client := http.Client{Transport: otelhttp.NewTransport(http.DefaultTransport)}
		
		req, _ := http.NewRequestWithContext(ctx, "GET", "http://localhost:8082/proses", nil)
		resp, err := client.Do(req)
		if err != nil {
			spanB.RecordError(err)
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Gagal panggil Service B"})
		}
		defer resp.Body.Close()

		bodyBytes, _ := io.ReadAll(resp.Body)
		
		// Berhasil memanggil Service B
		return c.JSON(http.StatusOK, map[string]string{
			"message":  "Berhasil menyelesaikan siklus request",
			"response_b": string(bodyBytes),
		})
	})

	fmt.Println("🚀 Service A berjalan di port 8081")
	e.Start(":8081")
}
