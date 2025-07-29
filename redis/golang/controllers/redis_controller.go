package controllers

import (
	modelrequests "note-golang-redis/models/requests"
	modelresponses "note-golang-redis/models/responses"
	"note-golang-redis/services"

	"github.com/labstack/echo/v4"
)

type RedisController interface {
	Set(c echo.Context) error
	Get(c echo.Context) error
	Del(c echo.Context) error
}

type redisController struct {
	RedisService services.RedisService
}

func NewRedisController(redisService services.RedisService) RedisController {
	return &redisController{
		RedisService: redisService,
	}
}

func (controller *redisController) Set(c echo.Context) error {
	var createRequest modelrequests.CreateRequest
	err := c.Bind(&createRequest)
	if err != nil {
		// httpResponse := modelresponses.SetHttpResponse(http.StatusBadRequest, nil, []modelresponses.Error{{Field: "message", Message: "bad request"}})
		response := modelresponses.SetBadRequestResponse(err.Error())
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.RedisService.Set(c.Request().Context(), createRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *redisController) Get(c echo.Context) error {
	id := c.Param("id")
	response := controller.RedisService.Get(c.Request().Context(), id)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *redisController) Del(c echo.Context) error {
	var deleteRequest modelrequests.DeleteRequest
	err := c.Bind(&deleteRequest)
	if err != nil {
		response := modelresponses.SetBadRequestResponse(err.Error())
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.RedisService.Del(c.Request().Context(), deleteRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}
