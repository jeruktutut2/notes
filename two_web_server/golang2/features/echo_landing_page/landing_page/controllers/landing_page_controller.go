package controllers

import (
	"fmt"
	"net/http"
	"time"

	"github.com/labstack/echo/v4"
)

type EchoController interface {
	LandingPage(c echo.Context) error
}

type echoController struct {
}

func NewEchoController() EchoController {
	return &echoController{}
}

func (controller *echoController) LandingPage(c echo.Context) error {
	fmt.Println("LandingPage EchoController")
	return c.JSON(http.StatusOK, map[string]string{
		"app":  "echo",
		"time": time.Now().String(),
	})
}
