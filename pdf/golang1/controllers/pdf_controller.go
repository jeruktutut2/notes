package controllers

import (
	"fmt"
	"net/http"
	"note-pdf-golang/services"

	"github.com/labstack/echo/v4"
)

type PdfController interface {
	GetPdf(c echo.Context) error
}

type pdfController struct {
	PdfService services.PdfService
}

func NewPdfController(pdfService services.PdfService) PdfController {
	return &pdfController{
		PdfService: pdfService,
	}
}

func (controller *pdfController) GetPdf(c echo.Context) error {
	pdfBytes, err := controller.PdfService.GetPdf()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"response": err.Error(),
		})
	}
	c.Response().Header().Set("Content-Type", "application/pdf")
	c.Response().Header().Set("Content-Disposition", "attachment; filename=output.pdf")
	fmt.Println("pdfBytes.Bytes():", pdfBytes.Bytes())
	c.Response().Write(pdfBytes.Bytes())
	return nil
}
