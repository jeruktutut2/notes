package controllers

import (
	"net/http"
	modelrequests "note-golang-cockroachdb/models/requests"
	"note-golang-cockroachdb/services"

	"github.com/labstack/echo/v4"
)

type Test1Controller interface {
	Create(c echo.Context) error
	GetById(c echo.Context) error
	GetAll(c echo.Context) error
	Update(c echo.Context) error
	Delete(c echo.Context) error
}

type test1Controller struct {
	test1Service services.Test1Service
}

func NewTest1Controller(test1Service services.Test1Service) Test1Controller {
	return &test1Controller{
		test1Service: test1Service,
	}
}

func (controller *test1Controller) Create(c echo.Context) error {
	var createRequest modelrequests.CreateRequest
	err := c.Bind(&createRequest)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"response": err.Error(),
		})
	}
	response := controller.test1Service.Create(c.Request().Context(), createRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *test1Controller) GetById(c echo.Context) error {
	id := c.Param("id")
	response := controller.test1Service.GetById(c.Request().Context(), id)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *test1Controller) GetAll(c echo.Context) error {
	response := controller.test1Service.GetAll(c.Request().Context())
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *test1Controller) Update(c echo.Context) error {
	var updateRequest modelrequests.UpdateRequest
	err := c.Bind(&updateRequest)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"response": err.Error(),
		})
	}
	response := controller.test1Service.Update(c.Request().Context(), updateRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}

func (controller *test1Controller) Delete(c echo.Context) error {
	var deleteRequest modelrequests.DeleteRequest
	err := c.Bind(&deleteRequest)
	if err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"response": err.Error(),
		})
	}
	response := controller.test1Service.Delete(c.Request().Context(), deleteRequest)
	return c.JSON(response.HttpStatusCode, response.BodyResponse)
}
