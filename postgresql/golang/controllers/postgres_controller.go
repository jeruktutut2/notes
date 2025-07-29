package controllers

import (
	modelrequests "note-golang-postgresql/models/requests"
	modelresponses "note-golang-postgresql/models/responses"
	"note-golang-postgresql/services"
	"strconv"

	"github.com/labstack/echo/v4"
)

type PostgresController interface {
	Create(c echo.Context) error
	Get(c echo.Context) error
	Update(c echo.Context) error
	Delete(c echo.Context) error
}

type postgresController struct {
	PostgresService services.PostgresService
}

func NewPostgresController(postgresService services.PostgresService) PostgresController {
	return &postgresController{
		PostgresService: postgresService,
	}
}

func (controller *postgresController) Create(c echo.Context) error {
	var createRequest modelrequests.CreateRequest
	err := c.Bind(&createRequest)
	if err != nil {
		response := modelresponses.SetBadRequestResponse("bad request")
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}

	response := controller.PostgresService.Create(c.Request().Context(), createRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *postgresController) Get(c echo.Context) error {
	idParam := c.Param("id")
	id, err := strconv.Atoi(idParam)
	if err != nil {
		response := modelresponses.SetInternalServerErrorResponse()
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.PostgresService.Get(c.Request().Context(), id)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *postgresController) Update(c echo.Context) error {
	var updateRequest modelrequests.UpdateRequest
	err := c.Bind(&updateRequest)
	if err != nil {
		response := modelresponses.SetInternalServerErrorResponse()
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.PostgresService.Update(c.Request().Context(), updateRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *postgresController) Delete(c echo.Context) error {
	// idParam := c.Param("id")
	// id, err := strconv.Atoi(idParam)
	// if err != nil {
	// 	response := modelresponses.SetInternalServerErrorResponse()
	// 	return c.JSON(response.HttpStatusCode, response.BodyResponse)
	// }
	var deleteRequest modelrequests.DeleteRequest
	err := c.Bind(&deleteRequest)
	if err != nil {
		response := modelresponses.SetInternalServerErrorResponse()
		return c.JSON(response.HttpStatusCode, response.BodyResponse)
	}
	response := controller.PostgresService.Delete(c.Request().Context(), deleteRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}
