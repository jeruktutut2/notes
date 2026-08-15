package rest

import (
	"time"

	"github.com/example/modular-monolith/internal/modules/notification/domain"
)

// --- Request DTOs ---

type CreateNotificationRequest struct {
	UserID  string `json:"user_id"`
	Title   string `json:"title"`
	Message string `json:"message"`
}

func (r *CreateNotificationRequest) Validate() string {
	if r.UserID == "" {
		return "user_id is required"
	}
	if r.Title == "" {
		return "title is required"
	}
	if r.Message == "" {
		return "message is required"
	}
	return ""
}

// --- Response DTOs ---

type NotificationResponse struct {
	ID        string    `json:"id"`
	UserID    string    `json:"user_id"`
	Title     string    `json:"title"`
	Message   string    `json:"message"`
	IsRead    bool      `json:"is_read"`
	CreatedAt time.Time `json:"created_at"`
}

func toNotificationResponse(n *domain.Notification) *NotificationResponse {
	if n == nil {
		return nil
	}
	return &NotificationResponse{
		ID:        n.ID,
		UserID:    n.UserID,
		Title:     n.Title,
		Message:   n.Message,
		IsRead:    n.IsRead,
		CreatedAt: n.CreatedAt,
	}
}

func toNotificationListResponse(notifications []*domain.Notification) []*NotificationResponse {
	result := make([]*NotificationResponse, len(notifications))
	for i, n := range notifications {
		result[i] = toNotificationResponse(n)
	}
	return result
}
