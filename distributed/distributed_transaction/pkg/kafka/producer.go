package kafka

import (
	"context"
	"log"
	"strings"

	"github.com/segmentio/kafka-go"
)

// Producer wraps kafka-go writer for publishing messages
type Producer struct {
	brokers []string
}

// NewProducer creates a new Kafka producer
func NewProducer(brokers string) *Producer {
	return &Producer{
		brokers: strings.Split(brokers, ","),
	}
}

// Publish sends a message to the specified Kafka topic
func (p *Producer) Publish(ctx context.Context, topic string, key string, value []byte) error {
	writer := &kafka.Writer{
		Addr:         kafka.TCP(p.brokers...),
		Topic:        topic,
		Balancer:     &kafka.LeastBytes{},
		RequiredAcks: kafka.RequireAll,
	}
	defer writer.Close()

	msg := kafka.Message{
		Key:   []byte(key),
		Value: value,
	}

	err := writer.WriteMessages(ctx, msg)
	if err != nil {
		log.Printf("[KAFKA PRODUCER] Failed to publish to %s: %v", topic, err)
		return err
	}

	log.Printf("[KAFKA PRODUCER] Published to topic=%s key=%s", topic, key)
	return nil
}
