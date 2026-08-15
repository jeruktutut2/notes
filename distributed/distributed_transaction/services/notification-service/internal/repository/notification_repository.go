package repository

import (
	"database/sql"

	"distributed-transaction/services/notification-service/internal/model"
)

type NotificationRepository struct {
	db *sql.DB
}

func NewNotificationRepository(db *sql.DB) *NotificationRepository {
	return &NotificationRepository{db: db}
}

func (r *NotificationRepository) Create(notif *model.Notification) error {
	query := `
		INSERT INTO notifications (id, order_id, type, message, status, created_at)
		VALUES ($1, $2, $3, $4, $5, $6)
	`
	_, err := r.db.Exec(query,
		notif.ID, notif.OrderID, notif.Type,
		notif.Message, notif.Status, notif.CreatedAt,
	)
	return err
}

func (r *NotificationRepository) GetAll() ([]model.Notification, error) {
	query := `
		SELECT id, order_id, type, message, status, created_at
		FROM notifications ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var notifications []model.Notification
	for rows.Next() {
		var n model.Notification
		err := rows.Scan(&n.ID, &n.OrderID, &n.Type, &n.Message, &n.Status, &n.CreatedAt)
		if err != nil {
			return nil, err
		}
		notifications = append(notifications, n)
	}
	return notifications, nil
}

func (r *NotificationRepository) GetByOrderID(orderID string) ([]model.Notification, error) {
	query := `
		SELECT id, order_id, type, message, status, created_at
		FROM notifications WHERE order_id = $1 ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query, orderID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var notifications []model.Notification
	for rows.Next() {
		var n model.Notification
		err := rows.Scan(&n.ID, &n.OrderID, &n.Type, &n.Message, &n.Status, &n.CreatedAt)
		if err != nil {
			return nil, err
		}
		notifications = append(notifications, n)
	}
	return notifications, nil
}
