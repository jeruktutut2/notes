package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/example/modular-monolith/internal/modules/order/domain"
)

type repository struct {
	pool *pgxpool.Pool
}

func NewRepository(pool *pgxpool.Pool) domain.OrderRepository {
	return &repository{pool: pool}
}

func (r *repository) Create(ctx context.Context, o *domain.Order) error {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback(ctx)

	orderQuery := `
		INSERT INTO orders (user_id, total_amount, status)
		VALUES ($1, $2, $3)
		RETURNING id, created_at, updated_at`

	err = tx.QueryRow(ctx, orderQuery, o.UserID, o.TotalAmount, o.Status).
		Scan(&o.ID, &o.CreatedAt, &o.UpdatedAt)
	if err != nil {
		return fmt.Errorf("failed to insert order: %w", err)
	}

	itemQuery := `
		INSERT INTO order_items (order_id, product_id, quantity, price)
		VALUES ($1, $2, $3, $4)
		RETURNING id, created_at`

	for _, item := range o.Items {
		item.OrderID = o.ID
		err = tx.QueryRow(ctx, itemQuery, item.OrderID, item.ProductID, item.Quantity, item.Price).
			Scan(&item.ID, &item.CreatedAt)
		if err != nil {
			return fmt.Errorf("failed to insert order item: %w", err)
		}
	}

	return tx.Commit(ctx)
}

func (r *repository) GetByID(ctx context.Context, id string) (*domain.Order, error) {
	orderQuery := `SELECT id, user_id, total_amount, status, created_at, updated_at FROM orders WHERE id = $1`
	o := &domain.Order{}
	err := r.pool.QueryRow(ctx, orderQuery, id).
		Scan(&o.ID, &o.UserID, &o.TotalAmount, &o.Status, &o.CreatedAt, &o.UpdatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("order not found")
		}
		return nil, err
	}

	itemQuery := `SELECT id, order_id, product_id, quantity, price, created_at FROM order_items WHERE order_id = $1`
	rows, err := r.pool.Query(ctx, itemQuery, id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		item := &domain.OrderItem{}
		if err := rows.Scan(&item.ID, &item.OrderID, &item.ProductID, &item.Quantity, &item.Price, &item.CreatedAt); err != nil {
			return nil, err
		}
		o.Items = append(o.Items, item)
	}

	return o, rows.Err()
}

func (r *repository) List(ctx context.Context, userID string, limit, offset int) ([]*domain.Order, int64, error) {
	var total int64
	var countQuery, listQuery string
	var countArgs, listArgs []interface{}

	if userID != "" {
		countQuery = `SELECT COUNT(*) FROM orders WHERE user_id = $1`
		countArgs = []interface{}{userID}
		listQuery = `SELECT id, user_id, total_amount, status, created_at, updated_at
			FROM orders WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3`
		listArgs = []interface{}{userID, limit, offset}
	} else {
		countQuery = `SELECT COUNT(*) FROM orders`
		listQuery = `SELECT id, user_id, total_amount, status, created_at, updated_at
			FROM orders ORDER BY created_at DESC LIMIT $1 OFFSET $2`
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

	var orders []*domain.Order
	for rows.Next() {
		o := &domain.Order{}
		if err := rows.Scan(&o.ID, &o.UserID, &o.TotalAmount, &o.Status, &o.CreatedAt, &o.UpdatedAt); err != nil {
			return nil, 0, err
		}
		orders = append(orders, o)
	}
	return orders, total, rows.Err()
}

func (r *repository) UpdateStatus(ctx context.Context, id, status string) error {
	query := `UPDATE orders SET status = $1, updated_at = NOW() WHERE id = $2`
	result, err := r.pool.Exec(ctx, query, status, id)
	if err != nil {
		return err
	}
	if result.RowsAffected() == 0 {
		return fmt.Errorf("order not found")
	}
	return nil
}
