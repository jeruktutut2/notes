package routes

import (
	"gateway/controllers"

	"github.com/labstack/echo/v4"
)

func SetRoute(e *echo.Echo) {
	proxyController := controllers.NewProxyController()
	e.GET("/cookie/set-remote1", proxyController.SetRemote1Cookie)
	e.GET("/cookie/set-remote2", proxyController.SetRemote2Cookie)
	e.GET("/assets/remoteEntry.js", proxyController.RemoteEntry)
	e.GET("/remote/remoteEntry.js", proxyController.RemoteEntry)
	e.GET("/remote/*", proxyController.RemoteEntry)
	e.GET("/assets/remote", proxyController.NotRemoteEntry)
	e.GET("/remoteEntry.js", proxyController.RemoteEntry)
	e.GET("/bundle", proxyController.Bundle)
}
