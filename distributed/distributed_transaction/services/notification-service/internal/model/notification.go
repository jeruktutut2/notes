package model

import "time"

const (
	NotifTypeOrderCompleted = "ORDER_COMPLETED"
	NotifTypeOrderFailed    = "ORDER_FAILED"

	NotifStatusSent   = "SENT"
	NotifStatusFailed = "FAILED"
)

// Notification represents a notification record
type Notification struct {
	ID        string    `json:"id"`
	OrderID   string    `json:"order_id"`
	Type      string    `json:"type"`
	Message   string    `json:"message"`
	Status    string    `json:"status"`
	CreatedAt time.Time `json:"created_at"`
}
