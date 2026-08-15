package rest

import (
	"strconv"

	"github.com/labstack/echo/v5"

	"github.com/example/modular-monolith/internal/modules/product/domain"
	"github.com/example/modular-monolith/internal/shared/response"
)

type Handler struct {
	service domain.ProductService
}

func NewHandler(service domain.ProductService) *Handler {
	return &Handler{service: service}
}

func (h *Handler) Create(c *echo.Context) error {
	var req CreateProductRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}
	if msg := req.Validate(); msg != "" {
		return response.BadRequest(c, msg)
	}

	product, err := h.service.Create(c.Request().Context(), req.Name, req.Description, req.Price, req.Category)
	if err != nil {
		return response.InternalError(c, err.Error())
	}
	return response.Created(c, toProductResponse(product))
}

func (h *Handler) GetByID(c *echo.Context) error {
	id := c.Param("id")
	product, err := h.service.GetByID(c.Request().Context(), id)
	if err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, toProductResponse(product))
}

func (h *Handler) List(c *echo.Context) error {
	page, _ := strconv.Atoi(c.QueryParam("page"))
	limit, _ := strconv.Atoi(c.QueryParam("limit"))
	category := c.QueryParam("category")

	products, total, err := h.service.List(c.Request().Context(), category, page, limit)
	if err != nil {
		return response.InternalError(c, err.Error())
	}

	if page < 1 {
		page = 1
	}
	if limit < 1 {
		limit = 10
	}
	return response.Paginated(c, toProductListResponse(products), total, page, limit)
}

func (h *Handler) Update(c *echo.Context) error {
	id := c.Param("id")
	var req UpdateProductRequest
	if err := c.Bind(&req); err != nil {
		return response.BadRequest(c, "invalid request body")
	}

	product, err := h.service.Update(c.Request().Context(), id, req.Name, req.Description, req.Price, req.Category)
	if err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, toProductResponse(product))
}

func (h *Handler) Delete(c *echo.Context) error {
	id := c.Param("id")
	if err := h.service.Delete(c.Request().Context(), id); err != nil {
		return response.NotFound(c, err.Error())
	}
	return response.OK(c, map[string]string{"message": "product deleted"})
}
