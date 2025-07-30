package routes

import (
	"golang-note-two-web-server/features/echo_landing_page/landing_page/controllers"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	echoController := controllers.NewEchoController()
	e.GET("/echo/landing-page", echoController.LandingPage)
}
