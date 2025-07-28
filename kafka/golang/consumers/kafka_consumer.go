package consumers

import (
	"context"
	"log"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
)

type KafkaConsumer interface {
	Close()
}

type kafkaConsumer struct {
	Consumer *kafka.Consumer
}

func NewKafkaConsumer(ctx context.Context) KafkaConsumer {
	config := &kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092",
		"group.id":          "text-message-consumer-group-table",
		"auto.offset.reset": "earliest",
	}
	consumer, err := kafka.NewConsumer(config)
	if err != nil {
		log.Fatalln("error when creating new consumer text-message:", err)
	}

	err = consumer.Subscribe("text-message", nil)
	if err != nil {
		log.Fatalln("error when subscribing consumer:", err)
	}

	go func() {
		for {
			select {
			case <-ctx.Done():
				log.Println("stopping consumer")
				return
			default:
				message, err := consumer.ReadMessage(-1)
				if err != nil {
					log.Println("error reading message:", err)
				} else {
					log.Println("message:", string(message.Value), message.TopicPartition.Partition, message.TopicPartition.Offset)
				}
			}
		}
	}()

	log.Println("listening consumer text-message")
	return &kafkaConsumer{
		Consumer: consumer,
	}
}

func (consumer *kafkaConsumer) Close() {
	err := consumer.Consumer.Close()
	if err != nil {
		log.Fatalln("error when closing kafka consumer:", err)
	}
	log.Println("stop consumer")
}
