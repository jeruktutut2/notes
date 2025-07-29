package routes

import (
	"note-golang-mongodb/controllers"
	"note-golang-mongodb/helpers"
	"note-golang-mongodb/repositories"
	"note-golang-mongodb/services"
	"note-golang-mongodb/utils"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo, mongoUtil utils.MongoUtil, uuidHelper helpers.UuidHelper) {
	mongodbRepository := repositories.NewMongodbRepository()
	mongodbService := services.NewMongodbService(mongoUtil, uuidHelper, mongodbRepository)
	mongodbController := controllers.NewMongodbController(mongodbService)
	e.POST("/api/v1/test1", mongodbController.Create)
	e.GET("/api/v1/test1/:id", mongodbController.GetById)
	e.PUT("/api/v1/test1", mongodbController.UpdateById)
	e.DELETE("/api/v1/test1", mongodbController.DeleteOne)
}
