package handler

import (
	"net/http"

	"distributed-transaction/services/notification-service/internal/service"

	"github.com/labstack/echo/v5"
)

type NotificationHandler struct {
	svc *service.NotificationService
}

func NewNotificationHandler(svc *service.NotificationService) *NotificationHandler {
	return &NotificationHandler{svc: svc}
}

func (h *NotificationHandler) RegisterRoutes(e *echo.Echo) {
	e.GET("/notifications", h.GetAllNotifications)
}

func (h *NotificationHandler) GetAllNotifications(c *echo.Context) error {
	notifications, err := h.svc.GetAllNotifications()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, notifications)
}
