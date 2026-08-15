package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/example/modular-monolith/internal/modules/notification/domain"
)

type repository struct {
	pool *pgxpool.Pool
}

func NewRepository(pool *pgxpool.Pool) domain.NotificationRepository {
	return &repository{pool: pool}
}

func (r *repository) Create(ctx context.Context, n *domain.Notification) error {
	query := `
		INSERT INTO notifications (user_id, title, message)
		VALUES ($1, $2, $3)
		RETURNING id, is_read, created_at`

	return r.pool.QueryRow(ctx, query, n.UserID, n.Title, n.Message).
		Scan(&n.ID, &n.IsRead, &n.CreatedAt)
}

func (r *repository) GetByID(ctx context.Context, id string) (*domain.Notification, error) {
	query := `SELECT id, user_id, title, message, is_read, created_at FROM notifications WHERE id = $1`

	n := &domain.Notification{}
	err := r.pool.QueryRow(ctx, query, id).
		Scan(&n.ID, &n.UserID, &n.Title, &n.Message, &n.IsRead, &n.CreatedAt)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, fmt.Errorf("notification not found")
		}
		return nil, err
	}
	return n, nil
}

func (r *repository) ListByUser(ctx context.Context, userID string, limit, offset int) ([]*domain.Notification, int64, error) {
	var total int64
	err := r.pool.QueryRow(ctx, `SELECT COUNT(*) FROM notifications WHERE user_id = $1`, userID).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	query := `SELECT id, user_id, title, message, is_read, created_at
		FROM notifications WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3`

	rows, err := r.pool.Query(ctx, query, userID, limit, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var notifications []*domain.Notification
	for rows.Next() {
		n := &domain.Notification{}
		if err := rows.Scan(&n.ID, &n.UserID, &n.Title, &n.Message, &n.IsRead, &n.CreatedAt); err != nil {
			return nil, 0, err
		}
		notifications = append(notifications, n)
	}
	return notifications, total, rows.Err()
}

func (r *repository) MarkAsRead(ctx context.Context, id string) error {
	result, err := r.pool.Exec(ctx, `UPDATE notifications SET is_read = TRUE WHERE id = $1`, id)
	if err != nil {
		return err
	}
	if result.RowsAffected() == 0 {
		return fmt.Errorf("notification not found")
	}
	return nil
}
