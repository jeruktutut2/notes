package controllers

import (
	"golang2-note-pdf/services"
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
)

type FileController interface {
	ShowPdf(c echo.Context) error
	DownloadPdf(c echo.Context) error
	StreamPdf(c echo.Context) error
}

type fileController struct {
	fileService services.FileService
}

func NewFileController(fileService services.FileService) FileController {
	return &fileController{
		fileService: fileService,
	}
}

func (controller *fileController) ShowPdf(c echo.Context) error {
	response := controller.fileService.GeneratePdf(c.Request().Context())
	c.Response().Header().Set(echo.HeaderContentType, "application/pdf")
	c.Response().Header().Set("Content-Disposition", "inline; filename="+response)
	return c.File(response)
}

func (controller *fileController) DownloadPdf(c echo.Context) error {
	response := controller.fileService.GeneratePdf(c.Request().Context())
	c.Response().Header().Set(echo.HeaderContentType, "application/pdf")
	c.Response().Header().Set("Content-Disposition", "attachment; filename="+response)
	return c.File(response)
}

func (controller *fileController) StreamPdf(c echo.Context) error {
	response := controller.fileService.GeneratePdf(c.Request().Context())
	f, err := os.Open(response)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"response": err.Error(),
		})
	}
	c.Response().Header().Set(echo.HeaderContentType, "application/pdf")
	c.Response().Header().Set("Content-Disposition", "inline; filename="+response)
	return c.Stream(http.StatusOK, "application/pdf", f)
}
