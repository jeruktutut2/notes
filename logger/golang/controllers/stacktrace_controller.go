package controllers

import (
	"net/http"
	"note-golang-logger/services"

	"github.com/labstack/echo/v4"
)

type LoggerController interface {
	CheckLogger(c echo.Context) error
}

type loggerController struct {
	loggerService services.LoggerService
}

func NewloggerController(loggerService services.LoggerService) LoggerController {
	return &loggerController{
		loggerService: loggerService,
	}
}

func (controller *loggerController) CheckLogger(c echo.Context) error {
	response := controller.loggerService.CheckLogger(c.Request().Context())
	return c.JSON(http.StatusOK, map[string]string{
		"response": response,
	})
}
