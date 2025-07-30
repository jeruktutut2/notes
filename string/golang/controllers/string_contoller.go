package controllers

import (
	"net/http"
	"note-string-golang/services"

	"github.com/labstack/echo/v4"
)

type StringController interface {
	Substring2(c echo.Context) error
	Substring1(c echo.Context) error
	Subsequence1(c echo.Context) error
	Subsequence2(c echo.Context) error
	Rotation(c echo.Context) error
	BinaryString(c echo.Context) error
	Palindrome(c echo.Context) error
	LexicographicRankString(c echo.Context) error
	PatternSearching(c echo.Context) error
}

type stringController struct {
	StringService services.StringService
}

func NewStringController(stringService services.StringService) StringController {
	return &stringController{
		StringService: stringService,
	}
}

func (controller *stringController) Substring1(c echo.Context) error {
	numberOfContain := controller.StringService.Substring1()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": numberOfContain,
	})
}

func (controller *stringController) Substring2(c echo.Context) error {
	arr := controller.StringService.Substring2()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *stringController) Subsequence1(c echo.Context) error {
	arr := controller.StringService.Subsequence1()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}

func (controller *stringController) Subsequence2(c echo.Context) error {
	gks := controller.StringService.Subsequence2()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": gks,
	})
}

func (controller *stringController) Rotation(c echo.Context) error {
	srotation := controller.StringService.Rotation()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": srotation,
	})
}

func (controller *stringController) BinaryString(c echo.Context) error {
	s := controller.StringService.BinaryString()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": s,
	})
}

func (controller *stringController) Palindrome(c echo.Context) error {
	s := controller.StringService.Palindrome()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": s,
	})
}

func (controller *stringController) LexicographicRankString(c echo.Context) error {
	rank := controller.StringService.LexicographicRackString()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": rank,
	})
}

func (controller *stringController) PatternSearching(c echo.Context) error {
	arr := controller.StringService.PatternSearching()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": arr,
	})
}
