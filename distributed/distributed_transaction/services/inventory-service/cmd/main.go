package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	"distributed-transaction/pkg/config"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/inventory-service/internal/handler"
	kafkaconsumer "distributed-transaction/services/inventory-service/internal/kafka"
	"distributed-transaction/services/inventory-service/internal/repository"
	"distributed-transaction/services/inventory-service/internal/service"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	_ "github.com/lib/pq"
)

func main() {
	log.Println("🚀 Starting Inventory Service...")

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

	repo := repository.NewInventoryRepository(db)
	producer := pkgkafka.NewProducer(cfg.KafkaBrokers)
	svc := service.NewInventoryService(repo, producer)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	kafkaconsumer.StartConsumers(ctx, cfg.KafkaBrokers, svc)
	log.Println("✅ Kafka consumers started")

	e := echo.New()
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	e.GET("/health", func(c *echo.Context) error {
		return c.JSON(200, map[string]string{"status": "ok", "service": "inventory-service"})
	})

	inventoryHandler := handler.NewInventoryHandler(svc)
	inventoryHandler.RegisterRoutes(e)

	port := fmt.Sprintf(":%s", cfg.ServicePort)
	log.Printf("✅ Inventory Service running on %s", port)
	if err := e.Start(port); err != nil {
		log.Printf("Server stopped: %v", err)
	}
}

func runMigrations(db *sql.DB) error {
	migration := `
	CREATE TABLE IF NOT EXISTS products (
		id VARCHAR(36) PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		stock INT NOT NULL DEFAULT 0,
		reserved_stock INT NOT NULL DEFAULT 0,
		price DECIMAL(15,2) NOT NULL DEFAULT 0,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
		updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);

	CREATE TABLE IF NOT EXISTS inventory_logs (
		id VARCHAR(36) PRIMARY KEY,
		order_id VARCHAR(36) NOT NULL,
		product_id VARCHAR(36) NOT NULL,
		quantity INT NOT NULL,
		action VARCHAR(50) NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);

	CREATE INDEX IF NOT EXISTS idx_inventory_logs_order_id ON inventory_logs(order_id);
	CREATE INDEX IF NOT EXISTS idx_inventory_logs_product_id ON inventory_logs(product_id);

	-- Seed data (only if empty)
	INSERT INTO products (id, name, stock, reserved_stock, price)
	SELECT 'prod-001', 'Laptop Gaming', 50, 0, 15000000
	WHERE NOT EXISTS (SELECT 1 FROM products WHERE id = 'prod-001');

	INSERT INTO products (id, name, stock, reserved_stock, price)
	SELECT 'prod-002', 'Mechanical Keyboard', 100, 0, 1500000
	WHERE NOT EXISTS (SELECT 1 FROM products WHERE id = 'prod-002');

	INSERT INTO products (id, name, stock, reserved_stock, price)
	SELECT 'prod-003', 'Gaming Mouse', 200, 0, 750000
	WHERE NOT EXISTS (SELECT 1 FROM products WHERE id = 'prod-003');

	INSERT INTO products (id, name, stock, reserved_stock, price)
	SELECT 'prod-004', 'Monitor 4K', 30, 0, 5000000
	WHERE NOT EXISTS (SELECT 1 FROM products WHERE id = 'prod-004');

	INSERT INTO products (id, name, stock, reserved_stock, price)
	SELECT 'prod-005', 'Headset Wireless', 75, 0, 2000000
	WHERE NOT EXISTS (SELECT 1 FROM products WHERE id = 'prod-005');
	`
	_, err := db.Exec(migration)
	return err
}
