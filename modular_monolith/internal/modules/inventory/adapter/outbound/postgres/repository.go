package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/example/modular-monolith/internal/modules/inventory/domain"
)

type repository struct {
	pool *pgxpool.Pool
}

func NewRepository(pool *pgxpool.Pool) domain.InventoryRepository {
	return &repository{pool: pool}
}

func (r *repository) Create(ctx context.Context, inv *domain.Inventory) error {
	query := `
		INSERT INTO inventory (product_id, quantity, reserved)
		VALUES ($1, $2, 0)
		RETURNING id, updated_at`

	return r.pool.QueryRow(ctx, query, inv.ProductID, inv.Quantity).
		Scan(&inv.ID, &inv.UpdatedAt)
}

func (r *repository) GetByProductID(ctx context.Context, productID string) (*domain.Inventory, error) {
	query := `SELECT id, product_id, quantity, reserved, updated_at FROM inventory WHERE product_id = $1`

	inv := &domain.Inventory{}
	err := r.pool.QueryRow(ctx, query, productID).
		Scan(&inv.ID, &inv.ProductID, &inv.Quantity, &inv.Reserved, &inv.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("inventory not found for product")
		}
		return nil, err
	}
	inv.Available = inv.Quantity - inv.Reserved
	return inv, nil
}

func (r *repository) List(ctx context.Context, limit, offset int) ([]*domain.Inventory, int64, error) {
	var total int64
	err := r.pool.QueryRow(ctx, `SELECT COUNT(*) FROM inventory`).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	query := `SELECT id, product_id, quantity, reserved, updated_at
		FROM inventory ORDER BY updated_at DESC LIMIT $1 OFFSET $2`

	rows, err := r.pool.Query(ctx, query, limit, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var items []*domain.Inventory
	for rows.Next() {
		inv := &domain.Inventory{}
		if err := rows.Scan(&inv.ID, &inv.ProductID, &inv.Quantity, &inv.Reserved, &inv.UpdatedAt); err != nil {
			return nil, 0, err
		}
		inv.Available = inv.Quantity - inv.Reserved
		items = append(items, inv)
	}
	return items, total, rows.Err()
}

func (r *repository) AdjustQuantity(ctx context.Context, productID string, adjustment int) (*domain.Inventory, error) {
	query := `
		UPDATE inventory
		SET quantity = quantity + $1, updated_at = NOW()
		WHERE product_id = $2
		RETURNING id, product_id, quantity, reserved, updated_at`

	inv := &domain.Inventory{}
	err := r.pool.QueryRow(ctx, query, adjustment, productID).
		Scan(&inv.ID, &inv.ProductID, &inv.Quantity, &inv.Reserved, &inv.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("inventory not found for product")
		}
		return nil, err
	}
	inv.Available = inv.Quantity - inv.Reserved
	return inv, nil
}
