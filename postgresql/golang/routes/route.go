package routes

import (
	"note-golang-postgresql/controllers"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo, controller controllers.PostgresController) {
	e.POST("/api/v1/test1", controller.Create)
	e.GET("/api/v1/test1/:id", controller.Get)
	e.PUT("/api/v1/test1", controller.Update)
	e.DELETE("/api/v1/test1", controller.Delete)
}
