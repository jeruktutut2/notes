package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/example/modular-monolith/internal/modules/product/domain"
)

type repository struct {
	pool *pgxpool.Pool
}

func NewRepository(pool *pgxpool.Pool) domain.ProductRepository {
	return &repository{pool: pool}
}

func (r *repository) Create(ctx context.Context, p *domain.Product) error {
	query := `
		INSERT INTO products (name, description, price, category)
		VALUES ($1, $2, $3, $4)
		RETURNING id, created_at, updated_at`

	return r.pool.QueryRow(ctx, query, p.Name, p.Description, p.Price, p.Category).
		Scan(&p.ID, &p.CreatedAt, &p.UpdatedAt)
}

func (r *repository) GetByID(ctx context.Context, id string) (*domain.Product, error) {
	query := `SELECT id, name, description, price, category, created_at, updated_at FROM products WHERE id = $1`

	p := &domain.Product{}
	err := r.pool.QueryRow(ctx, query, id).
		Scan(&p.ID, &p.Name, &p.Description, &p.Price, &p.Category, &p.CreatedAt, &p.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("product not found")
		}
		return nil, err
	}
	return p, nil
}

func (r *repository) List(ctx context.Context, category string, limit, offset int) ([]*domain.Product, int64, error) {
	var total int64
	var countQuery, listQuery string
	var countArgs, listArgs []interface{}

	if category != "" {
		countQuery = `SELECT COUNT(*) FROM products WHERE category = $1`
		countArgs = []interface{}{category}
		listQuery = `SELECT id, name, description, price, category, created_at, updated_at
			FROM products WHERE category = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3`
		listArgs = []interface{}{category, limit, offset}
	} else {
		countQuery = `SELECT COUNT(*) FROM products`
		listQuery = `SELECT id, name, description, price, category, created_at, updated_at
			FROM products ORDER BY created_at DESC LIMIT $1 OFFSET $2`
		listArgs = []interface{}{limit, offset}
	}

	err := r.pool.QueryRow(ctx, countQuery, countArgs...).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	rows, err := r.pool.Query(ctx, listQuery, listArgs...)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var products []*domain.Product
	for rows.Next() {
		p := &domain.Product{}
		if err := rows.Scan(&p.ID, &p.Name, &p.Description, &p.Price, &p.Category, &p.CreatedAt, &p.UpdatedAt); err != nil {
			return nil, 0, err
		}
		products = append(products, p)
	}
	return products, total, rows.Err()
}

func (r *repository) Update(ctx context.Context, p *domain.Product) error {
	query := `
		UPDATE products SET name = $1, description = $2, price = $3, category = $4, updated_at = NOW()
		WHERE id = $5
		RETURNING updated_at`

	return r.pool.QueryRow(ctx, query, p.Name, p.Description, p.Price, p.Category, p.ID).
		Scan(&p.UpdatedAt)
}

func (r *repository) Delete(ctx context.Context, id string) error {
	result, err := r.pool.Exec(ctx, `DELETE FROM products WHERE id = $1`, id)
	if err != nil {
		return err
	}
	if result.RowsAffected() == 0 {
		return fmt.Errorf("product not found")
	}
	return nil
}
