package service

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"time"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/shipping-service/internal/model"
	"distributed-transaction/services/shipping-service/internal/repository"

	"github.com/google/uuid"
)

type ShippingService struct {
	repo     *repository.ShippingRepository
	producer *pkgkafka.Producer
}

func NewShippingService(repo *repository.ShippingRepository, producer *pkgkafka.Producer) *ShippingService {
	return &ShippingService{
		repo:     repo,
		producer: producer,
	}
}

// CreateShipment creates a shipment for an order
// Simulasi: 10% chance gagal untuk demo compensation flow
func (s *ShippingService) CreateShipment(orderID string) error {
	trackingNumber := fmt.Sprintf("TRK-%s", uuid.New().String()[:8])

	shipment := &model.Shipment{
		ID:             uuid.New().String(),
		OrderID:        orderID,
		Address:        "Jl. Contoh Alamat No. 123, Jakarta",
		Status:         model.ShipmentStatusPending,
		TrackingNumber: trackingNumber,
		CreatedAt:      time.Now(),
		UpdatedAt:      time.Now(),
	}

	if err := s.repo.Create(shipment); err != nil {
		return err
	}

	log.Printf("[SHIPPING SERVICE] Processing shipment %s for order %s", shipment.ID, orderID)

	// Simulasi proses shipping (delay 1 detik)
	time.Sleep(1 * time.Second)

	// Simulasi random failure 10%
	if rand.Float64() < 0.1 {
		log.Printf("[SHIPPING SERVICE] ❌ Shipping FAILED for order %s (simulated failure)", orderID)

		s.repo.UpdateStatus(shipment.ID, model.ShipmentStatusFailed, "Courier unavailable (simulated)")

		// Publish shipping.failed → Payment Service (refund) + Inventory Service (release) + Order Service
		event := events.ShippingFailedEvent{
			OrderID:   orderID,
			Reason:    "Courier unavailable (simulated)",
			Timestamp: events.Now(),
		}
		data, _ := events.Marshal(event)
		go func() {
			s.producer.Publish(context.Background(), events.TopicShippingFailed, orderID, data)
		}()
		return nil
	}

	// Shipping berhasil
	log.Printf("[SHIPPING SERVICE] ✅ Shipping CREATED for order %s tracking: %s", orderID, trackingNumber)
	s.repo.UpdateStatus(shipment.ID, model.ShipmentStatusCreated, "")

	// Publish shipping.created → Order Service (saga complete!)
	event := events.ShippingCreatedEvent{
		OrderID:        orderID,
		ShipmentID:     shipment.ID,
		TrackingNumber: trackingNumber,
		Timestamp:      events.Now(),
	}
	data, _ := events.Marshal(event)
	go func() {
		s.producer.Publish(context.Background(), events.TopicShippingCreated, orderID, data)
	}()

	return nil
}

func (s *ShippingService) GetAllShipments() ([]model.Shipment, error) {
	return s.repo.GetAll()
}
