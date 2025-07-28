package routes

import (
	"note-array-golang/controllers"
	"note-array-golang/services"

	"github.com/labstack/echo/v4"
)

func SetArrayRoute(e *echo.Echo) {
	arrayService := services.NewArrayService()
	arrayController := controllers.NewArrayController(arrayService)
	e.GET("/algoruthm-dutch-national-flag", arrayController.DutchNationalFlagAlgorithm)
	e.GET("/algorithm-kadanes", arrayController.KadanesAlgorithm)
	e.GET("/algorithm-metric-array1", arrayController.MetricArray1)
	e.GET("/algorithm-metric-array2", arrayController.MetricArray2)
	e.GET("/algorithm-multiply-matrix", arrayController.MultiplyMatrix)
	e.GET("/range-sum-array", arrayController.RangeSumArray)
	e.GET("/range-with-update-array", arrayController.RangeWithUpdateArray)
	e.GET("/rearrange-array", arrayController.RearrangeArray)
	e.GET("/reverse-array", arrayController.ReverseArray)
	e.GET("/rotation-array", arrayController.RotationArray)
}
