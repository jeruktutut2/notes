package domain

import "time"

// Inventory represents the inventory domain entity.
type Inventory struct {
	ID        string
	ProductID string
	Quantity  int
	Reserved  int
	Available int // calculated: quantity - reserved
	UpdatedAt time.Time
}
