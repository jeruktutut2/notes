package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	_ "github.com/lib/pq"
	"github.com/segmentio/kafka-go"
)

type Order struct {
	ID              string    `json:"id"`
	UserID          string    `json:"user_id"`
	FlashSaleID     string    `json:"flash_sale_id"`
	ProductID       string    `json:"product_id"`
	Price           float64   `json:"price"`
	Status          string    `json:"status"`
	IdempotencyKey  string    `json:"idempotency_key"`
	PaymentDeadline time.Time `json:"payment_deadline"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

type OrderMessage struct {
	OrderID        string    `json:"order_id"`
	UserID         string    `json:"user_id"`
	FlashSaleID    string    `json:"flash_sale_id"`
	ProductID      string    `json:"product_id"`
	Price          float64   `json:"price"`
	IdempotencyKey string    `json:"idempotency_key"`
	Timestamp      time.Time `json:"timestamp"`
}

var db *sql.DB

func main() {
	var err error
	dbHost := getEnv("DB_HOST", "pgbouncer")
	dbPort := getEnv("DB_PORT", "6432")
	connStr := fmt.Sprintf("host=%s port=%s user=postgres password=postgres dbname=flash_sale_db sslmode=disable", dbHost, dbPort)

	for i := 0; i < 10; i++ {
		db, err = sql.Open("postgres", connStr)
		if err == nil && db.Ping() == nil {
			break
		}
		time.Sleep(2 * time.Second)
	}

	kafkaBroker := getEnv("KAFKA_BROKER", "kafka:9092")
	go startKafkaConsumer(kafkaBroker)

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP", "service": "order_service"})
	})

	e.GET("/api/v1/orders", listOrders)
	e.GET("/api/v1/orders/:id", getOrderByID)
	e.POST("/api/v1/orders/direct", createOrderDirect)

	port := getEnv("PORT", "8083")
	e.Logger.Fatal(e.Start(":" + port))
}

func getEnv(key, fallback string) string {
	val := os.Getenv(key)
	if val == "" {
		return fallback
	}
	return val
}

func startKafkaConsumer(broker string) {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{broker},
		Topic:    "order-requests",
		GroupID:  "order-service-group",
		MinBytes: 10,
		MaxBytes: 10e6,
	})
	defer reader.Close()

	fmt.Println("Kafka Order Consumer started listening on topic 'order-requests'...")

	for {
		m, err := reader.ReadMessage(context.Background())
		if err != nil {
			time.Sleep(1 * time.Second)
			continue
		}

		var msg OrderMessage
		if err := json.Unmarshal(m.Value, &msg); err != nil {
			fmt.Printf("Error unmarshaling order message: %v\n", err)
			continue
		}

		processOrder(msg)
	}
}

func processOrder(msg OrderMessage) {
	// Idempotency check
	var existingID string
	err := db.QueryRow("SELECT id FROM orders WHERE idempotency_key = $1", msg.IdempotencyKey).Scan(&existingID)
	if err == nil {
		fmt.Printf("Order with idempotency key %s already processed.\n", msg.IdempotencyKey)
		return
	}

	deadline := time.Now().Add(15 * time.Minute)
	_, err = db.Exec(`
		INSERT INTO orders (id, user_id, flash_sale_id, product_id, price, status, idempotency_key, payment_deadline)
		VALUES ($1, $2, $3, $4, $5, 'AWAITING_PAYMENT', $6, $7)
	`, msg.OrderID, msg.UserID, msg.FlashSaleID, msg.ProductID, msg.Price, msg.IdempotencyKey, deadline)

	if err != nil {
		fmt.Printf("Failed to insert order into DB: %v\n", err)
	} else {
		fmt.Printf("Successfully created order %s for user %s\n", msg.OrderID, msg.UserID)
	}
}

func createOrderDirect(c echo.Context) error {
	var msg OrderMessage
	if err := c.Bind(&msg); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid payload"})
	}

	processOrder(msg)
	return c.JSON(http.StatusCreated, map[string]string{"status": "CREATED", "order_id": msg.OrderID})
}

func listOrders(c echo.Context) error {
	userID := c.QueryParam("user_id")
	var rows *sql.Rows
	var err error

	if userID != "" {
		rows, err = db.Query("SELECT id, user_id, flash_sale_id, product_id, price, status, idempotency_key, payment_deadline, created_at, updated_at FROM orders WHERE user_id = $1 ORDER BY created_at DESC", userID)
	} else {
		rows, err = db.Query("SELECT id, user_id, flash_sale_id, product_id, price, status, idempotency_key, payment_deadline, created_at, updated_at FROM orders ORDER BY created_at DESC")
	}

	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	defer rows.Close()

	orders := []Order{}
	for rows.Next() {
		var o Order
		if err := rows.Scan(&o.ID, &o.UserID, &o.FlashSaleID, &o.ProductID, &o.Price, &o.Status, &o.IdempotencyKey, &o.PaymentDeadline, &o.CreatedAt, &o.UpdatedAt); err != nil {
			continue
		}
		orders = append(orders, o)
	}
	return c.JSON(http.StatusOK, orders)
}

func getOrderByID(c echo.Context) error {
	id := c.Param("id")
	var o Order
	err := db.QueryRow("SELECT id, user_id, flash_sale_id, product_id, price, status, idempotency_key, payment_deadline, created_at, updated_at FROM orders WHERE id = $1", id).
		Scan(&o.ID, &o.UserID, &o.FlashSaleID, &o.ProductID, &o.Price, &o.Status, &o.IdempotencyKey, &o.PaymentDeadline, &o.CreatedAt, &o.UpdatedAt)
	if err != nil {
		if err == sql.ErrNoRows {
			return c.JSON(http.StatusNotFound, map[string]string{"error": "Order not found"})
		}
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, o)
}
