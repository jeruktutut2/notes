package controllers

import (
	"net/http"
	modelrequests "note-golang-millisecond/models/requests"
	"note-golang-millisecond/services"

	"github.com/labstack/echo/v4"
)

type MillisecondController interface {
	GetByGmtPlus8(c echo.Context) error
	GetByGmtMinus8(c echo.Context) error
}

type millisecondController struct {
	millisecondService services.MillisecondService
}

func NewMillisecondController(millisecondService services.MillisecondService) MillisecondController {
	return &millisecondController{
		millisecondService: millisecondService,
	}
}

func (controller *millisecondController) GetByGmtPlus8(c echo.Context) error {
	var millisecondRequest modelrequests.MillisecondRequest
	err := c.Bind(&millisecondRequest)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"response": err.Error(),
		})
	}
	response := controller.millisecondService.GetByGMTPlus8(c.Request().Context(), millisecondRequest)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}

func (controller *millisecondController) GetByGmtMinus8(c echo.Context) error {
	var millisecondRequest modelrequests.MillisecondRequest
	err := c.Bind(&millisecondRequest)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"response": err.Error(),
		})
	}
	response := controller.millisecondService.GetByGMTMinus8(c.Request().Context(), millisecondRequest)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}
