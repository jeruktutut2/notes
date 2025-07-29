package controllers

import (
	"note-golang-resumeable-download/services"

	"github.com/labstack/echo/v4"
)

type FileController interface {
	GetFileStat(c echo.Context) error
	Download(c echo.Context) error
}

type fileController struct {
	fileService services.FileService
}

func NewFileController(fileService services.FileService) FileController {
	return &fileController{
		fileService: fileService,
	}
}

func (controller *fileController) GetFileStat(c echo.Context) error {
	httpStatusCode, response := controller.fileService.GetFileStat()
	return c.JSON(httpStatusCode, response)
}

func (controller *fileController) Download(c echo.Context) error {
	rangeHeader := c.Request().Header.Get("Range")
	httpStatusCpde, response := controller.fileService.Download(c.Response(), rangeHeader)
	return c.JSON(httpStatusCpde, response)
}
