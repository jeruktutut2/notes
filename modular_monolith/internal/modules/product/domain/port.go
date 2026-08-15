package domain

import "context"

// ProductRepository is the OUTBOUND PORT for product data persistence.
type ProductRepository interface {
	Create(ctx context.Context, p *Product) error
	GetByID(ctx context.Context, id string) (*Product, error)
	List(ctx context.Context, category string, limit, offset int) ([]*Product, int64, error)
	Update(ctx context.Context, p *Product) error
	Delete(ctx context.Context, id string) error
}

// ProductService is the INBOUND PORT defining use cases for products.
type ProductService interface {
	Create(ctx context.Context, name, description string, price float64, category string) (*Product, error)
	GetByID(ctx context.Context, id string) (*Product, error)
	List(ctx context.Context, category string, page, limit int) ([]*Product, int64, error)
	Update(ctx context.Context, id, name, description string, price float64, category string) (*Product, error)
	Delete(ctx context.Context, id string) error
}
