package rest

import (
	"time"

	"github.com/example/modular-monolith/internal/modules/inventory/domain"
)

// --- Request DTOs ---

type CreateInventoryRequest struct {
	ProductID string `json:"product_id"`
	Quantity  int    `json:"quantity"`
}

func (r *CreateInventoryRequest) Validate() string {
	if r.ProductID == "" {
		return "product_id is required"
	}
	if r.Quantity < 0 {
		return "quantity must be non-negative"
	}
	return ""
}

type AdjustInventoryRequest struct {
	Adjustment int    `json:"adjustment"`
	Reason     string `json:"reason"`
}

func (r *AdjustInventoryRequest) Validate() string {
	if r.Adjustment == 0 {
		return "adjustment must be non-zero"
	}
	if r.Reason == "" {
		return "reason is required"
	}
	return ""
}

// --- Response DTOs ---

type InventoryResponse struct {
	ID        string    `json:"id"`
	ProductID string    `json:"product_id"`
	Quantity  int       `json:"quantity"`
	Reserved  int       `json:"reserved"`
	Available int       `json:"available"`
	UpdatedAt time.Time `json:"updated_at"`
}

func toInventoryResponse(inv *domain.Inventory) *InventoryResponse {
	if inv == nil {
		return nil
	}
	return &InventoryResponse{
		ID:        inv.ID,
		ProductID: inv.ProductID,
		Quantity:  inv.Quantity,
		Reserved:  inv.Reserved,
		Available: inv.Available,
		UpdatedAt: inv.UpdatedAt,
	}
}

func toInventoryListResponse(items []*domain.Inventory) []*InventoryResponse {
	result := make([]*InventoryResponse, len(items))
	for i, inv := range items {
		result[i] = toInventoryResponse(inv)
	}
	return result
}
