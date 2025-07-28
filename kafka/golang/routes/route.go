package routes

import (
	"log"
	"note-golang-kafka/controllers"
	"note-golang-kafka/services"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	"github.com/labstack/echo/v4"
)

func SetKafkaRoute(e *echo.Echo) {
	config := &kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092",
	}
	producer, err := kafka.NewProducer(config)
	if err != nil {
		log.Fatalln("error creating producer:", err)
	}
	kafkaService := services.NewKafkaService(producer)
	kafkaController := controllers.NewKafkaController(kafkaService)
	e.GET("/api/v1/message/send-message", kafkaController.SendMessage)
}
