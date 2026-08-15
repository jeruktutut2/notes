package handler

import (
	"net/http"

	"distributed-transaction/services/shipping-service/internal/service"

	"github.com/labstack/echo/v5"
)

type ShippingHandler struct {
	svc *service.ShippingService
}

func NewShippingHandler(svc *service.ShippingService) *ShippingHandler {
	return &ShippingHandler{svc: svc}
}

func (h *ShippingHandler) RegisterRoutes(e *echo.Echo) {
	e.GET("/shipments", h.GetAllShipments)
}

func (h *ShippingHandler) GetAllShipments(c *echo.Context) error {
	shipments, err := h.svc.GetAllShipments()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, shipments)
}
