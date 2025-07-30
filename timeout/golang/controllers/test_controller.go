package controllers

import (
	"context"
	"net/http"
	"time"
	"timeout/services"

	"github.com/labstack/echo/v4"
)

type TestController interface {
	Test1WithTx(c echo.Context) error
	Test1WithoutTx(c echo.Context) error
	ChangeTimeout(c echo.Context) error
}

type testController struct {
	TestService services.TestService
}

func NewTestController(testService services.TestService) TestController {
	return &testController{
		TestService: testService,
	}
}

func (controller *testController) Test1WithTx(c echo.Context) error {
	result := controller.TestService.TestWithTx(c.Request().Context())
	return c.JSON(http.StatusOK, map[string]interface{}{
		"key": result,
	})
}

func (controller *testController) Test1WithoutTx(c echo.Context) error {
	result := controller.TestService.TestWithoutTx(c.Request().Context())
	return c.JSON(http.StatusOK, map[string]interface{}{
		"key": result,
	})
}

func (controller *testController) ChangeTimeout(c echo.Context) error {
	ctx, cancel := context.WithTimeout(c.Request().Context(), time.Duration(2)*time.Second)
	defer cancel()
	result := controller.TestService.TestWithTx(ctx)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"key": result,
	})
}
