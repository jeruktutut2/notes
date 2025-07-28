package controllers

import (
	"net/http"
	"note-golang-kafka/services"

	"github.com/labstack/echo/v4"
)

type KafkaController interface {
	SendMessage(c echo.Context) error
}

type kafkaController struct {
	KafkaService services.KafkaService
}

func NewKafkaController(kafkaService services.KafkaService) KafkaController {
	return &kafkaController{
		KafkaService: kafkaService,
	}
}

func (controller *kafkaController) SendMessage(c echo.Context) error {
	textMessage := c.QueryParam("message")
	response := controller.KafkaService.SendMessage(c.Request().Context(), textMessage)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}
