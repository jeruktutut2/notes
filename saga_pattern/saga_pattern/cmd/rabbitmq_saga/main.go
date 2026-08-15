package main

import (
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
	amqp "github.com/rabbitmq/amqp091-go"

	"saga_pattern/common/db"
)

// Command & Event Models
type ReserveInventoryCommand struct {
	OrderID     string  `json:"order_id"`
	ItemID      string  `json:"item_id"`
	Quantity    int     `json:"quantity"`
	Amount      float64 `json:"amount"`
	FailPayment bool    `json:"fail_payment"`
}

type ProcessPaymentCommand struct {
	OrderID     string  `json:"order_id"`
	Amount      float64 `json:"amount"`
	FailPayment bool    `json:"fail_payment"`
}

type CompensateInventoryCommand struct {
	OrderID  string `json:"order_id"`
	ItemID   string `json:"item_id"`
	Quantity int    `json:"quantity"`
}

type StepResponse struct {
	OrderID  string `json:"order_id"`
	StepName string `json:"step_name"`
	Success  bool   `json:"success"`
	Message  string `json:"message"`
	ItemID   string `json:"item_id,omitempty"`
	Quantity int    `json:"quantity,omitempty"`
}

type CreateOrderRequest struct {
	ItemID      string  `json:"item_id"`
	Quantity    int     `json:"quantity"`
	Amount      float64 `json:"amount"`
	FailPayment bool    `json:"fail_payment"`
}

var (
	amqpURL  string
	database *db.DB
	rmqConn  *amqp.Connection
	rmqChan  *amqp.Channel
)

func main() {
	amqpURL = getEnv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

	// Connect to Database
	var err error
	database, err = db.ConnectDB()
	if err != nil {
		log.Fatalf("Database connection failed: %v", err)
	}

	// Connect to RabbitMQ with retries
	initRabbitMQ()
	defer rmqConn.Close()
	defer rmqChan.Close()

	// Start 3 Dedicated Logic Modules (Order Orchestrator, Inventory Worker, Payment Worker)
	go startInventoryWorker()
	go startPaymentWorker()
	go startOrchestratorReplyConsumer()

	// Echo v5 Web Server
	e := echo.New()

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP", "saga": "RabbitMQ Orchestration"})
	})

	e.POST("/rabbitmq/orders", handleCreateRabbitMQOrder)
	e.GET("/orders/:id", handleGetOrder)
	e.GET("/inventory", handleGetInventory)

	port := getEnv("PORT", "8082")
	go func() {
		if err := e.Start(":" + port); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Echo server shut down: %v", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down RabbitMQ Orchestration Saga Service...")
}

func getEnv(key, fallback string) string {
	if val, ok := os.LookupEnv(key); ok {
		return val
	}
	return fallback
}

func initRabbitMQ() {
	var err error
	for i := 0; i < 15; i++ {
		rmqConn, err = amqp.Dial(amqpURL)
		if err == nil {
			rmqChan, err = rmqConn.Channel()
			if err == nil {
				log.Println("Connected to RabbitMQ successfully!")

				// Declare Queues
				queues := []string{
					"cmd.inventory.reserve",
					"cmd.inventory.compensate",
					"cmd.payment.process",
					"reply.inventory",
					"reply.payment",
				}
				for _, q := range queues {
					_, err = rmqChan.QueueDeclare(q, true, false, false, false, nil)
					if err != nil {
						log.Fatalf("Failed to declare queue %s: %v", q, err)
					}
				}
				return
			}
		}
		log.Printf("Waiting for RabbitMQ... attempt %d/15 (error: %v)\n", i+1, err)
		time.Sleep(2 * time.Second)
	}
	log.Fatalf("Could not connect to RabbitMQ: %v", err)
}

