package routes

import (
	"note-golang-logger/controllers"
	"note-golang-logger/services"

	"github.com/labstack/echo/v4"
	"github.com/sirupsen/logrus"
)

func SetRoute(e *echo.Echo, logger *logrus.Logger) {
	loggerService := services.NewLoggerService(logger)
	loggerController := controllers.NewloggerController(loggerService)
	e.GET("/logger", loggerController.CheckLogger)
}
