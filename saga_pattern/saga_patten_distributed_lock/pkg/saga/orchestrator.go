package saga

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"saga-watchdog-demo/pkg/db"

	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/segmentio/kafka-go"
)

type SagaOrchestrator struct {
	db          *db.DB
	kafkaWriter *kafka.Writer
	rabbitConn  *amqp.Connection
	rabbitChan  *amqp.Channel
}

type OrderRequest struct {
	ProductID  string  `json:"product_id"`
	Quantity   int     `json:"quantity"`
	TotalPrice float64 `json:"total_price"`
	SimulateFailAt string `json:"simulate_fail_at"` // "", "inventory", "payment"
}

type SagaResult struct {
	OrderID string `json:"order_id"`
	Status  string `json:"status"`
	Message string `json:"message"`
}

type KafkaEvent struct {
	OrderID   string    `json:"order_id"`
	EventType string    `json:"event_type"`
	Timestamp time.Time `json:"timestamp"`
	Payload   string    `json:"payload"`
}

type RabbitMessage struct {
	OrderID    string  `json:"order_id"`
	ProductID  string  `json:"product_id"`
	Quantity   int     `json:"quantity"`
	Amount     float64 `json:"amount"`
	Action     string  `json:"action"` // "RESERVE_INVENTORY", "CANCEL_INVENTORY", "PROCESS_PAYMENT"
	ShouldFail bool    `json:"should_fail"`
}

func NewSagaOrchestrator(database *db.DB, kafkaBrokers []string, rabbitURL string) (*SagaOrchestrator, error) {
	// Initialize Kafka Writer
	writer := &kafka.Writer{
		Addr:     kafka.TCP(kafkaBrokers...),
		Topic:    "order-events",
		Balancer: &kafka.LeastBytes{},
	}

	// Initialize RabbitMQ Connection
	conn, err := amqp.Dial(rabbitURL)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to RabbitMQ: %w", err)
	}

	ch, err := conn.Channel()
	if err != nil {
		return nil, fmt.Errorf("failed to open RabbitMQ channel: %w", err)
	}

	// Declare RabbitMQ queues
	queues := []string{"inventory-service-queue", "payment-service-queue"}
	for _, q := range queues {
		_, err := ch.QueueDeclare(q, true, false, false, false, nil)
		if err != nil {
			return nil, fmt.Errorf("failed to declare RabbitMQ queue %s: %w", q, err)
		}
	}

	return &SagaOrchestrator{
		db:          database,
		kafkaWriter: writer,
		rabbitConn:  conn,
		rabbitChan:  ch,
	}, nil
}

func (so *SagaOrchestrator) Close() {
	if so.kafkaWriter != nil {
		so.kafkaWriter.Close()
	}
	if so.rabbitChan != nil {
		so.rabbitChan.Close()
	}
	if so.rabbitConn != nil {
		so.rabbitConn.Close()
	}
}

// PublishKafkaEvent sends audit event to Apache Kafka topic
func (so *SagaOrchestrator) PublishKafkaEvent(ctx context.Context, orderID, eventType, payload string) {
	event := KafkaEvent{
		OrderID:   orderID,
		EventType: eventType,
		Timestamp: time.Now(),
		Payload:   payload,
	}

	bytes, _ := json.Marshal(event)
	err := so.kafkaWriter.WriteMessages(ctx, kafka.Message{
		Key:   []byte(orderID),
		Value: bytes,
	})

	if err != nil {
		log.Printf("[KAFKA ERROR] Failed to publish event %s for order %s: %v", eventType, orderID, err)
	} else {
		log.Printf("[KAFKA AUDIT EVENT ➔] Topic: order-events | Event: %s | OrderID: %s", eventType, orderID)
	}
}

// SendRabbitCommand sends AMQP message to RabbitMQ queue
func (so *SagaOrchestrator) SendRabbitCommand(queueName string, msg RabbitMessage) error {
	body, _ := json.Marshal(msg)
	err := so.rabbitChan.Publish(
		"",        // exchange
		queueName, // routing key
		false,     // mandatory
		false,     // immediate
		amqp.Publishing{
			ContentType: "application/json",
			Body:        body,
		},
	)
	if err != nil {
		return fmt.Errorf("failed to publish to RabbitMQ %s: %w", queueName, err)
	}
	log.Printf("[RABBITMQ COMMAND ➔] Queue: %s | Action: %s | OrderID: %s", queueName, msg.Action, msg.OrderID)
	return nil
}

