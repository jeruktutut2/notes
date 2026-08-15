package domain

import "time"

// Product represents the product domain entity.
type Product struct {
	ID          string
	Name        string
	Description string
	Price       float64
	Category    string
	CreatedAt   time.Time
	UpdatedAt   time.Time
}
