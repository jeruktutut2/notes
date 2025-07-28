package routes

import (
	"note-golang-memcached/controllers"
	"note-golang-memcached/services"
	"note-golang-memcached/utils"

	"github.com/labstack/echo/v4"
)

func SetMemcachedRoute(e *echo.Echo, memcachedUtil utils.MemcachedUtil) {
	memcachedService := services.NewMemcachedService(memcachedUtil)
	memcachedController := controllers.NewMemcachedController(memcachedService)
	e.POST("/api/v1/memcached", memcachedController.Set)
	e.GET("/api/v1/memcached/:id", memcachedController.Get)
	e.DELETE("/api/v1/memcached", memcachedController.Delete)
}
