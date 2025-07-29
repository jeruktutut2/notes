package controllers

import (
	"net/http"
	"note-golang-stacktrace/services"

	"github.com/labstack/echo/v4"
)

type Controller interface {
	CheckStacktrace(c echo.Context) error
}

type controller struct {
	service services.Service
}

func NewController(service services.Service) Controller {
	return &controller{
		service: service,
	}
}

func (controller *controller) CheckStacktrace(c echo.Context) error {
	response := controller.service.CheckStacktrace(c.Request().Context())
	return c.JSON(http.StatusOK, map[string]string{
		"response": response,
	})
}
