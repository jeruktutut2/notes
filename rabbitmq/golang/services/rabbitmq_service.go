package services

import (
	"context"
	"fmt"
	"time"

	"github.com/rabbitmq/amqp091-go"
)

type RabbitmqService interface {
	SendTextMessage(ctx context.Context, key string, message string) (response string)
}

type rabbitmqService struct {
	Channel *amqp091.Channel
}

func NewRabbitmqService(channel *amqp091.Channel) RabbitmqService {
	return &rabbitmqService{
		Channel: channel,
	}
}

func (service *rabbitmqService) SendTextMessage(ctx context.Context, key string, message string) (response string) {
	messagePublish := amqp091.Publishing{
		Headers: amqp091.Table{
			"sample": "value",
		},
		Body: []byte("message: " + message),
	}
	err := service.Channel.PublishWithContext(ctx, "notification", key, false, false, messagePublish)
	if err != nil {
		fmt.Println(time.Now().String(), "error when publish message:", err)
		response = err.Error()
		return
	}
	response = "success"
	return
}
