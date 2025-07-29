package routes

import (
	"note-pdf-golang/controllers"
	"note-pdf-golang/services"

	"github.com/labstack/echo/v4"
)

func SetPdfRoute(e *echo.Echo) {
	pdfService := services.NewPdfService()
	pdfController := controllers.NewPdfController(pdfService)
	e.GET("/pdf", pdfController.GetPdf)
}
