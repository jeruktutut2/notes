package routes

import (
	"golang-note-resumeable-upload/controllers"
	"golang-note-resumeable-upload/services"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	fileService := services.NewFileService()
	fileController := controllers.NewFileController(fileService)
	e.POST("/file/upload", fileController.Upload)
	e.POST("/file/merge", fileController.Merge)
	e.GET("/file/check-file/:fileId", fileController.CheckFile)
	e.POST("/file/upload-merge", fileController.UploadAndMerge)
}
