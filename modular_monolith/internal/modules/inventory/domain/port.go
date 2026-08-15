package domain

import "context"

// InventoryRepository is the OUTBOUND PORT for inventory data persistence.
type InventoryRepository interface {
	Create(ctx context.Context, inv *Inventory) error
	GetByProductID(ctx context.Context, productID string) (*Inventory, error)
	List(ctx context.Context, limit, offset int) ([]*Inventory, int64, error)
	AdjustQuantity(ctx context.Context, productID string, adjustment int) (*Inventory, error)
}

// InventoryService is the INBOUND PORT defining use cases for inventory.
type InventoryService interface {
	Create(ctx context.Context, productID string, quantity int) (*Inventory, error)
	GetByProductID(ctx context.Context, productID string) (*Inventory, error)
	List(ctx context.Context, page, limit int) ([]*Inventory, int64, error)
	Adjust(ctx context.Context, productID string, adjustment int, reason string) (*Inventory, error)
}
