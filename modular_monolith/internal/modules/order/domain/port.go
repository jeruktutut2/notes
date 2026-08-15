package domain

import "context"

// OrderRepository is the OUTBOUND PORT for order data persistence.
type OrderRepository interface {
	Create(ctx context.Context, o *Order) error
	GetByID(ctx context.Context, id string) (*Order, error)
	List(ctx context.Context, userID string, limit, offset int) ([]*Order, int64, error)
	UpdateStatus(ctx context.Context, id, status string) error
}

// OrderService is the INBOUND PORT defining use cases for orders.
type OrderService interface {
	Create(ctx context.Context, userID string, items []OrderItemInput) (*Order, error)
	GetByID(ctx context.Context, id string) (*Order, error)
	List(ctx context.Context, userID string, page, limit int) ([]*Order, int64, error)
	UpdateStatus(ctx context.Context, id, status string) error
}
