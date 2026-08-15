package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
	"github.com/segmentio/kafka-go"

	"saga_pattern/common/db"
)

// Event Structures
type OrderCreatedEvent struct {
	OrderID     string  `json:"order_id"`
	ItemID      string  `json:"item_id"`
	Quantity    int     `json:"quantity"`
	Amount      float64 `json:"amount"`
	FailPayment bool    `json:"fail_payment"`
}

type InventoryReservedEvent struct {
	OrderID     string  `json:"order_id"`
	ItemID      string  `json:"item_id"`
	Quantity    int     `json:"quantity"`
	Amount      float64 `json:"amount"`
	FailPayment bool    `json:"fail_payment"`
}

type InventoryFailedEvent struct {
	OrderID string `json:"order_id"`
	Reason  string `json:"reason"`
}

type PaymentSuccessEvent struct {
	OrderID string `json:"order_id"`
}

type PaymentFailedEvent struct {
	OrderID  string `json:"order_id"`
	ItemID   string `json:"item_id"`
	Quantity int    `json:"quantity"`
	Reason   string `json:"reason"`
}

// Request Payload
type CreateOrderRequest struct {
	ItemID      string  `json:"item_id"`
	Quantity    int     `json:"quantity"`
	Amount      float64 `json:"amount"`
	FailPayment bool    `json:"fail_payment"`
}

var (
	kafkaBroker string
	database    *db.DB
	kafkaWriter *kafka.Writer
)

func main() {
	kafkaBroker = getEnv("KAFKA_BROKER", "kafka:9092")

	// Connect to Database
	var err error
	database, err = db.ConnectDB()
	if err != nil {
		log.Fatalf("Database connection failed: %v", err)
	}

	initKafkaWriter()
	defer kafkaWriter.Close()

	// Ensure Kafka topics are created
	initKafkaTopics()


	// Start Background Kafka Consumers (Choreography participants)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	go startInventoryConsumer(ctx)
	go startPaymentConsumer(ctx)
	go startOrderStateConsumer(ctx)

	// Echo v5 Web Server
	e := echo.New()

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP", "saga": "Kafka Choreography"})
	})

	e.POST("/kafka/orders", handleCreateKafkaOrder)
	e.GET("/orders/:id", handleGetOrder)
	e.GET("/inventory", handleGetInventory)

	port := getEnv("PORT", "8081")
	go func() {
		if err := e.Start(":" + port); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Echo server shut down: %v", err)
		}
	}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down Kafka Choreography Saga Service...")
}

func getEnv(key, fallback string) string {
	if val, ok := os.LookupEnv(key); ok {
		return val
	}
	return fallback
}

func initKafkaWriter() {
	kafkaWriter = &kafka.Writer{
		Addr:                   kafka.TCP(kafkaBroker),
		Balancer:               &kafka.LeastBytes{},
		AllowAutoTopicCreation: true,
	}
}

func initKafkaTopics() {
	topics := []string{
		"saga.order.created",
		"saga.inventory.reserved",
		"saga.inventory.failed",
		"saga.payment.success",
		"saga.payment.failed",
	}

	for _, topic := range topics {
		w := &kafka.Writer{
			Addr:                   kafka.TCP(kafkaBroker),
			Topic:                  topic,
			AllowAutoTopicCreation: true,
		}
		err := w.WriteMessages(context.Background(), kafka.Message{
			Key:   []byte("INIT"),
			Value: []byte("INIT"),
		})
		if err != nil {
			log.Printf("[InitKafkaTopics Error for %s]: %v\n", topic, err)
		} else {
			log.Printf("[InitKafkaTopics Success for %s]\n", topic)
		}
		w.Close()
	}

	log.Println("Kafka topics initialized and created successfully!")
}



