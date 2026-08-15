package domain

import "time"

// Order represents the order domain entity.
type Order struct {
	ID          string
	UserID      string
	TotalAmount float64
	Status      string
	Items       []*OrderItem
	CreatedAt   time.Time
	UpdatedAt   time.Time
}

// OrderItem represents a line item within an order.
type OrderItem struct {
	ID        string
	OrderID   string
	ProductID string
	Quantity  int
	Price     float64
	CreatedAt time.Time
}

// OrderItemInput is a domain value object for creating order items.
// Used by the service port to accept item data without HTTP concerns.
type OrderItemInput struct {
	ProductID string
	Quantity  int
	Price     float64
}

// ValidStatuses defines all valid order status transitions.
var ValidStatuses = map[string]bool{
	"pending":    true,
	"confirmed":  true,
	"processing": true,
	"shipped":    true,
	"delivered":  true,
	"cancelled":  true,
}
