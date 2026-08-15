package handler

import (
	"net/http"

	"distributed-transaction/services/inventory-service/internal/model"
	"distributed-transaction/services/inventory-service/internal/service"

	"github.com/labstack/echo/v5"
)

type InventoryHandler struct {
	svc *service.InventoryService
}

func NewInventoryHandler(svc *service.InventoryService) *InventoryHandler {
	return &InventoryHandler{svc: svc}
}

func (h *InventoryHandler) RegisterRoutes(e *echo.Echo) {
	e.GET("/products", h.GetAllProducts)
	e.POST("/products", h.CreateProduct)
}

// GetAllProducts handles GET /products
func (h *InventoryHandler) GetAllProducts(c *echo.Context) error {
	products, err := h.svc.GetAllProducts()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, products)
}

// CreateProduct handles POST /products
func (h *InventoryHandler) CreateProduct(c *echo.Context) error {
	var req model.CreateProductRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request body"})
	}

	product, err := h.svc.CreateProduct(req)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}

	return c.JSON(http.StatusCreated, product)
}
