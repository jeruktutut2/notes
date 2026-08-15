package kafka

import (
	"context"
	"log"
	"strings"

	"github.com/segmentio/kafka-go"
)

// MessageHandler is a function that handles a consumed Kafka message
type MessageHandler func(ctx context.Context, msg kafka.Message) error

// Consumer wraps kafka-go reader for consuming messages
type Consumer struct {
	brokers []string
	groupID string
}

// NewConsumer creates a new Kafka consumer
func NewConsumer(brokers string, groupID string) *Consumer {
	return &Consumer{
		brokers: strings.Split(brokers, ","),
		groupID: groupID,
	}
}

// Subscribe starts consuming messages from the specified topic
// This is a blocking call - should be run in a goroutine
func (c *Consumer) Subscribe(ctx context.Context, topic string, handler MessageHandler) {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  c.brokers,
		Topic:    topic,
		GroupID:  c.groupID,
		MinBytes: 1,
		MaxBytes: 10e6,
	})

	log.Printf("[KAFKA CONSUMER] Subscribed to topic=%s group=%s", topic, c.groupID)

	for {
		select {
		case <-ctx.Done():
			log.Printf("[KAFKA CONSUMER] Stopping consumer for topic=%s", topic)
			reader.Close()
			return
		default:
			msg, err := reader.ReadMessage(ctx)
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				log.Printf("[KAFKA CONSUMER] Error reading from %s: %v", topic, err)
				continue
			}

			log.Printf("[KAFKA CONSUMER] Received from topic=%s key=%s", topic, string(msg.Key))

			if err := handler(ctx, msg); err != nil {
				log.Printf("[KAFKA CONSUMER] Error handling message from %s: %v", topic, err)
			}
		}
	}
}

// SubscribeMultiple starts consuming from multiple topics with their respective handlers
func (c *Consumer) SubscribeMultiple(ctx context.Context, topicHandlers map[string]MessageHandler) {
	for topic, handler := range topicHandlers {
		go c.Subscribe(ctx, topic, handler)
	}
}
