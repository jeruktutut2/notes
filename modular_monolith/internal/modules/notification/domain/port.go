package domain

import "context"

// NotificationRepository is the OUTBOUND PORT for notification data persistence.
type NotificationRepository interface {
	Create(ctx context.Context, n *Notification) error
	GetByID(ctx context.Context, id string) (*Notification, error)
	ListByUser(ctx context.Context, userID string, limit, offset int) ([]*Notification, int64, error)
	MarkAsRead(ctx context.Context, id string) error
}

// NotificationService is the INBOUND PORT defining use cases for notifications.
type NotificationService interface {
	Create(ctx context.Context, userID, title, message string) (*Notification, error)
	GetByID(ctx context.Context, id string) (*Notification, error)
	ListByUser(ctx context.Context, userID string, page, limit int) ([]*Notification, int64, error)
	MarkAsRead(ctx context.Context, id string) error
}
