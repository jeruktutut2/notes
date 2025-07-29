package main

import (
	"context"
	"golang-note-open-telemetry/routes"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"go.opentelemetry.io/contrib/instrumentation/github.com/labstack/echo/otelecho"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
	"go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
)

func main() {
	// 1. Setup tracer
	tp, err := setupTracerProvider()
	if err != nil {
		log.Fatalf("failed to setup trace provider: %v", err)
	}
	defer func() {
		_ = tp.Shutdown(context.Background())
	}()

	// 2. Setup Echo
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// 3. OTEL middleware
	e.Use(otelecho.Middleware("echo-server"))
	routes.SetRoute(e)

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	go func() {
		if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed {
			e.Logger.Fatal("shutting down the server")
		}
	}()
	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
}

func setupTracerProvider() (*sdktrace.TracerProvider, error) {
	// 1. Jaeger exporter
	// exp, err := jaeger.New(jaeger.WithCollectorEndpoint(jaeger.WithEndpoint("http://localhost:14268/api/traces")))
	// if err != nil {
	// 	return nil, err
	// }

	// Setup stdout exporter untuk pretty print di terminal
	stdoutExp, err := stdouttrace.New(stdouttrace.WithPrettyPrint())
	if err != nil {
		log.Fatalf("failed to create stdout exporter: %v", err)
	}

	// Setup OTLP exporter untuk mengirim trace ke kolektor atau sistem lain
	otlptraceExp, err := otlptracehttp.New(context.Background(),
		otlptracehttp.WithEndpoint("localhost:4318"), // Misalnya OTLP HTTP
		otlptracehttp.WithInsecure(),                 // Sesuaikan jika perlu
	)

	// 2. Resource
	res, err := resource.New(context.Background(),
		resource.WithAttributes(
			semconv.ServiceName("echo-service"),
		),
	)
	if err != nil {
		return nil, err
	}

	// 3. Tracer provider
	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(stdoutExp),
		sdktrace.WithBatcher(otlptraceExp),
		sdktrace.WithResource(res),
	)

	otel.SetTracerProvider(tp)
	return tp, nil
}
