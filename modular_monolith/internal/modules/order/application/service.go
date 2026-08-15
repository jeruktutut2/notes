package application

import (
	"context"
	"fmt"

	"go.opentelemetry.io/otel"

	"github.com/example/modular-monolith/internal/modules/order/domain"
)

var tracer = otel.Tracer("module.order")

type service struct {
	repo domain.OrderRepository
}

func NewService(repo domain.OrderRepository) domain.OrderService {
	return &service{repo: repo}
}

func (s *service) Create(ctx context.Context, userID string, items []domain.OrderItemInput) (*domain.Order, error) {
	ctx, span := tracer.Start(ctx, "OrderService.Create")
	defer span.End()

	// Calculate total amount and build order items.
	var total float64
	var orderItems []*domain.OrderItem
	for _, ri := range items {
		total += ri.Price * float64(ri.Quantity)
		orderItems = append(orderItems, &domain.OrderItem{
			ProductID: ri.ProductID,
			Quantity:  ri.Quantity,
			Price:     ri.Price,
		})
	}

	o := &domain.Order{
		UserID:      userID,
		TotalAmount: total,
		Status:      "pending",
		Items:       orderItems,
	}

	if err := s.repo.Create(ctx, o); err != nil {
		return nil, fmt.Errorf("failed to create order: %w", err)
	}
	return o, nil
}

func (s *service) GetByID(ctx context.Context, id string) (*domain.Order, error) {
	ctx, span := tracer.Start(ctx, "OrderService.GetByID")
	defer span.End()

	return s.repo.GetByID(ctx, id)
}

func (s *service) List(ctx context.Context, userID string, page, limit int) ([]*domain.Order, int64, error) {
	ctx, span := tracer.Start(ctx, "OrderService.List")
	defer span.End()

	if page < 1 {
		page = 1
	}
	if limit < 1 || limit > 100 {
		limit = 10
	}
	offset := (page - 1) * limit
	return s.repo.List(ctx, userID, limit, offset)
}

func (s *service) UpdateStatus(ctx context.Context, id, status string) error {
	ctx, span := tracer.Start(ctx, "OrderService.UpdateStatus")
	defer span.End()

	return s.repo.UpdateStatus(ctx, id, status)
}
