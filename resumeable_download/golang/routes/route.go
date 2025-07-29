package routes

import (
	"note-golang-resumeable-download/controllers"
	"note-golang-resumeable-download/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	fileService := services.NewFileService()
	fileController := controllers.NewFileController(fileService)
	e.GET("/file/stat", fileController.GetFileStat)
	e.GET("/file/download", fileController.Download)
}
