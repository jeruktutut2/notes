package controllers

import (
	modelrequests "note-golang-mysql/models/requests"
	modelresponses "note-golang-mysql/models/responses"
	"note-golang-mysql/services"
	"strconv"

	"github.com/labstack/echo/v4"
)

type MysqlController interface {
	Create(c echo.Context) error
	Get(c echo.Context) error
	Update(c echo.Context) error
	Delete(c echo.Context) error
}

type mysqlController struct {
	MysqlService services.MysqlService
}

func NewMysqlController(mysqlService services.MysqlService) MysqlController {
	return &mysqlController{
		MysqlService: mysqlService,
	}
}

func (controller *mysqlController) Create(c echo.Context) error {
	var createRequest modelrequests.CreateRequest
	err := c.Bind(&createRequest)
	if err != nil {
		httpResponse := modelresponses.SetBadRequestResponse(err.Error())
		return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
	}

	httpResponse := controller.MysqlService.Create(c.Request().Context(), createRequest)

	return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
}

func (controller *mysqlController) Get(c echo.Context) error {
	idParam := c.Param("id")
	id, err := strconv.Atoi(idParam)
	if err != nil {
		httpResponse := modelresponses.SetInternalServerErrorResponse()
		return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
	}
	httpResponse := controller.MysqlService.Get(c.Request().Context(), id)
	return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
}

func (controller *mysqlController) Update(c echo.Context) error {
	var updateRequest modelrequests.UpdateRequest
	err := c.Bind(&updateRequest)
	if err != nil {
		httpResponse := modelresponses.SetInternalServerErrorResponse()
		return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
	}
	httpResponse := controller.MysqlService.Update(c.Request().Context(), updateRequest)
	return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
}

func (controller *mysqlController) Delete(c echo.Context) error {
	idParam := c.Param("id")
	id, err := strconv.Atoi(idParam)
	if err != nil {
		httpResponse := modelresponses.SetInternalServerErrorResponse()
		return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
	}
	httpResponse := controller.MysqlService.Delete(c.Request().Context(), id)
	return c.JSON(httpResponse.HttpStatusCode, httpResponse.BodyResponse)
}
