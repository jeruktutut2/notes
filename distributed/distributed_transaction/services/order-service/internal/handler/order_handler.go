package handler

import (
	"net/http"

	"distributed-transaction/services/order-service/internal/model"
	"distributed-transaction/services/order-service/internal/service"

	"github.com/labstack/echo/v5"
)

// OrderHandler handles HTTP requests for orders
type OrderHandler struct {
	svc *service.OrderService
}

// NewOrderHandler creates a new OrderHandler
func NewOrderHandler(svc *service.OrderService) *OrderHandler {
	return &OrderHandler{svc: svc}
}

// RegisterRoutes registers order routes
func (h *OrderHandler) RegisterRoutes(e *echo.Echo) {
	e.POST("/orders", h.CreateOrder)
	e.GET("/orders/:id", h.GetOrder)
	e.GET("/orders", h.GetAllOrders)
}

// CreateOrder handles POST /orders
// Ini adalah entry point dari saga - membuat order baru dan memulai flow
func (h *OrderHandler) CreateOrder(c *echo.Context) error {
	var req model.CreateOrderRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Invalid request body",
		})
	}

	// Validasi sederhana
	if req.CustomerName == "" || req.ProductID == "" || req.Quantity <= 0 || req.TotalPrice <= 0 {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "customer_name, product_id, quantity (>0), and total_price (>0) are required",
		})
	}

	order, err := h.svc.CreateOrder(req)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
	}

	return c.JSON(http.StatusCreated, map[string]interface{}{
		"message": "Order created, saga started",
		"order":   order,
	})
}

// GetOrder handles GET /orders/:id
func (h *OrderHandler) GetOrder(c *echo.Context) error {
	id := c.Param("id")
	order, err := h.svc.GetOrder(id)
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{
			"error": "Order not found",
		})
	}
	return c.JSON(http.StatusOK, order)
}

// GetAllOrders handles GET /orders
func (h *OrderHandler) GetAllOrders(c *echo.Context) error {
	orders, err := h.svc.GetAllOrders()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
	}
	return c.JSON(http.StatusOK, orders)
}
