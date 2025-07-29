package controllers

import (
	"golang-note-stream-audio/services"

	"github.com/labstack/echo/v4"
)

type FileController interface {
	Stream(c echo.Context) error
}

type fileController struct {
	fileService services.FileService
}

func NewFileController(fileService services.FileService) FileController {
	return &fileController{
		fileService: fileService,
	}
}

func (controller *fileController) Stream(c echo.Context) error {
	rangeHeader := c.Request().Header.Get("Range")
	httpStatusCode, response := controller.fileService.Stream(c.Response(), rangeHeader)
	return c.JSON(httpStatusCode, response)
}
