package routes

import (
	"note-golang-rabbitmq/controllers"
	"note-golang-rabbitmq/services"

	"github.com/labstack/echo/v4"
	"github.com/rabbitmq/amqp091-go"
)

func SetRabbitmqRoute(e *echo.Echo, channel *amqp091.Channel) {
	rabbitmqService := services.NewRabbitmqService(channel)
	rabbitmqController := controllers.NewRabbitmqController(rabbitmqService)
	e.GET("/api/v1/message/send-message", rabbitmqController.SendTextMessage)
}
