package kafka

import (
	"context"
	"log"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/payment-service/internal/service"

	segkafka "github.com/segmentio/kafka-go"
)

// StartConsumers starts all Kafka consumers for Payment Service
// Payment Service mendengarkan:
// - inventory.reserved → proses pembayaran
// - shipping.failed    → refund payment (compensation)
func StartConsumers(ctx context.Context, brokers string, svc *service.PaymentService) {
	consumer := pkgkafka.NewConsumer(brokers, "payment-service-group")

	handlers := map[string]pkgkafka.MessageHandler{
		// Saat inventory berhasil di-reserve, proses payment
		events.TopicInventoryReserved: func(ctx context.Context, msg segkafka.Message) error {
			var event events.InventoryReservedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[PAYMENT CONSUMER] Received inventory.reserved for order: %s", event.OrderID)

			// Kita perlu amount - untuk simplicity, kita gunakan quantity * 10000 sebagai harga
			// Dalam real app, amount akan ada di event atau di-query dari order service
			amount := float64(event.Quantity) * 10000
			return svc.ProcessPayment(event.OrderID, amount)
		},

		// Saat shipping gagal, refund payment (compensation)
		events.TopicShippingFailed: func(ctx context.Context, msg segkafka.Message) error {
			var event events.ShippingFailedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[PAYMENT CONSUMER] Received shipping.failed → REFUNDING payment for order: %s", event.OrderID)
			return svc.RefundPayment(event.OrderID)
		},
	}

	consumer.SubscribeMultiple(ctx, handlers)
	log.Println("[PAYMENT CONSUMER] All consumers started")
}
