package routes

import (
	"golang-note-stream-video/controllers"
	"golang-note-stream-video/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	fileService := services.NewFileService()
	fileController := controllers.NewFileController(fileService)
	e.GET("/file/stream-video", fileController.Stream)
}
