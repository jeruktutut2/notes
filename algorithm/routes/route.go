package routes

import (
	"note-algorithm-golang/controllers"
	"note-algorithm-golang/services"

	"github.com/labstack/echo/v4"
)

func SetAlgorithmRoute(e *echo.Echo) {
	algorithmService := services.NewAlgorithService()
	algorithmController := controllers.NewAlgorithmController(algorithmService)
	e.GET("/algoritm-binary-search", algorithmController.BinarySearch)
	e.GET("/algoruthm-interpolation-search", algorithmController.InterpolationSearch)
	e.GET("/algorithm-jump-search", algorithmController.JumpSearch)
	e.GET("/algorithm-linear-search", algorithmController.LinearSearch)
	e.GET("/algorithm-ternary-search", algorithmController.TernarySearch)
}
