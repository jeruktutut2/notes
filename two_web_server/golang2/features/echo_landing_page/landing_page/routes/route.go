package routes

import (
	"golang2-note-two-web-server/commons/middlewares"
	"golang2-note-two-web-server/features/echo_landing_page/landing_page/controllers"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	echoController := controllers.NewEchoController()
	e.GET("/echo/landing-page", echoController.LandingPage, middlewares.EchoExampleMiddleware)
}
