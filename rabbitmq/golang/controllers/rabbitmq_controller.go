package controllers

import (
	"net/http"
	"note-golang-rabbitmq/services"

	"github.com/labstack/echo/v4"
)

type RabbitmqController interface {
	SendTextMessage(c echo.Context) error
}

type rabbitmqController struct {
	RabbitmqService services.RabbitmqService
}

func NewRabbitmqController(rabbitmqService services.RabbitmqService) RabbitmqController {
	return &rabbitmqController{
		RabbitmqService: rabbitmqService,
	}
}

func (controller *rabbitmqController) SendTextMessage(c echo.Context) error {
	key := c.QueryParam("key")
	message := c.QueryParam("message")
	response := controller.RabbitmqService.SendTextMessage(c.Request().Context(), key, message)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"message": response,
	})
}
