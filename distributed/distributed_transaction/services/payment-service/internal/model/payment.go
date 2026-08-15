package model

import "time"

const (
	PaymentStatusPending   = "PENDING"
	PaymentStatusCompleted = "COMPLETED"
	PaymentStatusFailed    = "FAILED"
	PaymentStatusRefunded  = "REFUNDED"
)

// Payment represents a payment record
type Payment struct {
	ID            string    `json:"id"`
	OrderID       string    `json:"order_id"`
	Amount        float64   `json:"amount"`
	Status        string    `json:"status"`
	FailureReason string    `json:"failure_reason,omitempty"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}
