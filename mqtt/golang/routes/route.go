package routes

import (
	"golang-note-mqtt/controllers"
	"golang-note-mqtt/services"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/labstack/echo/v4"
)

func SetMqttRoute(e *echo.Echo, client mqtt.Client) {
	mqttService := services.NewMqttService(client)
	mqttController := controllers.NewMqttController(mqttService)
	e.GET("/send-message", mqttController.SendMessage)
}
