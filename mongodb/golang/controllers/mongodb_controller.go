package controllers

import (
	modelrequests "note-golang-mongodb/models/requests"
	modelresponses "note-golang-mongodb/models/responses"
	"note-golang-mongodb/services"

	"github.com/labstack/echo/v4"
)

type MongodbController interface {
	Create(c echo.Context) error
	Get(c echo.Context) error
	GetById(c echo.Context) error
	UpdateOne(c echo.Context) error
	UpdateById(c echo.Context) error
	DeleteOne(c echo.Context) error
}

type mongodbController struct {
	MongodbService services.MongodbService
}

func NewMongodbController(mongodbService services.MongodbService) MongodbController {
	return &mongodbController{
		MongodbService: mongodbService,
	}
}

func (controller *mongodbController) Create(c echo.Context) error {
	var createRequest modelrequests.CreateRequest
	err := c.Bind(&createRequest)
	if err != nil {
		response := modelresponses.SetBadRequestResponse(err.Error())
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.MongodbService.Create(c.Request().Context(), createRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *mongodbController) Get(c echo.Context) error {
	test := c.QueryParam("test")
	response := controller.MongodbService.Get(c.Request().Context(), test)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *mongodbController) GetById(c echo.Context) error {
	id := c.Param("id")
	response := controller.MongodbService.GetById(c.Request().Context(), id)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *mongodbController) UpdateOne(c echo.Context) error {
	var updateRequest modelrequests.UpdateRequest
	err := c.Bind(&updateRequest)
	if err != nil {
		response := modelresponses.SetBadRequestResponse(err.Error())
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.MongodbService.UpdateById(c.Request().Context(), updateRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *mongodbController) UpdateById(c echo.Context) error {
	var updateRequest modelrequests.UpdateRequest
	err := c.Bind(&updateRequest)
	if err != nil {
		response := modelresponses.SetBadRequestResponse(err.Error())
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.MongodbService.UpdateById(c.Request().Context(), updateRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *mongodbController) DeleteOne(c echo.Context) error {
	var deleteRequest modelrequests.DeleteRequest
	err := c.Bind(&deleteRequest)
	if err != nil {
		response := modelresponses.SetBadRequestResponse(err.Error())
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.MongodbService.DeleteOne(c.Request().Context(), deleteRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}
