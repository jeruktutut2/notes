package routes

import (
	"golang2-note-two-web-server/controllers"
	"golang2-note-two-web-server/middlewares"

	"github.com/julienschmidt/httprouter"
)

func SetHttprouterRoute(router *httprouter.Router, controller controllers.HttprouterController) {
	router.GET("/httprouter/landing-page", middlewares.MultiMiddleware(controller.LandingPage, middlewares.HttprouterExampleMiddleware))
}
