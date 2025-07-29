package routes

import (
	"golang-note-stream-audio/controllers"
	"golang-note-stream-audio/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	fileService := services.NewFileService()
	fileController := controllers.NewFileController(fileService)
	e.GET("/file/stream-audio", fileController.Stream)
}
