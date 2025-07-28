package controllers

import (
	"net/http"
	"note-linked-list-golang/services"

	"github.com/labstack/echo/v4"
)

type LinkedListController interface {
	Singly(c echo.Context) error
}

type linkedListController struct {
	LinkedListService services.LinkedListService
}

func NewLinkedListController(linkedListService services.LinkedListService) LinkedListController {
	return &linkedListController{
		LinkedListService: linkedListService,
	}
}

func (controller *linkedListController) Singly(c echo.Context) error {
	controller.LinkedListService.Singly()
	return c.JSON(http.StatusOK, map[string]interface{}{
		"response": "response",
	})
}