// HTTP Handlers
func handleCreateKafkaOrder(c echo.Context) error {
	var req CreateOrderRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request body"})
	}

	if req.ItemID == "" || req.Quantity <= 0 {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid item_id or quantity"})
	}

	orderID := "ORD-KAFKA-" + uuid.New().String()[:8]

	// Step 1: Create local order state in PENDING
	err := database.CreateOrder(orderID, req.ItemID, req.Quantity, req.Amount, "KAFKA_CHOREOGRAPHY")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Failed to create order in DB"})
	}
	_ = database.LogSagaStep(orderID, "OrderService", "CreateOrder", "PENDING", "Order created in database")

	// Step 2: Publish OrderCreated Event to Kafka
	event := OrderCreatedEvent{
		OrderID:     orderID,
		ItemID:      req.ItemID,
		Quantity:    req.Quantity,
		Amount:      req.Amount,
		FailPayment: req.FailPayment,
	}

	payload, _ := json.Marshal(event)
	err = publishKafkaMessage("saga.order.created", orderID, payload)
	if err != nil {
		log.Printf("Failed to publish kafka message: %v\n", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": fmt.Sprintf("Failed to publish Kafka event: %v", err)})
	}
	log.Printf("Successfully published saga.order.created for %s\n", orderID)

	return c.JSON(http.StatusAccepted, map[string]interface{}{
		"message":  "Order processing started (Kafka Choreography)",
		"order_id": orderID,
		"status":   "PENDING",
	})
}


func handleGetOrder(c echo.Context) error {
	id := c.Param("id")
	var orderID, itemID, status, sagaType string
	var qty int
	var amount float64

	err := database.QueryRow(`SELECT id, item_id, quantity, total_amount, status, saga_type FROM orders WHERE id = $1`, id).
		Scan(&orderID, &itemID, &qty, &amount, &status, &sagaType)
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "Order not found"})
	}

	// Fetch saga execution logs
	rows, err := database.Query(`SELECT service_name, step_name, status, details, created_at FROM saga_logs WHERE order_id = $1 ORDER BY id ASC`, id)
	var logs []map[string]interface{}
	if err == nil {
		defer rows.Close()
		for rows.Next() {
			var svc, step, stat, details string
			var createdAt time.Time
			rows.Scan(&svc, &step, &stat, &details, &createdAt)
			logs = append(logs, map[string]interface{}{
				"service":    svc,
				"step":       step,
				"status":     stat,
				"details":    details,
				"created_at": createdAt,
			})
		}
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"order_id":     orderID,
		"item_id":      itemID,
		"quantity":     qty,
		"total_amount": amount,
		"status":       status,
		"saga_type":    sagaType,
		"saga_logs":    logs,
	})
}

func handleGetInventory(c echo.Context) error {
	rows, err := database.Query(`SELECT item_id, item_name, stock, updated_at FROM inventory`)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Failed to fetch inventory"})
	}
	defer rows.Close()

	var items []map[string]interface{}
	for rows.Next() {
		var itemID, itemName string
		var stock int
		var updatedAt time.Time
		rows.Scan(&itemID, &itemName, &stock, &updatedAt)
		items = append(items, map[string]interface{}{
			"item_id":    itemID,
			"item_name":  itemName,
			"stock":      stock,
			"updated_at": updatedAt,
		})
	}
	return c.JSON(http.StatusOK, items)
}

// Kafka Helper
func publishKafkaMessage(topic, key string, value []byte) error {
	w := &kafka.Writer{
		Addr:                   kafka.TCP(kafkaBroker),
		Topic:                  topic,
		Balancer:               &kafka.LeastBytes{},
		AllowAutoTopicCreation: true,
	}
	defer w.Close()

	err := w.WriteMessages(context.Background(), kafka.Message{
		Key:   []byte(key),
		Value: value,
	})
	if err != nil {
		log.Printf("[Publish Kafka Error on topic %s]: %v\n", topic, err)
	} else {
		log.Printf("[Publish Kafka Success on topic %s] key=%s\n", topic, key)
	}
	return err
}


// Background Kafka Consumers (Choreography Pattern)

