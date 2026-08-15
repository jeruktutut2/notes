package model

import "time"

// Product represents a product with stock management
type Product struct {
	ID            string    `json:"id"`
	Name          string    `json:"name"`
	Stock         int       `json:"stock"`          // Stok yang tersedia
	ReservedStock int       `json:"reserved_stock"` // Stok yang sedang di-reserve oleh saga
	Price         float64   `json:"price"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

// AvailableStock returns the actual available stock (stock - reserved)
func (p *Product) AvailableStock() int {
	return p.Stock - p.ReservedStock
}

const (
	ActionReserve = "RESERVE" // Stok di-reserve saat order masuk
	ActionRelease = "RELEASE" // Stok di-release saat compensation
	ActionDeduct  = "DEDUCT"  // Stok di-deduct saat order complete
)

// InventoryLog records all inventory changes for audit trail
type InventoryLog struct {
	ID        string    `json:"id"`
	OrderID   string    `json:"order_id"`
	ProductID string    `json:"product_id"`
	Quantity  int       `json:"quantity"`
	Action    string    `json:"action"`
	CreatedAt time.Time `json:"created_at"`
}

// CreateProductRequest for REST API
type CreateProductRequest struct {
	Name  string  `json:"name"`
	Stock int     `json:"stock"`
	Price float64 `json:"price"`
}
