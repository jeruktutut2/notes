package controllers

import (
	"net/http"
	"note-golang-memcached/services"

	"github.com/labstack/echo/v4"
)

type MemcachedController interface {
	Set(c echo.Context) error
	Get(c echo.Context) error
	Delete(c echo.Context) error
}

type memcachedController struct {
	MemcachedService services.MemcachedService
}

func NewMemcachedController(memcachedService services.MemcachedService) MemcachedController {
	return &memcachedController{
		MemcachedService: memcachedService,
	}
}

func (controller *memcachedController) Set(c echo.Context) error {
	key := c.QueryParam("key")
	value := c.QueryParam("value")
	response := controller.MemcachedService.Set(key, value)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}

func (controller *memcachedController) Get(c echo.Context) error {
	key := c.QueryParam("key")
	response := controller.MemcachedService.Get(key)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}

func (controller *memcachedController) Delete(c echo.Context) error {
	key := c.QueryParam("key")
	response := controller.MemcachedService.Delete(key)
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": response,
	})
}
