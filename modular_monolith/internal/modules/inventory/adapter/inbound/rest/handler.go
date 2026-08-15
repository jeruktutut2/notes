package rest

import (
	"strconv"

	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/inventory/domain"
	"github.com/example/modular-monolith/internal/shared/response"
)

type Handler struct {
	service domain.InventoryService
}

func NewHandler(service domain.InventoryService) *Handler {
	return &Handler{service: service}
}

func (h *Handler) Create(c *echo.Context) error {
	var req CreateInventoryRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}
	if msg := req.Validate(); msg != "" {
		return response.BadRequest(c, msg)
	}

	inv, err := h.service.Create(c.Request().Context(), req.ProductID, req.Quantity)
	if err != nil {
		return response.InternalError(c, err.Error())
	}
	return response.Created(c, toInventoryResponse(inv))
}

func (h *Handler) GetByProductID(c *echo.Context) error {
	productID := c.Param("product_id")
	inv, err := h.service.GetByProductID(c.Request().Context(), productID)
	if err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, toInventoryResponse(inv))
}

func (h *Handler) List(c *echo.Context) error {
	page, _ := strconv.Atoi(c.QueryParam("page"))
	limit, _ := strconv.Atoi(c.QueryParam("limit"))

	items, total, err := h.service.List(c.Request().Context(), page, limit)
	if err != nil {
		return response.InternalError(c, err.Error())
	}

	if page < 1 {
		page = 1
	}
	if limit < 1 {
		limit = 10
	}
	return response.Paginated(c, toInventoryListResponse(items), total, page, limit)
}

func (h *Handler) Adjust(c *echo.Context) error {
	productID := c.Param("product_id")
	var req AdjustInventoryRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}
	if msg := req.Validate(); msg != "" {
		return response.BadRequest(c, msg)
	}

	inv, err := h.service.Adjust(c.Request().Context(), productID, req.Adjustment, req.Reason)
	if err != nil {
		return response.BadRequest(c, err.Error())
	}
	return response.OK(c, toInventoryResponse(inv))
}
