package domain

import "time"

// Notification represents the notification domain entity.
type Notification struct {
	ID        string
	UserID    string
	Title     string
	Message   string
	IsRead    bool
	CreatedAt time.Time
}
