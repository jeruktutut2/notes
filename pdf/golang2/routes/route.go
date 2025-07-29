package routes

import (
	"golang2-note-pdf/controllers"
	"golang2-note-pdf/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	fileService := services.NewFileService()
	fileController := controllers.NewFileController(fileService)
	e.GET("/file/show-pdf", fileController.ShowPdf)
	e.GET("/file/download-pdf", fileController.DownloadPdf)
	e.GET("/file/stream-pdf", fileController.StreamPdf)
}
