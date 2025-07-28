package routes

import (
	"note-golang-cockroachdb/controllers"
	"note-golang-cockroachdb/repositories"
	"note-golang-cockroachdb/services"
	"note-golang-cockroachdb/utils"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo, cockroachDbUtil utils.CockroachDbUtil) {
	test1Repository := repositories.NewTest1Repository()
	test1Service := services.NewTest1Service(cockroachDbUtil, test1Repository)
	test1Controller := controllers.NewTest1Controller(test1Service)
	e.POST("/test1", test1Controller.Create)
	e.GET("/test1/:id", test1Controller.GetById)
	e.GET("/test1", test1Controller.GetAll)
	e.PUT("/test1", test1Controller.Update)
	e.DELETE("/test1", test1Controller.Delete)
}