// Inventory Service Consumer
func startInventoryConsumer(ctx context.Context) {
	// Consumer 1: Order Created -> Deduct Stock
	go func() {
		readerCreated := kafka.NewReader(kafka.ReaderConfig{
			Brokers:     []string{kafkaBroker},
			Topic:       "saga.order.created",
			GroupID:     "inventory-order-created-group",
			StartOffset: kafka.FirstOffset,
		})
		defer readerCreated.Close()

		for {
			m, err := readerCreated.ReadMessage(ctx)
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				time.Sleep(100 * time.Millisecond)
				continue
			}
			if string(m.Key) == "INIT" {
				continue
			}
			var evt OrderCreatedEvent
			json.Unmarshal(m.Value, &evt)
			log.Printf("[Inventory Service] Reacting to saga.order.created for %s\n", evt.OrderID)

			err = database.DeductStock(evt.ItemID, evt.Quantity)
			if err != nil {
				log.Printf("[Inventory Service] Stock deduction failed for %s: %v\n", evt.OrderID, err)
				database.LogSagaStep(evt.OrderID, "InventoryService", "DeductStock", "FAILED", err.Error())

				// Publish Inventory Failed Event
				failEvt, _ := json.Marshal(InventoryFailedEvent{OrderID: evt.OrderID, Reason: err.Error()})
				publishKafkaMessage("saga.inventory.failed", evt.OrderID, failEvt)
			} else {
				log.Printf("[Inventory Service] Stock reserved successfully for %s\n", evt.OrderID)
				database.LogSagaStep(evt.OrderID, "InventoryService", "DeductStock", "EXECUTED", fmt.Sprintf("Deducted %d units", evt.Quantity))

				// Publish Inventory Reserved Event
				resEvt, _ := json.Marshal(InventoryReservedEvent{
					OrderID:     evt.OrderID,
					ItemID:      evt.ItemID,
					Quantity:    evt.Quantity,
					Amount:      evt.Amount,
					FailPayment: evt.FailPayment,
				})
				publishKafkaMessage("saga.inventory.reserved", evt.OrderID, resEvt)
			}
		}
	}()

	// Consumer 2: Payment Failed -> Compensation (Restore Stock)
	go func() {
		readerPayFailed := kafka.NewReader(kafka.ReaderConfig{
			Brokers:     []string{kafkaBroker},
			Topic:       "saga.payment.failed",
			GroupID:     "inventory-payment-failed-group",
			StartOffset: kafka.FirstOffset,
		})
		defer readerPayFailed.Close()

		for {
			m, err := readerPayFailed.ReadMessage(ctx)
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				time.Sleep(100 * time.Millisecond)
				continue
			}
			if string(m.Key) == "INIT" {
				continue
			}
			var evt PaymentFailedEvent
			json.Unmarshal(m.Value, &evt)
			log.Printf("[Inventory Service] COMPENSATION: Payment failed for %s. Restoring stock...\n", evt.OrderID)

			err = database.RestoreStock(evt.ItemID, evt.Quantity)
			if err != nil {
				log.Printf("[Inventory Service] COMPENSATION ERROR restoring stock: %v\n", err)
			} else {
				database.LogSagaStep(evt.OrderID, "InventoryService", "RestoreStock", "COMPENSATED", fmt.Sprintf("Restored %d units due to payment failure", evt.Quantity))
			}
		}
	}()
}

