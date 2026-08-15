package events

import (
	"encoding/json"
	"time"
)

// ==================== TOPIC NAMES ====================

const (
	// Order topics
	TopicOrderCreated   = "order.created"
	TopicOrderCompleted = "order.completed"
	TopicOrderFailed    = "order.failed"

	// Inventory topics
	TopicInventoryReserved = "inventory.reserved"
	TopicInventoryFailed   = "inventory.failed"
	TopicInventoryReleased = "inventory.released"

	// Payment topics
	TopicPaymentCompleted = "payment.completed"
	TopicPaymentFailed    = "payment.failed"

	// Shipping topics
	TopicShippingCreated = "shipping.created"
	TopicShippingFailed  = "shipping.failed"
)

// AllTopics returns all Kafka topics used in the system
func AllTopics() []string {
	return []string{
		TopicOrderCreated,
		TopicOrderCompleted,
		TopicOrderFailed,
		TopicInventoryReserved,
		TopicInventoryFailed,
		TopicInventoryReleased,
		TopicPaymentCompleted,
		TopicPaymentFailed,
		TopicShippingCreated,
		TopicShippingFailed,
	}
}

// ==================== EVENT STRUCTS ====================

// OrderCreatedEvent - dikirim saat order baru dibuat
type OrderCreatedEvent struct {
	OrderID      string  `json:"order_id"`
	CustomerName string  `json:"customer_name"`
	ProductID    string  `json:"product_id"`
	Quantity     int     `json:"quantity"`
	TotalPrice   float64 `json:"total_price"`
	Timestamp    string  `json:"timestamp"`
}

// OrderCompletedEvent - dikirim saat order selesai (saga complete)
type OrderCompletedEvent struct {
	OrderID   string `json:"order_id"`
	Timestamp string `json:"timestamp"`
}

// OrderFailedEvent - dikirim saat order gagal
type OrderFailedEvent struct {
	OrderID   string `json:"order_id"`
	Reason    string `json:"reason"`
	Timestamp string `json:"timestamp"`
}

// InventoryReservedEvent - dikirim saat stok berhasil direserve
type InventoryReservedEvent struct {
	OrderID   string `json:"order_id"`
	ProductID string `json:"product_id"`
	Quantity  int    `json:"quantity"`
	Timestamp string `json:"timestamp"`
}

// InventoryFailedEvent - dikirim saat stok tidak cukup
type InventoryFailedEvent struct {
	OrderID   string `json:"order_id"`
	ProductID string `json:"product_id"`
	Reason    string `json:"reason"`
	Timestamp string `json:"timestamp"`
}

// InventoryReleasedEvent - dikirim saat stok di-release (compensation)
type InventoryReleasedEvent struct {
	OrderID   string `json:"order_id"`
	ProductID string `json:"product_id"`
	Quantity  int    `json:"quantity"`
	Timestamp string `json:"timestamp"`
}

// PaymentCompletedEvent - dikirim saat pembayaran berhasil
type PaymentCompletedEvent struct {
	OrderID   string  `json:"order_id"`
	PaymentID string  `json:"payment_id"`
	Amount    float64 `json:"amount"`
	Timestamp string  `json:"timestamp"`
}

// PaymentFailedEvent - dikirim saat pembayaran gagal
type PaymentFailedEvent struct {
	OrderID   string `json:"order_id"`
	Reason    string `json:"reason"`
	Timestamp string `json:"timestamp"`
}

// ShippingCreatedEvent - dikirim saat pengiriman dibuat
type ShippingCreatedEvent struct {
	OrderID        string `json:"order_id"`
	ShipmentID     string `json:"shipment_id"`
	TrackingNumber string `json:"tracking_number"`
	Timestamp      string `json:"timestamp"`
}

// ShippingFailedEvent - dikirim saat pengiriman gagal
type ShippingFailedEvent struct {
	OrderID string `json:"order_id"`
	Reason  string `json:"reason"`
	Timestamp string `json:"timestamp"`
}

// ==================== HELPER FUNCTIONS ====================

// Now returns current timestamp as string
func Now() string {
	return time.Now().Format(time.RFC3339)
}

// Marshal serializes event to JSON bytes
func Marshal(v interface{}) ([]byte, error) {
	return json.Marshal(v)
}

// Unmarshal deserializes JSON bytes to event struct
func Unmarshal(data []byte, v interface{}) error {
	return json.Unmarshal(data, v)
}
