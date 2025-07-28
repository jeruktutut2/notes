package routes

import (
	"note-linked-list-golang/controllers"
	"note-linked-list-golang/services"

	"github.com/labstack/echo/v4"
)

func SetLinkedListRoute(e *echo.Echo) {
	linkedListService := services.NewLinkedListService()
	linkedListController := controllers.NewLinkedListController(linkedListService)
	e.GET("/singly-linked-list", linkedListController.Singly)
}
