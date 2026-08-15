package repository

import (
	"database/sql"
	"fmt"
	"time"

	"distributed-transaction/services/shipping-service/internal/model"
)

type ShippingRepository struct {
	db *sql.DB
}

func NewShippingRepository(db *sql.DB) *ShippingRepository {
	return &ShippingRepository{db: db}
}

func (r *ShippingRepository) Create(shipment *model.Shipment) error {
	query := `
		INSERT INTO shipments (id, order_id, address, status, tracking_number, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7)
	`
	_, err := r.db.Exec(query,
		shipment.ID, shipment.OrderID, shipment.Address,
		shipment.Status, shipment.TrackingNumber,
		shipment.CreatedAt, shipment.UpdatedAt,
	)
	return err
}

func (r *ShippingRepository) GetByOrderID(orderID string) (*model.Shipment, error) {
	query := `
		SELECT id, order_id, address, status, COALESCE(tracking_number, ''), 
			   COALESCE(failure_reason, ''), created_at, updated_at
		FROM shipments WHERE order_id = $1 ORDER BY created_at DESC LIMIT 1
	`
	s := &model.Shipment{}
	err := r.db.QueryRow(query, orderID).Scan(
		&s.ID, &s.OrderID, &s.Address, &s.Status,
		&s.TrackingNumber, &s.FailureReason,
		&s.CreatedAt, &s.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("shipment not found: %w", err)
	}
	return s, nil
}

func (r *ShippingRepository) GetAll() ([]model.Shipment, error) {
	query := `
		SELECT id, order_id, address, status, COALESCE(tracking_number, ''),
			   COALESCE(failure_reason, ''), created_at, updated_at
		FROM shipments ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var shipments []model.Shipment
	for rows.Next() {
		var s model.Shipment
		err := rows.Scan(&s.ID, &s.OrderID, &s.Address, &s.Status,
			&s.TrackingNumber, &s.FailureReason, &s.CreatedAt, &s.UpdatedAt)
		if err != nil {
			return nil, err
		}
		shipments = append(shipments, s)
	}
	return shipments, nil
}

func (r *ShippingRepository) UpdateStatus(id string, status string, reason string) error {
	query := `UPDATE shipments SET status = $1, failure_reason = $2, updated_at = $3 WHERE id = $4`
	result, err := r.db.Exec(query, status, reason, time.Now(), id)
	if err != nil {
		return err
	}
	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		return fmt.Errorf("shipment %s not found", id)
	}
	return nil
}