// Payment Service Consumer
func startPaymentConsumer(ctx context.Context) {
	go func() {
		reader := kafka.NewReader(kafka.ReaderConfig{
			Brokers:     []string{kafkaBroker},
			Topic:       "saga.inventory.reserved",
			GroupID:     "payment-inventory-reserved-group",
			StartOffset: kafka.FirstOffset,
		})
		defer reader.Close()

		for {
			m, err := reader.ReadMessage(ctx)
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				time.Sleep(100 * time.Millisecond)
				continue
			}
			if string(m.Key) == "INIT" {
				continue
			}
			var evt InventoryReservedEvent
			json.Unmarshal(m.Value, &evt)
			log.Printf("[Payment Service] Reacting to saga.inventory.reserved for %s\n", evt.OrderID)

			paymentID := "PAY-" + uuid.New().String()[:8]
			if evt.FailPayment {
				// Trigger Payment Failure (Rollback path)
				database.CreatePayment(paymentID, evt.OrderID, evt.Amount, "FAILED")
				database.LogSagaStep(evt.OrderID, "PaymentService", "ProcessPayment", "FAILED", "Payment rejected by gateway rule")

				payFailed, _ := json.Marshal(PaymentFailedEvent{
					OrderID:  evt.OrderID,
					ItemID:   evt.ItemID,
					Quantity: evt.Quantity,
					Reason:   "Payment rejected",
				})
				publishKafkaMessage("saga.payment.failed", evt.OrderID, payFailed)
			} else {
				// Payment Success (Happy path)
				database.CreatePayment(paymentID, evt.OrderID, evt.Amount, "SUCCESS")
				database.LogSagaStep(evt.OrderID, "PaymentService", "ProcessPayment", "EXECUTED", "Payment charged successfully")

				paySuccess, _ := json.Marshal(PaymentSuccessEvent{OrderID: evt.OrderID})
				publishKafkaMessage("saga.payment.success", evt.OrderID, paySuccess)
			}
		}
	}()
}

// Order State Consumer
func startOrderStateConsumer(ctx context.Context) {
	// Consumer for Success
	go func() {
		readerSuccess := kafka.NewReader(kafka.ReaderConfig{
			Brokers:     []string{kafkaBroker},
			Topic:       "saga.payment.success",
			GroupID:     "order-payment-success-group",
			StartOffset: kafka.FirstOffset,
		})
		defer readerSuccess.Close()

		for {
			m, err := readerSuccess.ReadMessage(ctx)
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				time.Sleep(100 * time.Millisecond)
				continue
			}
			if string(m.Key) == "INIT" {
				continue
			}
			var evt PaymentSuccessEvent
			json.Unmarshal(m.Value, &evt)
			database.UpdateOrderStatus(evt.OrderID, "COMPLETED")
			database.LogSagaStep(evt.OrderID, "OrderService", "FinalizeOrder", "EXECUTED", "Order status updated to COMPLETED")
		}
	}()

	// Consumer for Payment Fail
	go func() {
		readerPayFail := kafka.NewReader(kafka.ReaderConfig{
			Brokers:     []string{kafkaBroker},
			Topic:       "saga.payment.failed",
			GroupID:     "order-payment-failed-group",
			StartOffset: kafka.FirstOffset,
		})
		defer readerPayFail.Close()

		for {
			m, err := readerPayFail.ReadMessage(ctx)
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				time.Sleep(100 * time.Millisecond)
				continue
			}
			if string(m.Key) == "INIT" {
				continue
			}
			var evt PaymentFailedEvent
			json.Unmarshal(m.Value, &evt)
			database.UpdateOrderStatus(evt.OrderID, "CANCELLED")
			database.LogSagaStep(evt.OrderID, "OrderService", "FinalizeOrder", "COMPENSATED", "Order status updated to CANCELLED due to Payment Failure")
		}
	}()

	// Consumer for Inventory Fail
	go func() {
		readerInvFail := kafka.NewReader(kafka.ReaderConfig{
			Brokers:     []string{kafkaBroker},
			Topic:       "saga.inventory.failed",
			GroupID:     "order-inventory-failed-group",
			StartOffset: kafka.FirstOffset,
		})
		defer readerInvFail.Close()

		for {
			m, err := readerInvFail.ReadMessage(ctx)
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				time.Sleep(100 * time.Millisecond)
				continue
			}
			if string(m.Key) == "INIT" {
				continue
			}
			var evt InventoryFailedEvent
			json.Unmarshal(m.Value, &evt)
			database.UpdateOrderStatus(evt.OrderID, "CANCELLED")
			database.LogSagaStep(evt.OrderID, "OrderService", "FinalizeOrder", "COMPENSATED", "Order status updated to CANCELLED due to Inventory Failure")
		}
	}()
}


