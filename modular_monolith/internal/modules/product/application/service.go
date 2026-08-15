package application

import (
	"context"
	"fmt"

	"go.opentelemetry.io/otel"

	"github.com/example/modular-monolith/internal/modules/product/domain"
)

var tracer = otel.Tracer("module.product")

type service struct {
	repo domain.ProductRepository
}

// NewService creates a new product application service.
func NewService(repo domain.ProductRepository) domain.ProductService {
	return &service{repo: repo}
}

func (s *service) Create(ctx context.Context, name, description string, price float64, category string) (*domain.Product, error) {
	ctx, span := tracer.Start(ctx, "ProductService.Create")
	defer span.End()

	p := &domain.Product{
		Name:        name,
		Description: description,
		Price:       price,
		Category:    category,
	}

	if err := s.repo.Create(ctx, p); err != nil {
		return nil, fmt.Errorf("failed to create product: %w", err)
	}
	return p, nil
}

func (s *service) GetByID(ctx context.Context, id string) (*domain.Product, error) {
	ctx, span := tracer.Start(ctx, "ProductService.GetByID")
	defer span.End()

	return s.repo.GetByID(ctx, id)
}

func (s *service) List(ctx context.Context, category string, page, limit int) ([]*domain.Product, int64, error) {
	ctx, span := tracer.Start(ctx, "ProductService.List")
	defer span.End()

	if page < 1 {
		page = 1
	}
	if limit < 1 || limit > 100 {
		limit = 10
	}
	offset := (page - 1) * limit
	return s.repo.List(ctx, category, limit, offset)
}

func (s *service) Update(ctx context.Context, id, name, description string, price float64, category string) (*domain.Product, error) {
	ctx, span := tracer.Start(ctx, "ProductService.Update")
	defer span.End()

	p, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	if name != "" {
		p.Name = name
	}
	if description != "" {
		p.Description = description
	}
	if price > 0 {
		p.Price = price
	}
	if category != "" {
		p.Category = category
	}

	if err := s.repo.Update(ctx, p); err != nil {
		return nil, fmt.Errorf("failed to update product: %w", err)
	}
	return p, nil
}

func (s *service) Delete(ctx context.Context, id string) error {
	ctx, span := tracer.Start(ctx, "ProductService.Delete")
	defer span.End()

	return s.repo.Delete(ctx, id)
}
