package rest

import (
	"time"

	"github.com/example/modular-monolith/internal/modules/order/domain"
)

// --- Request DTOs ---

type CreateOrderRequest struct {
	UserID string                   `json:"user_id"`
	Items  []*CreateOrderItemRequest `json:"items"`
}

type CreateOrderItemRequest struct {
	ProductID string  `json:"product_id"`
	Quantity  int     `json:"quantity"`
	Price     float64 `json:"price"`
}

func (r *CreateOrderRequest) Validate() string {
	if r.UserID == "" {
		return "user_id is required"
	}
	if len(r.Items) == 0 {
		return "at least one item is required"
	}
	for _, item := range r.Items {
		if item.ProductID == "" {
			return "product_id is required for all items"
		}
		if item.Quantity < 1 {
			return "quantity must be at least 1"
		}
		if item.Price < 0 {
			return "price must be non-negative"
		}
	}
	return ""
}

// toDomainItems maps HTTP DTOs to domain value objects.
func (r *CreateOrderRequest) toDomainItems() []domain.OrderItemInput {
	items := make([]domain.OrderItemInput, len(r.Items))
	for i, item := range r.Items {
		items[i] = domain.OrderItemInput{
			ProductID: item.ProductID,
			Quantity:  item.Quantity,
			Price:     item.Price,
		}
	}
	return items
}

type UpdateOrderStatusRequest struct {
	Status string `json:"status"`
}

func (r *UpdateOrderStatusRequest) Validate() string {
	if r.Status == "" {
		return "status is required"
	}
	if !domain.ValidStatuses[r.Status] {
		return "invalid status value"
	}
	return ""
}

// --- Response DTOs ---

type OrderResponse struct {
	ID          string              `json:"id"`
	UserID      string              `json:"user_id"`
	TotalAmount float64             `json:"total_amount"`
	Status      string              `json:"status"`
	Items       []*OrderItemResponse `json:"items,omitempty"`
	CreatedAt   time.Time           `json:"created_at"`
	UpdatedAt   time.Time           `json:"updated_at"`
}

type OrderItemResponse struct {
	ID        string    `json:"id"`
	OrderID   string    `json:"order_id"`
	ProductID string    `json:"product_id"`
	Quantity  int       `json:"quantity"`
	Price     float64   `json:"price"`
	CreatedAt time.Time `json:"created_at"`
}

func toOrderResponse(o *domain.Order) *OrderResponse {
	if o == nil {
		return nil
	}
	resp := &OrderResponse{
		ID:          o.ID,
		UserID:      o.UserID,
		TotalAmount: o.TotalAmount,
		Status:      o.Status,
		CreatedAt:   o.CreatedAt,
		UpdatedAt:   o.UpdatedAt,
	}
	for _, item := range o.Items {
		resp.Items = append(resp.Items, &OrderItemResponse{
			ID:        item.ID,
			OrderID:   item.OrderID,
			ProductID: item.ProductID,
			Quantity:  item.Quantity,
			Price:     item.Price,
			CreatedAt: item.CreatedAt,
		})
	}
	return resp
}

func toOrderListResponse(orders []*domain.Order) []*OrderResponse {
	result := make([]*OrderResponse, len(orders))
	for i, o := range orders {
		result[i] = toOrderResponse(o)
	}
	return result
}
