package utils

import (
	"fmt"
	"log"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

type MqttUtil interface {
	GetClient() mqtt.Client
	Close()
}

type mqttUtil struct {
	Client mqtt.Client
}

func NewMqttUtil() MqttUtil {
	opts := mqtt.NewClientOptions()
	opts.AddBroker("tcp://localhost:1883") // Alamat broker MQTT
	opts.SetClientID("golang_mqtt_client") // Client ID
	// opts.SetUsername("admin")              // Username (if using authentication)
	// opts.SetPassword("password123")        // Password (if using authentication)
	opts.OnConnect = func(client mqtt.Client) {
		fmt.Println("Terkoneksi ke broker MQTT!")
	}
	opts.OnConnectionLost = func(client mqtt.Client, err error) {
		fmt.Printf("Koneksi terputus: %v\n", err)
	}

	println(time.Now().String(), "mqtt: connecting")
	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		log.Fatalln("error when connecting to mqtt:", token.Error())
	}
	println(time.Now().String(), "mqtt: connected")

	return &mqttUtil{
		Client: client,
	}
}

func (util *mqttUtil) GetClient() mqtt.Client {
	return util.Client
}

func (util *mqttUtil) Close() {
	fmt.Println("mqtt: closing")
	util.Client.Disconnect(250)
	fmt.Println("mqtt: closed")
}
