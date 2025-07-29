package routes

import (
	"golang-rsa/handlers"
	"golang-rsa/services"
	"golang-rsa/utils"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo, keyUtil utils.KeyUtil) {
	keyService := services.NewKeyServcie(keyUtil)
	keyHandler := handlers.NewKeyHandler(keyService)
	e.GET("/sign", keyHandler.Sign)
	e.GET("/verify", keyHandler.Verify)
}
