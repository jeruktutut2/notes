package model

import "time"

const (
	ShipmentStatusPending   = "PENDING"
	ShipmentStatusCreated   = "CREATED"
	ShipmentStatusFailed    = "FAILED"
	ShipmentStatusCancelled = "CANCELLED"
)

// Shipment represents a shipping record
type Shipment struct {
	ID             string    `json:"id"`
	OrderID        string    `json:"order_id"`
	Address        string    `json:"address"`
	Status         string    `json:"status"`
	TrackingNumber string    `json:"tracking_number,omitempty"`
	FailureReason  string    `json:"failure_reason,omitempty"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}
