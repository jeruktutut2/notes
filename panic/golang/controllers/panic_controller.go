package controllers

import (
	"net/http"

	"note-golang-panic/services"

	"github.com/labstack/echo/v4"
)

type PanicController interface {
	CheckPanic(c echo.Context) error
}

type panicController struct {
	panicService services.PanicService
}

func NewPanicController(panicService services.PanicService) PanicController {
	return &panicController{
		panicService: panicService,
	}
}

func (controller *panicController) CheckPanic(c echo.Context) error {
	response := controller.panicService.CheckPanic(c.Request().Context())
	return c.JSON(http.StatusOK, map[string]string{
		"response": response,
	})
}
