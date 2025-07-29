package controllers

import (
	"golang-note-mqtt/services"
	"net/http"

	"github.com/labstack/echo/v4"
)

type MqttController interface {
	SendMessage(c echo.Context) error
}

type mqttController struct {
	MqttService services.MqttService
}

func NewMqttController(mqttService services.MqttService) MqttController {
	return &mqttController{
		MqttService: mqttService,
	}
}

func (controller *mqttController) SendMessage(c echo.Context) error {
	message := c.QueryParam("message")
	response := controller.MqttService.SendMessage(message)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}
