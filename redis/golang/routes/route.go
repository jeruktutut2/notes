package routes

import (
	"note-golang-redis/controllers"

	"github.com/labstack/echo/v4"
)

func SetRedisRoute(e *echo.Echo, controller controllers.RedisController) {
	// e.POST("/api/v1/redis", controller.Set)
	// e.GET("/api/v1/redis/:id", controller.Get)
	// e.DELETE("/api/v1/redis", controller.Del)
	e.POST("/", controller.Set)
	e.GET("/:id", controller.Get)
	e.DELETE("/", controller.Del)
}
