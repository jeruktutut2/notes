package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	"distributed-transaction/pkg/config"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/order-service/internal/handler"
	kafkaconsumer "distributed-transaction/services/order-service/internal/kafka"
	"distributed-transaction/services/order-service/internal/repository"
	"distributed-transaction/services/order-service/internal/service"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	_ "github.com/lib/pq"
)

func main() {
	log.Println("🚀 Starting Order Service...")

	// Load config
	cfg := config.Load()

	// Connect to database
	db, err := sql.Open("postgres", cfg.DSN())
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatalf("Failed to ping database: %v", err)
	}
	log.Println("✅ Connected to PostgreSQL")

	// Run migrations
	if err := runMigrations(db); err != nil {
		log.Fatalf("Failed to run migrations: %v", err)
	}
	log.Println("✅ Migrations completed")

	// Initialize layers
	repo := repository.NewOrderRepository(db)
	producer := pkgkafka.NewProducer(cfg.KafkaBrokers)
	svc := service.NewOrderService(repo, producer)

	// Start Kafka consumers
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	kafkaconsumer.StartConsumers(ctx, cfg.KafkaBrokers, svc)
	log.Println("✅ Kafka consumers started")

	// Setup Echo
	e := echo.New()
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	// Health check
	e.GET("/health", func(c *echo.Context) error {
		return c.JSON(200, map[string]string{"status": "ok", "service": "order-service"})
	})

	// Register routes
	orderHandler := handler.NewOrderHandler(svc)
	orderHandler.RegisterRoutes(e)

	// Start server
	port := fmt.Sprintf(":%s", cfg.ServicePort)
	log.Printf("✅ Order Service running on %s", port)
	if err := e.Start(port); err != nil {
		log.Printf("Server stopped: %v", err)
	}
}

func runMigrations(db *sql.DB) error {
	migration := `
	CREATE TABLE IF NOT EXISTS orders (
		id VARCHAR(36) PRIMARY KEY,
		customer_name VARCHAR(255) NOT NULL,
		product_id VARCHAR(36) NOT NULL,
		quantity INT NOT NULL,
		total_price DECIMAL(15,2) NOT NULL,
		status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
		failure_reason TEXT,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
		updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);
	CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
	CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
	`
	_, err := db.Exec(migration)
	return err
}
