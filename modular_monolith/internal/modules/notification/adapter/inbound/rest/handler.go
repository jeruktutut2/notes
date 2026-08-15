package rest

import (
	"strconv"

	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/notification/domain"
	"github.com/example/modular-monolith/internal/shared/response"
)

type Handler struct {
	service domain.NotificationService
}

func NewHandler(service domain.NotificationService) *Handler {
	return &Handler{service: service}
}

func (h *Handler) Create(c *echo.Context) error {
	var req CreateNotificationRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}
	if msg := req.Validate(); msg != "" {
		return response.BadRequest(c, msg)
	}

	notif, err := h.service.Create(c.Request().Context(), req.UserID, req.Title, req.Message)
	if err != nil {
		return response.InternalError(c, err.Error())
	}
	return response.Created(c, toNotificationResponse(notif))
}

func (h *Handler) GetByID(c *echo.Context) error {
	id := c.Param("id")
	notif, err := h.service.GetByID(c.Request().Context(), id)
	if err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, toNotificationResponse(notif))
}

func (h *Handler) List(c *echo.Context) error {
	userID := c.QueryParam("user_id")
	if userID == "" {
		return response.BadRequest(c, "user_id query parameter is required")
	}

	page, _ := strconv.Atoi(c.QueryParam("page"))
	limit, _ := strconv.Atoi(c.QueryParam("limit"))

	notifications, total, err := h.service.ListByUser(c.Request().Context(), userID, page, limit)
	if err != nil {
		return response.InternalError(c, err.Error())
	}

	if page < 1 {
		page = 1
	}
	if limit < 1 {
		limit = 10
	}
	return response.Paginated(c, toNotificationListResponse(notifications), total, page, limit)
}

func (h *Handler) MarkAsRead(c *echo.Context) error {
	id := c.Param("id")
	if err := h.service.MarkAsRead(c.Request().Context(), id); err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, map[string]string{"message": "notification marked as read"})
}
