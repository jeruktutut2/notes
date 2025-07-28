package controllers

import (
	"net/http"
	"note-array-golang/services"

	"github.com/labstack/echo/v4"
)

type ArrayController interface {
	ReverseArray(c echo.Context) error
	RotationArray(c echo.Context) error
	RearrangeArray(c echo.Context) error
	RangeSumArray(c echo.Context) error
	RangeWithUpdateArray(c echo.Context) error
	// sparsetable pending
	MetricArray1(c echo.Context) error
	MetricArray2(c echo.Context) error
	MultiplyMatrix(c echo.Context) error
	KadanesAlgorithm(c echo.Context) error
	DutchNationalFlagAlgorithm(c echo.Context) error
}

type arrayController struct {
	ArrayService services.ArrayService
}

func NewArrayController(arrayService services.ArrayService) ArrayController {
	return &arrayController{
		ArrayService: arrayService,
	}
}

func (controller *arrayController) ReverseArray(c echo.Context) error {
	arr := controller.ArrayService.ReverseArray()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) RotationArray(c echo.Context) error {
	arr := controller.ArrayService.RotationArray()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) RearrangeArray(c echo.Context) error {
	arr := controller.ArrayService.RearrangeArray()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) RangeSumArray(c echo.Context) error {
	arr := controller.ArrayService.RangeSumArray()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) RangeWithUpdateArray(c echo.Context) error {
	arr := controller.ArrayService.RangeWithUpdateArray()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) MetricArray1(c echo.Context) error {
	arr := controller.ArrayService.MetricArray1()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) MetricArray2(c echo.Context) error {
	arr := controller.ArrayService.MetricArray2()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) MultiplyMatrix(c echo.Context) error {
	arr := controller.ArrayService.MultiplyMatrix()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *arrayController) KadanesAlgorithm(c echo.Context) error {
	result := controller.ArrayService.KadanesAlgorithm()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": result,
	})
}

func (controller *arrayController) DutchNationalFlagAlgorithm(c echo.Context) error {
	arr := controller.ArrayService.DutchNationalFlagAlgorithm()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}
