package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	"distributed-transaction/pkg/config"
	"distributed-transaction/services/notification-service/internal/handler"
	kafkaconsumer "distributed-transaction/services/notification-service/internal/kafka"
	"distributed-transaction/services/notification-service/internal/repository"
	"distributed-transaction/services/notification-service/internal/service"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	_ "github.com/lib/pq"
)

func main() {
	log.Println("🚀 Starting Notification Service...")

	cfg := config.Load()

	db, err := sql.Open("postgres", cfg.DSN())
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatalf("Failed to ping database: %v", err)
	}
	log.Println("✅ Connected to PostgreSQL")

	if err := runMigrations(db); err != nil {
		log.Fatalf("Failed to run migrations: %v", err)
	}
	log.Println("✅ Migrations completed")

	repo := repository.NewNotificationRepository(db)
	svc := service.NewNotificationService(repo)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	kafkaconsumer.StartConsumers(ctx, cfg.KafkaBrokers, svc)
	log.Println("✅ Kafka consumers started")

	e := echo.New()
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	e.GET("/health", func(c *echo.Context) error {
		return c.JSON(200, map[string]string{"status": "ok", "service": "notification-service"})
	})

	notifHandler := handler.NewNotificationHandler(svc)
	notifHandler.RegisterRoutes(e)

	port := fmt.Sprintf(":%s", cfg.ServicePort)
	log.Printf("✅ Notification Service running on %s", port)
	if err := e.Start(port); err != nil {
		log.Printf("Server stopped: %v", err)
	}
}

func runMigrations(db *sql.DB) error {
	migration := `
	CREATE TABLE IF NOT EXISTS notifications (
		id VARCHAR(36) PRIMARY KEY,
		order_id VARCHAR(36) NOT NULL,
		type VARCHAR(50) NOT NULL,
		message TEXT NOT NULL,
		status VARCHAR(50) NOT NULL DEFAULT 'SENT',
		created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);
	CREATE INDEX IF NOT EXISTS idx_notifications_order_id ON notifications(order_id);
	CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(type);
	`
	_, err := db.Exec(migration)
	return err
}
