package repository

import (
	"database/sql"
	"fmt"
	"time"

	"distributed-transaction/services/payment-service/internal/model"
)

type PaymentRepository struct {
	db *sql.DB
}

func NewPaymentRepository(db *sql.DB) *PaymentRepository {
	return &PaymentRepository{db: db}
}

func (r *PaymentRepository) Create(payment *model.Payment) error {
	query := `
		INSERT INTO payments (id, order_id, amount, status, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6)
	`
	_, err := r.db.Exec(query,
		payment.ID, payment.OrderID, payment.Amount,
		payment.Status, payment.CreatedAt, payment.UpdatedAt,
	)
	return err
}

func (r *PaymentRepository) GetByOrderID(orderID string) (*model.Payment, error) {
	query := `
		SELECT id, order_id, amount, status, COALESCE(failure_reason, ''), created_at, updated_at
		FROM payments WHERE order_id = $1 ORDER BY created_at DESC LIMIT 1
	`
	payment := &model.Payment{}
	err := r.db.QueryRow(query, orderID).Scan(
		&payment.ID, &payment.OrderID, &payment.Amount,
		&payment.Status, &payment.FailureReason,
		&payment.CreatedAt, &payment.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("payment not found: %w", err)
	}
	return payment, nil
}

func (r *PaymentRepository) GetAll() ([]model.Payment, error) {
	query := `
		SELECT id, order_id, amount, status, COALESCE(failure_reason, ''), created_at, updated_at
		FROM payments ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var payments []model.Payment
	for rows.Next() {
		var p model.Payment
		err := rows.Scan(&p.ID, &p.OrderID, &p.Amount, &p.Status, &p.FailureReason, &p.CreatedAt, &p.UpdatedAt)
		if err != nil {
			return nil, err
		}
		payments = append(payments, p)
	}
	return payments, nil
}

func (r *PaymentRepository) UpdateStatus(id string, status string, reason string) error {
	query := `UPDATE payments SET status = $1, failure_reason = $2, updated_at = $3 WHERE id = $4`
	result, err := r.db.Exec(query, status, reason, time.Now(), id)
	if err != nil {
		return err
	}
	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		return fmt.Errorf("payment %s not found", id)
	}
	return nil
}
