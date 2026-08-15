package repository

import (
	"database/sql"
	"fmt"
	"time"

	"distributed-transaction/services/order-service/internal/model"
)

// OrderRepository handles database operations for orders
type OrderRepository struct {
	db *sql.DB
}

// NewOrderRepository creates a new OrderRepository
func NewOrderRepository(db *sql.DB) *OrderRepository {
	return &OrderRepository{db: db}
}

// Create inserts a new order into the database
func (r *OrderRepository) Create(order *model.Order) error {
	query := `
		INSERT INTO orders (id, customer_name, product_id, quantity, total_price, status, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	`
	_, err := r.db.Exec(query,
		order.ID,
		order.CustomerName,
		order.ProductID,
		order.Quantity,
		order.TotalPrice,
		order.Status,
		order.CreatedAt,
		order.UpdatedAt,
	)
	return err
}

// GetByID retrieves an order by its ID
func (r *OrderRepository) GetByID(id string) (*model.Order, error) {
	query := `
		SELECT id, customer_name, product_id, quantity, total_price, status, 
			   COALESCE(failure_reason, ''), created_at, updated_at
		FROM orders WHERE id = $1
	`
	order := &model.Order{}
	err := r.db.QueryRow(query, id).Scan(
		&order.ID,
		&order.CustomerName,
		&order.ProductID,
		&order.Quantity,
		&order.TotalPrice,
		&order.Status,
		&order.FailureReason,
		&order.CreatedAt,
		&order.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("order not found: %w", err)
	}
	return order, nil
}

// GetAll retrieves all orders
func (r *OrderRepository) GetAll() ([]model.Order, error) {
	query := `
		SELECT id, customer_name, product_id, quantity, total_price, status,
			   COALESCE(failure_reason, ''), created_at, updated_at
		FROM orders ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var orders []model.Order
	for rows.Next() {
		var order model.Order
		err := rows.Scan(
			&order.ID,
			&order.CustomerName,
			&order.ProductID,
			&order.Quantity,
			&order.TotalPrice,
			&order.Status,
			&order.FailureReason,
			&order.CreatedAt,
			&order.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}
		orders = append(orders, order)
	}
	return orders, nil
}

// UpdateStatus updates the status of an order
func (r *OrderRepository) UpdateStatus(id string, status string, reason string) error {
	query := `
		UPDATE orders SET status = $1, failure_reason = $2, updated_at = $3
		WHERE id = $4
	`
	result, err := r.db.Exec(query, status, reason, time.Now(), id)
	if err != nil {
		return err
	}
	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		return fmt.Errorf("order %s not found", id)
	}
	return nil
}