// HTTP Handlers
func handleCreateRabbitMQOrder(c echo.Context) error {
	var req CreateOrderRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request body"})
	}

	if req.ItemID == "" || req.Quantity <= 0 {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid item_id or quantity"})
	}

	orderID := "ORD-RMQ-" + uuid.New().String()[:8]

	// 1. Create order record in PENDING
	err := database.CreateOrder(orderID, req.ItemID, req.Quantity, req.Amount, "RABBITMQ_ORCHESTRATION")
	if err != nil {
		log.Printf("Failed to create order in DB for RabbitMQ: %v\n", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": fmt.Sprintf("Failed to create order: %v", err)})
	}
	_ = database.LogSagaStep(orderID, "OrchestratorService", "StartSaga", "PENDING", "Saga Orchestration started")

	// 2. Orchestrator issues Command 1: Reserve Inventory
	cmd := ReserveInventoryCommand{
		OrderID:     orderID,
		ItemID:      req.ItemID,
		Quantity:    req.Quantity,
		Amount:      req.Amount,
		FailPayment: req.FailPayment,
	}
	body, _ := json.Marshal(cmd)
	sendRMQCommand("cmd.inventory.reserve", body)
	_ = database.LogSagaStep(orderID, "OrchestratorService", "SendCommand", "EXECUTED", "Sent ReserveInventoryCommand to RabbitMQ")

	return c.JSON(http.StatusAccepted, map[string]interface{}{
		"message":  "Order processing started (RabbitMQ Orchestration)",
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

func sendRMQCommand(queue string, body []byte) {
	err := rmqChan.Publish(
		"",    // exchange
		queue, // routing key
		false, // mandatory
		false, // immediate
		amqp.Publishing{
			ContentType: "application/json",
			Body:        body,
		})
	if err != nil {
		log.Printf("Failed to publish RMQ command to %s: %v\n", queue, err)
	}
}

// -------------------------------------------------------------
// MODULE 1: Service Orchestrator Reply Consumer
// -------------------------------------------------------------
func startOrchestratorReplyConsumer() {
	invReplies, _ := rmqChan.Consume("reply.inventory", "", true, false, false, false, nil)
	payReplies, _ := rmqChan.Consume("reply.payment", "", true, false, false, false, nil)

	go func() {
		for d := range invReplies {
			var resp StepResponse
			json.Unmarshal(d.Body, &resp)
			log.Printf("[Orchestrator] Received Inventory Reply for %s: Success=%v\n", resp.OrderID, resp.Success)

			if resp.Success {
				// Step 2: Inventory Reserved -> Orchestrator issues Command 2: Process Payment
				var orderAmount float64
				_ = database.QueryRow(`SELECT total_amount FROM orders WHERE id = $1`, resp.OrderID).Scan(&orderAmount)

				payCmd, _ := json.Marshal(ProcessPaymentCommand{
					OrderID:     resp.OrderID,
					Amount:      orderAmount,
					FailPayment: resp.Message == "FAIL_PAYMENT_REQUESTED",
				})
				sendRMQCommand("cmd.payment.process", payCmd)
				_ = database.LogSagaStep(resp.OrderID, "OrchestratorService", "ProcessPaymentCommand", "EXECUTED", "Sent ProcessPaymentCommand to RabbitMQ")
			} else {
				// Inventory failed -> Abort Saga
				_ = database.UpdateOrderStatus(resp.OrderID, "CANCELLED")
				_ = database.LogSagaStep(resp.OrderID, "OrchestratorService", "AbortSaga", "FAILED", "Saga aborted due to inventory failure")
			}
		}
	}()

	go func() {
		for d := range payReplies {
			var resp StepResponse
			json.Unmarshal(d.Body, &resp)
			log.Printf("[Orchestrator] Received Payment Reply for %s: Success=%v\n", resp.OrderID, resp.Success)

			if resp.Success {
				// Saga Completed Successfully!
				_ = database.UpdateOrderStatus(resp.OrderID, "COMPLETED")
				_ = database.LogSagaStep(resp.OrderID, "OrchestratorService", "FinalizeSaga", "EXECUTED", "Saga completed successfully")
			} else {
				// Payment Failed! Orchestrator triggers COMPENSATION!
				log.Printf("[Orchestrator] TRIGGERING COMPENSATION for Order %s\n", resp.OrderID)
				_ = database.LogSagaStep(resp.OrderID, "OrchestratorService", "TriggerCompensation", "FAILED", "Payment failed. Sending CompensateInventoryCommand")

				compCmd, _ := json.Marshal(CompensateInventoryCommand{
					OrderID:  resp.OrderID,
					ItemID:   resp.ItemID,
					Quantity: resp.Quantity,
				})
				sendRMQCommand("cmd.inventory.compensate", compCmd)

				_ = database.UpdateOrderStatus(resp.OrderID, "CANCELLED")
				_ = database.LogSagaStep(resp.OrderID, "OrchestratorService", "FinalizeSaga", "COMPENSATED", "Saga cancelled and compensation executed")
			}
		}
	}()
}

// -------------------------------------------------------------
// MODULE 2: Inventory Worker Service
// -------------------------------------------------------------
func startInventoryWorker() {
	cmdReserve, _ := rmqChan.Consume("cmd.inventory.reserve", "", true, false, false, false, nil)
	cmdCompensate, _ := rmqChan.Consume("cmd.inventory.compensate", "", true, false, false, false, nil)

	go func() {
		for d := range cmdReserve {
			var cmd ReserveInventoryCommand
			json.Unmarshal(d.Body, &cmd)
			log.Printf("[Inventory Worker] Processing ReserveInventoryCommand for %s\n", cmd.OrderID)

			err := database.DeductStock(cmd.ItemID, cmd.Quantity)
			var resp StepResponse
			if err != nil {
				_ = database.LogSagaStep(cmd.OrderID, "InventoryWorker", "DeductStock", "FAILED", err.Error())
				resp = StepResponse{OrderID: cmd.OrderID, StepName: "ReserveInventory", Success: false, Message: err.Error()}
			} else {
				_ = database.LogSagaStep(cmd.OrderID, "InventoryWorker", "DeductStock", "EXECUTED", fmt.Sprintf("Reserved %d units", cmd.Quantity))
				msg := "SUCCESS"
				if cmd.FailPayment {
					msg = "FAIL_PAYMENT_REQUESTED"
				}
				resp = StepResponse{
					OrderID:  cmd.OrderID,
					StepName: "ReserveInventory",
					Success:  true,
					Message:  msg,
					ItemID:   cmd.ItemID,
					Quantity: cmd.Quantity,
				}
			}

			body, _ := json.Marshal(resp)
			sendRMQCommand("reply.inventory", body)
		}
	}()

	go func() {
		for d := range cmdCompensate {
			var cmd CompensateInventoryCommand
			json.Unmarshal(d.Body, &cmd)
			log.Printf("[Inventory Worker] Processing Compensation for %s (Restoring Stock)\n", cmd.OrderID)

			err := database.RestoreStock(cmd.ItemID, cmd.Quantity)
			if err != nil {
				log.Printf("[Inventory Worker] Compensation error: %v\n", err)
			} else {
				_ = database.LogSagaStep(cmd.OrderID, "InventoryWorker", "RestoreStock", "COMPENSATED", fmt.Sprintf("Restored %d units", cmd.Quantity))
			}
		}
	}()
}

// -------------------------------------------------------------
// MODULE 3: Payment Worker Service
// -------------------------------------------------------------
func startPaymentWorker() {
	cmdPay, _ := rmqChan.Consume("cmd.payment.process", "", true, false, false, false, nil)

	for d := range cmdPay {
		var cmd ProcessPaymentCommand
		json.Unmarshal(d.Body, &cmd)
		log.Printf("[Payment Worker] Processing ProcessPaymentCommand for %s\n", cmd.OrderID)

		paymentID := "PAY-RMQ-" + uuid.New().String()[:8]
		var resp StepResponse
		if cmd.FailPayment {
			_ = database.CreatePayment(paymentID, cmd.OrderID, cmd.Amount, "FAILED")
			_ = database.LogSagaStep(cmd.OrderID, "PaymentWorker", "ProcessPayment", "FAILED", "Payment rejected by mock rule")

			// Fetch item info for compensation reply
			var itemID string
			var qty int
			_ = database.QueryRow(`SELECT item_id, quantity FROM orders WHERE id = $1`, cmd.OrderID).Scan(&itemID, &qty)

			resp = StepResponse{
				OrderID:  cmd.OrderID,
				StepName: "ProcessPayment",
				Success:  false,
				Message:  "Payment failed",
				ItemID:   itemID,
				Quantity: qty,
			}
		} else {
			_ = database.CreatePayment(paymentID, cmd.OrderID, cmd.Amount, "SUCCESS")
			_ = database.LogSagaStep(cmd.OrderID, "PaymentWorker", "ProcessPayment", "EXECUTED", "Payment processed successfully")
			resp = StepResponse{OrderID: cmd.OrderID, StepName: "ProcessPayment", Success: true, Message: "Payment successful"}
		}

		body, _ := json.Marshal(resp)
		sendRMQCommand("reply.payment", body)
	}
}
