package routes

import (
	"note-golang-stacktrace/controllers"
	"note-golang-stacktrace/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	service := services.NewService()
	controller := controllers.NewController(service)
	e.GET("/", controller.CheckStacktrace)
}
