package controllers

import (
	"net/http"
	"note-golang-fiberv3-timeout/services"

	"github.com/gofiber/fiber/v3"
)

type TestController interface {
	Test1WithTx(c fiber.Ctx) error
	Test1WithoutTx(c fiber.Ctx) error
}

type testController struct {
	TestService services.TestService
}

func NewTestController(testService services.TestService) TestController {
	return &testController{
		TestService: testService,
	}
}

func (controller *testController) Test1WithTx(c fiber.Ctx) error {
	result := controller.TestService.TestWithTx(c.RequestCtx())
	return c.Status(http.StatusOK).JSON(fiber.Map{
		"respnose": result,
	})
}

func (controller *testController) Test1WithoutTx(c fiber.Ctx) error {
	result := controller.TestService.TestWithoutTx(c.RequestCtx())
	return c.Status(http.StatusOK).JSON(fiber.Map{
		"response": result,
	})
}
