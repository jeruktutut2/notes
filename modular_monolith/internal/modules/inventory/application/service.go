package application

import (
	"context"
	"fmt"

	"go.opentelemetry.io/otel"

	"github.com/example/modular-monolith/internal/modules/inventory/domain"
)

var tracer = otel.Tracer("module.inventory")

type service struct {
	repo domain.InventoryRepository
}

func NewService(repo domain.InventoryRepository) domain.InventoryService {
	return &service{repo: repo}
}

func (s *service) Create(ctx context.Context, productID string, quantity int) (*domain.Inventory, error) {
	ctx, span := tracer.Start(ctx, "InventoryService.Create")
	defer span.End()

	inv := &domain.Inventory{
		ProductID: productID,
		Quantity:  quantity,
	}

	if err := s.repo.Create(ctx, inv); err != nil {
		return nil, fmt.Errorf("failed to create inventory: %w", err)
	}
	inv.Available = inv.Quantity - inv.Reserved
	return inv, nil
}

func (s *service) GetByProductID(ctx context.Context, productID string) (*domain.Inventory, error) {
	ctx, span := tracer.Start(ctx, "InventoryService.GetByProductID")
	defer span.End()

	return s.repo.GetByProductID(ctx, productID)
}

func (s *service) List(ctx context.Context, page, limit int) ([]*domain.Inventory, int64, error) {
	ctx, span := tracer.Start(ctx, "InventoryService.List")
	defer span.End()

	if page < 1 {
		page = 1
	}
	if limit < 1 || limit > 100 {
		limit = 10
	}
	offset := (page - 1) * limit
	return s.repo.List(ctx, limit, offset)
}

func (s *service) Adjust(ctx context.Context, productID string, adjustment int, reason string) (*domain.Inventory, error) {
	ctx, span := tracer.Start(ctx, "InventoryService.Adjust")
	defer span.End()

	// Check current stock to prevent negative quantities.
	current, err := s.repo.GetByProductID(ctx, productID)
	if err != nil {
		return nil, err
	}

	newQuantity := current.Quantity + adjustment
	if newQuantity < 0 {
		return nil, fmt.Errorf("insufficient stock: current=%d, adjustment=%d", current.Quantity, adjustment)
	}

	return s.repo.AdjustQuantity(ctx, productID, adjustment)
}
