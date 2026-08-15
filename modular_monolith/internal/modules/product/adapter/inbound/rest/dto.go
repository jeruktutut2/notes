package rest

import (
	"time"

	"github.com/example/modular-monolith/internal/modules/product/domain"
)

// --- Request DTOs ---

type CreateProductRequest struct {
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Price       float64 `json:"price"`
	Category    string  `json:"category"`
}

func (r *CreateProductRequest) Validate() string {
	if r.Name == "" {
		return "name is required"
	}
	if r.Price < 0 {
		return "price must be non-negative"
	}
	return ""
}

type UpdateProductRequest struct {
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Price       float64 `json:"price"`
	Category    string  `json:"category"`
}

// --- Response DTOs ---

type ProductResponse struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Price       float64   `json:"price"`
	Category    string    `json:"category"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

func toProductResponse(p *domain.Product) *ProductResponse {
	if p == nil {
		return nil
	}
	return &ProductResponse{
		ID:          p.ID,
		Name:        p.Name,
		Description: p.Description,
		Price:       p.Price,
		Category:    p.Category,
		CreatedAt:   p.CreatedAt,
		UpdatedAt:   p.UpdatedAt,
	}
}

func toProductListResponse(products []*domain.Product) []*ProductResponse {
	result := make([]*ProductResponse, len(products))
	for i, p := range products {
		result[i] = toProductResponse(p)
	}
	return result
}
