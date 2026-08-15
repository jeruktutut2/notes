package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"time"

	"github.com/example/modular-monolith/internal/config"
	"github.com/example/modular-monolith/internal/modules/inventory"
	"github.com/example/modular-monolith/internal/modules/notification"
	"github.com/example/modular-monolith/internal/modules/order"
	"github.com/example/modular-monolith/internal/modules/product"
	"github.com/example/modular-monolith/internal/modules/user"
	"github.com/example/modular-monolith/internal/platform/database"
	"github.com/example/modular-monolith/internal/platform/server"
	"github.com/example/modular-monolith/internal/platform/telemetry"
)

func main() {
	// Setup structured logging.
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	})))

	// Load configuration.
	cfg := config.Load()
	slog.Info("configuration loaded", "config", cfg.String())

	ctx := context.Background()

	// Initialize OpenTelemetry tracing.
	shutdownTracer, err := telemetry.InitTracer(ctx, cfg.OtelEndpoint, cfg.ServiceName)
	if err != nil {
		slog.Warn("failed to initialize tracer, continuing without tracing", "error", err)
	} else {
		defer func() {
			shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			defer cancel()
			if err := shutdownTracer(shutdownCtx); err != nil {
				slog.Error("failed to shutdown tracer", "error", err)
			}
		}()
	}

	// Initialize database connection pool.
	pool, err := database.NewPool(ctx, cfg.DatabaseURL)
	if err != nil {
		slog.Error("failed to connect to database", "error", err)
		os.Exit(1)
	}
	defer pool.Close()

	// Create Echo server.
	e := server.NewServer()

	// Register modules under /api/v1
	api := e.Group("/api/v1")

	user.RegisterRoutes(api.Group("/users"), pool)
	product.RegisterRoutes(api.Group("/products"), pool)
	order.RegisterRoutes(api.Group("/orders"), pool)
	inventory.RegisterRoutes(api.Group("/inventory"), pool)
	notification.RegisterRoutes(api.Group("/notifications"), pool)

	slog.Info("all modules registered",
		"modules", []string{"user", "product", "order", "inventory", "notification"},
	)

	// Start server — Echo v5's Start() handles graceful shutdown via signal.NotifyContext internally.
	addr := fmt.Sprintf(":%s", cfg.ServerPort)
	slog.Info("starting server", "address", addr)
	if err := e.Start(addr); err != nil {
		slog.Error("server error", "error", err)
		os.Exit(1)
	}
}
