package kafka

import (
	"context"
	"log"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/inventory-service/internal/service"

	segkafka "github.com/segmentio/kafka-go"
)

// StartConsumers starts all Kafka consumers for Inventory Service
// Inventory Service mendengarkan:
// - order.created   → reserve stock
// - payment.failed  → release stock (compensation)
// - shipping.failed → release stock (compensation)
func StartConsumers(ctx context.Context, brokers string, svc *service.InventoryService) {
	consumer := pkgkafka.NewConsumer(brokers, "inventory-service-group")

	handlers := map[string]pkgkafka.MessageHandler{
		// Saat order dibuat, coba reserve stock
		events.TopicOrderCreated: func(ctx context.Context, msg segkafka.Message) error {
			var event events.OrderCreatedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[INVENTORY CONSUMER] Received order.created: order=%s product=%s qty=%d",
				event.OrderID, event.ProductID, event.Quantity)
			return svc.ReserveStock(event.OrderID, event.ProductID, event.Quantity)
		},

		// Saat payment gagal, release stock (compensation)
		events.TopicPaymentFailed: func(ctx context.Context, msg segkafka.Message) error {
			var event events.PaymentFailedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[INVENTORY CONSUMER] Received payment.failed → RELEASING stock for order: %s", event.OrderID)
			return svc.ReleaseStockByOrderID(event.OrderID)
		},

		// Saat shipping gagal, release stock (compensation)
		events.TopicShippingFailed: func(ctx context.Context, msg segkafka.Message) error {
			var event events.ShippingFailedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[INVENTORY CONSUMER] Received shipping.failed → RELEASING stock for order: %s", event.OrderID)
			return svc.ReleaseStockByOrderID(event.OrderID)
		},
	}

	consumer.SubscribeMultiple(ctx, handlers)
	log.Println("[INVENTORY CONSUMER] All consumers started")
}
