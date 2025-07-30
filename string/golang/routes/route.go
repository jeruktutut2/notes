package routes

import (
	"note-string-golang/controllers"
	"note-string-golang/services"

	"github.com/labstack/echo/v4"
)

func SetStringRoute(e *echo.Echo) {
	stringService := services.NewStringService()
	stringController := controllers.NewStringController(stringService)
	e.GET("/binary-string", stringController.BinaryString)
	e.GET("/lexicographic-rank-string", stringController.LexicographicRankString)
	e.GET("/palindrome", stringController.Palindrome)
	e.GET("/pattern-searching", stringController.PatternSearching)
	e.GET("/rotation", stringController.Rotation)
	e.GET("/subsequenec1", stringController.Subsequence1)
	e.GET("/subsequence2", stringController.Subsequence2)
	e.GET("/substring1", stringController.Substring1)
	e.GET("/substring2", stringController.Substring2)
}
