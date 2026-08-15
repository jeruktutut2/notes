package kafka

import (
	"context"
	"log"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/notification-service/internal/service"

	segkafka "github.com/segmentio/kafka-go"
)

// StartConsumers starts all Kafka consumers for Notification Service
// Notification Service mendengarkan:
// - order.completed → kirim notifikasi sukses
// - order.failed    → kirim notifikasi gagal
func StartConsumers(ctx context.Context, brokers string, svc *service.NotificationService) {
	consumer := pkgkafka.NewConsumer(brokers, "notification-service-group")

	handlers := map[string]pkgkafka.MessageHandler{
		events.TopicOrderCompleted: func(ctx context.Context, msg segkafka.Message) error {
			var event events.OrderCompletedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[NOTIFICATION CONSUMER] Received order.completed for order: %s", event.OrderID)
			return svc.SendOrderCompletedNotification(event.OrderID)
		},

		events.TopicOrderFailed: func(ctx context.Context, msg segkafka.Message) error {
			var event events.OrderFailedEvent
			if err := events.Unmarshal(msg.Value, &event); err != nil {
				return err
			}
			log.Printf("[NOTIFICATION CONSUMER] Received order.failed for order: %s reason: %s", event.OrderID, event.Reason)
			return svc.SendOrderFailedNotification(event.OrderID, event.Reason)
		},
	}

	consumer.SubscribeMultiple(ctx, handlers)
	log.Println("[NOTIFICATION CONSUMER] All consumers started")
}
