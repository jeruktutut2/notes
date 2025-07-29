package consumers

import (
	"fmt"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

type MqttConsumer interface {
}

type mqttConsumer struct {
}

func NewMqttConsumer(client mqtt.Client) MqttConsumer {
	topic := "test/topic"
	token := client.Subscribe(topic, 1, func(client mqtt.Client, msg mqtt.Message) {
		fmt.Printf("Pesan diterima: [%s] %s\n", msg.Topic(), msg.Payload())
	})
	token.Wait()
	fmt.Println("subscribed to test/topic")
	return &mqttConsumer{}
}
