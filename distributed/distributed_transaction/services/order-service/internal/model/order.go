package model

import "time"

// Order status constants - menunjukkan state saga saat ini
const (
	OrderStatusPending           = "PENDING"            // Order baru dibuat
	OrderStatusInventoryReserved = "INVENTORY_RESERVED" // Stok direserve
	OrderStatusPaymentCompleted  = "PAYMENT_COMPLETED"  // Payment berhasil
	OrderStatusCompleted         = "COMPLETED"          // Saga complete
	OrderStatusFailed            = "FAILED"             // Saga failed
)

// Order represents an order in the system
type Order struct {
	ID            string    `json:"id"`
	CustomerName  string    `json:"customer_name"`
	ProductID     string    `json:"product_id"`
	Quantity      int       `json:"quantity"`
	TotalPrice    float64   `json:"total_price"`
	Status        string    `json:"status"`
	FailureReason string    `json:"failure_reason,omitempty"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

// CreateOrderRequest represents the request body for creating an order
type CreateOrderRequest struct {
	CustomerName string  `json:"customer_name" validate:"required"`
	ProductID    string  `json:"product_id" validate:"required"`
	Quantity     int     `json:"quantity" validate:"required,gt=0"`
	TotalPrice   float64 `json:"total_price" validate:"required,gt=0"`
}
