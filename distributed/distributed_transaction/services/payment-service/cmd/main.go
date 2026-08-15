package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	"distributed-transaction/pkg/config"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/payment-service/internal/handler"
	kafkaconsumer "distributed-transaction/services/payment-service/internal/kafka"
	"distributed-transaction/services/payment-service/internal/repository"
	"distributed-transaction/services/payment-service/internal/service"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	_ "github.com/lib/pq"
)

func main() {
	log.Println("🚀 Starting Payment Service...")

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

	repo := repository.NewPaymentRepository(db)
	producer := pkgkafka.NewProducer(cfg.KafkaBrokers)
	svc := service.NewPaymentService(repo, producer)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	kafkaconsumer.StartConsumers(ctx, cfg.KafkaBrokers, svc)
	log.Println("✅ Kafka consumers started")

	e := echo.New()
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	e.GET("/health", func(c *echo.Context) error {
		return c.JSON(200, map[string]string{"status": "ok", "service": "payment-service"})
	})

	paymentHandler := handler.NewPaymentHandler(svc)
	paymentHandler.RegisterRoutes(e)

	port := fmt.Sprintf(":%s", cfg.ServicePort)
	log.Printf("✅ Payment Service running on %s", port)
	if err := e.Start(port); err != nil {
		log.Printf("Server stopped: %v", err)
	}
}

func runMigrations(db *sql.DB) error {
	migration := `
	CREATE TABLE IF NOT EXISTS payments (
		id VARCHAR(36) PRIMARY KEY,
		order_id VARCHAR(36) NOT NULL,
		amount DECIMAL(15,2) NOT NULL,
		status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
		failure_reason TEXT,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
		updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);
	CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);
	CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
	`
	_, err := db.Exec(migration)
	return err
}
