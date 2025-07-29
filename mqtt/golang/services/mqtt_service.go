package services

import (
	"fmt"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

type MqttService interface {
	SendMessage(message string) (response string)
}

type mqttService struct {
	Client mqtt.Client
}

func NewMqttService(client mqtt.Client) MqttService {
	return &mqttService{
		Client: client,
	}
}

func (service *mqttService) SendMessage(message string) (response string) {
	token := service.Client.Publish("test/topic", 0, false, message)
	token.Wait()
	fmt.Println("sending message:", message)
	response = "success"
	return
}
