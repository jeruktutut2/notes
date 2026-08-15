package kafka

import (
	"context"
	"log"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/shipping-service/internal/service"

	segkafka "github.com/segmentio/kafka-go"
)

// StartConsumers starts all Kafka consumers for Shipping Service
// Shipping Service mendengarkan:
// - payment.completed → create shipment
func StartConsumers(ctx context.Context, brokers string, svc *service.ShippingService) {
	consumer := pkgkafka.NewConsumer(brokers, "shipping-service-group")

	handlers := map[string]pkgkafka.MessageHandler{
		// Saat payment berhasil, buat shipment
		events.TopicPaymentCompleted: func(ctx context.Context, msg segkafka.Message) error {
			var event events.PaymentCompletedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[SHIPPING CONSUMER] Received payment.completed for order: %s", event.OrderID)
			return svc.CreateShipment(event.OrderID)
		},
	}

	consumer.SubscribeMultiple(ctx, handlers)
	log.Println("[SHIPPING CONSUMER] All consumers started")
}
