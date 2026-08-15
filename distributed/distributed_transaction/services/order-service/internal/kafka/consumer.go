package kafka

import (
	"context"
	"log"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/order-service/internal/service"

	segkafka "github.com/segmentio/kafka-go"
)

// StartConsumers starts all Kafka consumers for the Order Service
// Order Service mendengarkan:
// - inventory.reserved  → update status ke INVENTORY_RESERVED
// - inventory.failed    → saga failed (stok tidak cukup)
// - payment.completed   → update status ke PAYMENT_COMPLETED
// - payment.failed      → saga failed (payment gagal)
// - shipping.created    → saga complete!
// - shipping.failed     → saga failed (shipping gagal)
func StartConsumers(ctx context.Context, brokers string, svc *service.OrderService) {
	consumer := pkgkafka.NewConsumer(brokers, "order-service-group")

	handlers := map[string]pkgkafka.MessageHandler{
		events.TopicInventoryReserved: func(ctx context.Context, msg segkafka.Message) error {
			var event events.InventoryReservedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[ORDER CONSUMER] ✅ Inventory reserved for order: %s", event.OrderID)
			return svc.HandleInventoryReserved(event.OrderID)
		},

		events.TopicInventoryFailed: func(ctx context.Context, msg segkafka.Message) error {
			var event events.InventoryFailedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[ORDER CONSUMER] ❌ Inventory failed for order: %s reason: %s", event.OrderID, event.Reason)
			return svc.HandleSagaFailure(event.OrderID, "Inventory: "+event.Reason)
		},

		events.TopicPaymentCompleted: func(ctx context.Context, msg segkafka.Message) error {
			var event events.PaymentCompletedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[ORDER CONSUMER] ✅ Payment completed for order: %s", event.OrderID)
			return svc.HandlePaymentCompleted(event.OrderID)
		},

		events.TopicPaymentFailed: func(ctx context.Context, msg segkafka.Message) error {
			var event events.PaymentFailedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[ORDER CONSUMER] ❌ Payment failed for order: %s reason: %s", event.OrderID, event.Reason)
			return svc.HandleSagaFailure(event.OrderID, "Payment: "+event.Reason)
		},

		events.TopicShippingCreated: func(ctx context.Context, msg segkafka.Message) error {
			var event events.ShippingCreatedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[ORDER CONSUMER] ✅ Shipping created for order: %s tracking: %s", event.OrderID, event.TrackingNumber)
			return svc.HandleShippingCreated(event.OrderID)
		},

		events.TopicShippingFailed: func(ctx context.Context, msg segkafka.Message) error {
			var event events.ShippingFailedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[ORDER CONSUMER] ❌ Shipping failed for order: %s reason: %s", event.OrderID, event.Reason)
			return svc.HandleSagaFailure(event.OrderID, "Shipping: "+event.Reason)
		},
	}

	consumer.SubscribeMultiple(ctx, handlers)
	log.Println("[ORDER CONSUMER] All consumers started")
}
