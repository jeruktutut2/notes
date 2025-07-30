package routes

import (
	"golang-note-two-web-server/controllers"

	"github.com/julienschmidt/httprouter"
)

func SetHttprouterRoute(router *httprouter.Router, controller controllers.HttprouterController) {
	router.GET("/httprouter/landing-page", controller.LandingPage)
}
