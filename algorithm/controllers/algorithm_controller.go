package controllers

import (
	"net/http"
	"note-algorithm-golang/services"

	"github.com/labstack/echo/v4"
)

type AlgorithmController interface {
	LinearSearch(c echo.Context) error
	BinarySearch(c echo.Context) error
	InterpolationSearch(c echo.Context) error
	JumpSearch(c echo.Context) error
	TernarySearch(c echo.Context) error
}

type algorithmController struct {
	AlgorithmService services.AlgorithmService
}

func NewAlgorithmController(algorithmService services.AlgorithmService) AlgorithmController {
	return &algorithmController{
		AlgorithmService: algorithmService,
	}
}

func (controller *algorithmController) LinearSearch(c echo.Context) error {
	arrvalue := controller.AlgorithmService.LinearSearch()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arrvalue,
	})
}

func (controller *algorithmController) BinarySearch(c echo.Context) error {
	arrvalue := controller.AlgorithmService.BinarySearch()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arrvalue,
	})
}

func (controller *algorithmController) InterpolationSearch(c echo.Context) error {
	arrvalue := controller.AlgorithmService.InterpolationSearch()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arrvalue,
	})
}

func (controller *algorithmController) JumpSearch(c echo.Context) error {
	arrvalue := controller.AlgorithmService.JumpSearch()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arrvalue,
	})
}

func (controller *algorithmController) TernarySearch(c echo.Context) error {
	arrvalue := controller.AlgorithmService.TernarySearch()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arrvalue,
	})
}
