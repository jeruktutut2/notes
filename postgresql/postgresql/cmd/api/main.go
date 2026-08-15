package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"echo-otel-demo/internal/config"
	"echo-otel-demo/internal/database"
	"echo-otel-demo/internal/handler"
	"echo-otel-demo/internal/repository"
	"echo-otel-demo/internal/telemetry"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	echootel "github.com/labstack/echo-opentelemetry"
)

func main() {
	// ── Load Config ─────────────────────────────────────────────
	cfg := config.Load()

	// ── Init OpenTelemetry ──────────────────────────────────────
	tp, err := telemetry.InitTracer(cfg.OtelServiceName, cfg.OtelEndpoint)
	if err != nil {
		log.Fatalf("failed to init tracer: %v", err)
	}
	defer func() {
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		if err := tp.Shutdown(ctx); err != nil {
			log.Printf("error shutting down tracer: %v", err)
		}
	}()

	// ── Init Database (via PgBouncer) ───────────────────────────
	db := database.NewPostgresql(cfg)
	defer db.Close()

	// ── Init Repository & Handler ───────────────────────────────
	userRepo := repository.NewUserRepository(db.GetPool())
	userHandler := handler.NewUserHandler(userRepo)

	// ── Echo Setup ──────────────────────────────────────────────
	e := echo.New()

	// Middleware
	e.Use(middleware.Recover())
	e.Use(middleware.RequestLogger())
	e.Use(middleware.RequestID())
	e.Use(middleware.CORS())
	e.Use(echootel.NewMiddleware(cfg.OtelServiceName))

	// ── Routes ──────────────────────────────────────────────────
	e.GET("/health", func(c *echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{
			"status":  "ok",
			"service": cfg.OtelServiceName,
			"time":    time.Now().Format(time.RFC3339),
		})
	})

	api := e.Group("/api/v1")
	api.GET("/users", userHandler.GetAllUsers)
	api.GET("/users/:id", userHandler.GetUserByID)
	api.POST("/users", userHandler.CreateUser)
	api.PUT("/users/:id", userHandler.UpdateUser)
	api.DELETE("/users/:id", userHandler.DeleteUser)

	// ── Graceful Shutdown ───────────────────────────────────────
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	sc := echo.StartConfig{
		Address:         fmt.Sprintf(":%s", cfg.AppPort),
		GracefulTimeout: 10 * time.Second,
	}

	log.Printf("🚀 Server starting on %s", sc.Address)
	if err := sc.Start(ctx, e); err != nil {
		log.Fatalf("server error: %v", err)
	}

	log.Println("✅ Server exited gracefully")
}
