package routes

import (
	"note-golang-panic/controllers"
	"note-golang-panic/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	panicService := services.NewPanicService()
	panicController := controllers.NewPanicController(panicService)
	e.GET("/", panicController.CheckPanic)
}