// ExecuteSaga executes the multi-step transaction with compensating rollback actions
func (so *SagaOrchestrator) ExecuteSaga(ctx context.Context, orderID string, req OrderRequest) (*SagaResult, error) {
	log.Printf("\n--- [SAGA START] Order ID: %s ---", orderID)

	// Step 1: Local DB Transaction (PostgreSQL via PgBouncer)
	order := db.Order{
		ID:         orderID,
		ProductID:  req.ProductID,
		Quantity:   req.Quantity,
		TotalPrice: req.TotalPrice,
		Status:     "PENDING",
		CreatedAt:  time.Now(),
	}

	if err := so.db.CreateOrder(order); err != nil {
		return nil, fmt.Errorf("failed to create pending order: %w", err)
	}
	log.Printf("[SAGA STEP 1] Created Order %s in PostgreSQL (Status: PENDING)", orderID)
	so.PublishKafkaEvent(ctx, orderID, "ORDER_CREATED", "Pending order created in DB")

	// Step 2: Reserve Inventory via RabbitMQ
	invFail := req.SimulateFailAt == "inventory"
	err := so.SendRabbitCommand("inventory-service-queue", RabbitMessage{
		OrderID:    orderID,
		ProductID:  req.ProductID,
		Quantity:   req.Quantity,
		Action:     "RESERVE_INVENTORY",
		ShouldFail: invFail,
	})

	if err != nil || invFail {
		log.Printf("[SAGA STEP 2 FAILED ❌] Inventory Reservation Failed for Order %s", orderID)
		
		// COMPENSATING ACTION FOR STEP 1: Cancel Order in DB
		so.db.UpdateOrderStatus(orderID, "CANCELLED_DUE_TO_INVENTORY_FAILURE")
		so.PublishKafkaEvent(ctx, orderID, "ORDER_CANCELLED", "Inventory reservation failed, order cancelled")

		log.Printf("--- [SAGA ROLLBACK COMPLETE] Order %s Cancelled ---", orderID)
		return &SagaResult{
			OrderID: orderID,
			Status:  "CANCELLED_DUE_TO_INVENTORY_FAILURE",
			Message: "Saga rolled back: Inventory reservation failed",
		}, nil
	}
	log.Printf("[SAGA STEP 2 SUCCESS ✔] Reserved %d items of %s", req.Quantity, req.ProductID)

	// Step 3: Process Payment via RabbitMQ
	payFail := req.SimulateFailAt == "payment"
	err = so.SendRabbitCommand("payment-service-queue", RabbitMessage{
		OrderID:    orderID,
		Amount:     req.TotalPrice,
		Action:     "PROCESS_PAYMENT",
		ShouldFail: payFail,
	})

	if err != nil || payFail {
		log.Printf("[SAGA STEP 3 FAILED ❌] Payment Processing Failed for Order %s", orderID)

		// COMPENSATING ACTION FOR STEP 2: Release Reserved Inventory via RabbitMQ
		log.Printf("[SAGA COMPENSATING ACTION ↺] Sending CANCEL_INVENTORY to RabbitMQ for Order %s", orderID)
		so.SendRabbitCommand("inventory-service-queue", RabbitMessage{
			OrderID:   orderID,
			ProductID: req.ProductID,
			Quantity:  req.Quantity,
			Action:    "CANCEL_INVENTORY",
		})

		// COMPENSATING ACTION FOR STEP 1: Update Order Status to Cancelled in DB
		so.db.UpdateOrderStatus(orderID, "CANCELLED_DUE_TO_PAYMENT_FAILURE")
		so.PublishKafkaEvent(ctx, orderID, "ORDER_CANCELLED", "Payment failed, inventory released, order cancelled")

		log.Printf("--- [SAGA ROLLBACK COMPLETE] Order %s Cancelled ---", orderID)
		return &SagaResult{
			OrderID: orderID,
			Status:  "CANCELLED_DUE_TO_PAYMENT_FAILURE",
			Message: "Saga rolled back: Payment failed, inventory released",
		}, nil
	}
	log.Printf("[SAGA STEP 3 SUCCESS ✔] Processed payment of $%.2f", req.TotalPrice)

	// Step 4: Finalize Order Status to COMPLETED in PostgreSQL
	if err := so.db.UpdateOrderStatus(orderID, "COMPLETED"); err != nil {
		return nil, fmt.Errorf("failed to complete order: %w", err)
	}
	so.PublishKafkaEvent(ctx, orderID, "ORDER_COMPLETED", "Order successfully processed and completed")

	log.Printf("--- [SAGA SUCCESS COMPLETE] Order %s Completed ---", orderID)
	return &SagaResult{
		OrderID: orderID,
		Status:  "COMPLETED",
		Message: "Saga completed successfully: Order confirmed and processed",
	}, nil
}
