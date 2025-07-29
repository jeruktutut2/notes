package consumers

import (
	"context"
	"log"
	"time"

	"github.com/rabbitmq/amqp091-go"
)

type RabbitmqConsumer interface {
	ReadTextMessage()
}

type rabbitmqConsumer struct {
	Channel *amqp091.Channel
}

func NewRabbitmqConsumer(channel *amqp091.Channel) RabbitmqConsumer {
	return &rabbitmqConsumer{
		Channel: channel,
	}
}

func (consumer *rabbitmqConsumer) ReadTextMessage() {
	go func() {
		ctx := context.Background()
		textMessageDeliverys, err := consumer.Channel.ConsumeWithContext(ctx, "text-message", "text-message-consumer", true, false, false, false, nil)
		if err != nil {
			log.Fatalln(time.Now().String(), "error when consuming text message:", err)
		}
		println(time.Now().String(), "rabbitmq: listening to text-message queue")

		for textMessageDelivery := range textMessageDeliverys {
			println(time.Now().String(), "text-message:", textMessageDelivery.RoutingKey, string(textMessageDelivery.Body))
		}
	}()
}
