package handler

import (
	"net/http"

	"distributed-transaction/services/payment-service/internal/service"

	"github.com/labstack/echo/v5"
)

type PaymentHandler struct {
	svc *service.PaymentService
}

func NewPaymentHandler(svc *service.PaymentService) *PaymentHandler {
	return &PaymentHandler{svc: svc}
}

func (h *PaymentHandler) RegisterRoutes(e *echo.Echo) {
	e.GET("/payments", h.GetAllPayments)
}

// GetAllPayments handles GET /payments
func (h *PaymentHandler) GetAllPayments(c *echo.Context) error {
	payments, err := h.svc.GetAllPayments()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, payments)
}
