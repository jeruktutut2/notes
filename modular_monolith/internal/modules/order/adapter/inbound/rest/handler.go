package rest

import (
	"strconv"

	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/order/domain"
	"github.com/example/modular-monolith/internal/shared/response"
)

type Handler struct {
	service domain.OrderService
}

func NewHandler(service domain.OrderService) *Handler {
	return &Handler{service: service}
}

func (h *Handler) Create(c *echo.Context) error {
	var req CreateOrderRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}
	if msg := req.Validate(); msg != "" {
		return response.BadRequest(c, msg)
	}

	order, err := h.service.Create(c.Request().Context(), req.UserID, req.toDomainItems())
	if err != nil {
		return response.InternalError(c, err.Error())
	}
	return response.Created(c, toOrderResponse(order))
}

func (h *Handler) GetByID(c *echo.Context) error {
	id := c.Param("id")
	order, err := h.service.GetByID(c.Request().Context(), id)
	if err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, toOrderResponse(order))
}

func (h *Handler) List(c *echo.Context) error {
	page, _ := strconv.Atoi(c.QueryParam("page"))
	limit, _ := strconv.Atoi(c.QueryParam("limit"))
	userID := c.QueryParam("user_id")

	orders, total, err := h.service.List(c.Request().Context(), userID, page, limit)
	if err != nil {
		return response.InternalError(c, err.Error())
	}

	if page < 1 {
		page = 1
	}
	if limit < 1 {
		limit = 10
	}
	return response.Paginated(c, toOrderListResponse(orders), total, page, limit)
}

func (h *Handler) UpdateStatus(c *echo.Context) error {
	id := c.Param("id")
	var req UpdateOrderStatusRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}
	if msg := req.Validate(); msg != "" {
		return response.BadRequest(c, msg)
	}

	if err := h.service.UpdateStatus(c.Request().Context(), id, req.Status); err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, map[string]string{"message": "order status updated"})
}
