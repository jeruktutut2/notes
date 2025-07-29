package routes

import (
	"note-golang-millisecond/controllers"
	"note-golang-millisecond/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	millisecondService := services.NewMillisecondService()
	millisecondController := controllers.NewMillisecondController(millisecondService)
	e.GET("/millisecond/plus8", millisecondController.GetByGmtPlus8)
	e.GET("/millisecond/minus8", millisecondController.GetByGmtMinus8)
}
