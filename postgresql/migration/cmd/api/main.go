package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"

	"github.com/bsa/migration/internal/config"
	"github.com/bsa/migration/internal/database"
	"github.com/bsa/migration/internal/handler"
	"github.com/bsa/migration/internal/repository"
	"github.com/bsa/migration/migrations"
)

func main() {
	// Setup structured logging
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	})))

	slog.Info("=== Memulai Migration Demo API ===")

	// Load konfigurasi
	cfg := config.NewConfig()
	slog.Info("Konfigurasi dimuat",
		"server_port", cfg.ServerPort,
		"db_host", cfg.DBHost,
		"db_port", cfg.DBPort,
		"db_name", cfg.DBName,
		"migrate_host", cfg.MigrateDBHost,
		"migrate_port", cfg.MigrateDBPort,
	)

	// Koneksi ke database (via PgBouncer)
	db, err := database.New(cfg)
	if err != nil {
		slog.Error("Gagal koneksi database", "error", err)
		os.Exit(1)
	}
	defer db.Close()

	// Jalankan auto-migration saat startup
	// Migration langsung ke PostgreSQL (bypass PgBouncer)
	slog.Info("Menjalankan database migration...")
	if err := db.RunMigrations(migrations.FS); err != nil {
		slog.Error("Gagal menjalankan migration", "error", err)
		os.Exit(1)
	}

	// Cek versi migration saat ini
	version, dirty, err := db.GetMigrationVersion(migrations.FS)
	if err != nil {
		slog.Warn("Gagal membaca versi migration", "error", err)
	} else {
		slog.Info("Versi migration saat ini", "version", version, "dirty", dirty)
	}

	// Setup Echo v5
	e := echo.New()

	// Middleware
	e.Use(middleware.RequestLogger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	// Health check endpoint
	e.GET("/health", func(c *echo.Context) error {
		return c.JSON(http.StatusOK, map[string]interface{}{
			"status":    "ok",
			"timestamp": time.Now().Format(time.RFC3339),
			"database":  "connected",
		})
	})

	// Info endpoint
	e.GET("/", func(c *echo.Context) error {
		return c.JSON(http.StatusOK, map[string]interface{}{
			"app":     "Migration Demo API",
			"version": "1.0.0",
			"stack":   "Go Echo v5 + PgBouncer + PostgreSQL",
			"routes": map[string]string{
				"GET /health":           "Health check",
				"GET /api/users":        "List semua users",
				"GET /api/users/:id":    "Detail user by ID",
				"POST /api/users":       "Buat user baru",
				"PUT /api/users/:id":    "Update user",
				"DELETE /api/users/:id": "Hapus user",
			},
		})
	})

	// Setup repositories dan handlers
	userRepo := repository.NewUserRepository(db.Pool)
	userHandler := handler.NewUserHandler(userRepo)
	userHandler.RegisterRoutes(e)

	// Graceful shutdown menggunakan signal.NotifyContext (Echo v5 pattern)
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	// Konfigurasi server
	sc := echo.StartConfig{
		Address:         ":" + cfg.ServerPort,
		GracefulTimeout: 10 * time.Second,
	}

	slog.Info("Server berjalan", "address", sc.Address)

	// Start server - akan berhenti gracefully saat context cancelled
	if err := sc.Start(ctx, e); err != nil && err != http.ErrServerClosed {
		slog.Error("Server error", "error", err)
		os.Exit(1)
	}

	slog.Info("Server berhasil dihentikan")
}
