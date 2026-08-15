package service

import (
	"context"
	"log"
	"time"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/inventory-service/internal/model"
	"distributed-transaction/services/inventory-service/internal/repository"

	"github.com/google/uuid"
)

type InventoryService struct {
	repo     *repository.InventoryRepository
	producer *pkgkafka.Producer
}

func NewInventoryService(repo *repository.InventoryRepository, producer *pkgkafka.Producer) *InventoryService {
	return &InventoryService{
		repo:     repo,
		producer: producer,
	}
}

// ReserveStock attempts to reserve stock for an order
func (s *InventoryService) ReserveStock(orderID string, productID string, quantity int) error {
	log.Printf("[INVENTORY SERVICE] Attempting to reserve %d of product %s for order %s", quantity, productID, orderID)

	// Coba reserve stock di database
	err := s.repo.ReserveStock(productID, quantity)
	if err != nil {
		log.Printf("[INVENTORY SERVICE] ❌ Failed to reserve stock: %v", err)

		// Publish inventory.failed
		event := events.InventoryFailedEvent{
			OrderID:   orderID,
			ProductID: productID,
			Reason:    err.Error(),
			Timestamp: events.Now(),
		}
		data, _ := events.Marshal(event)
		go func() {
			s.producer.Publish(context.Background(), events.TopicInventoryFailed, orderID, data)
		}()
		return nil // Return nil karena failure sudah di-handle via event
	}

	// Log the reservation
	s.repo.CreateLog(&model.InventoryLog{
		ID:        uuid.New().String(),
		OrderID:   orderID,
		ProductID: productID,
		Quantity:  quantity,
		Action:    model.ActionReserve,
		CreatedAt: time.Now(),
	})

	log.Printf("[INVENTORY SERVICE] ✅ Stock reserved: %d of product %s for order %s", quantity, productID, orderID)

	// Publish inventory.reserved → Payment Service
	event := events.InventoryReservedEvent{
		OrderID:   orderID,
		ProductID: productID,
		Quantity:  quantity,
		Timestamp: events.Now(),
	}
	data, _ := events.Marshal(event)
	go func() {
		s.producer.Publish(context.Background(), events.TopicInventoryReserved, orderID, data)
	}()

	return nil
}

// ReleaseStockByOrderID releases previously reserved stock using inventory_logs (compensation)
func (s *InventoryService) ReleaseStockByOrderID(orderID string) error {
	// Query inventory_logs to find what was reserved
	reservation, err := s.repo.GetReservationByOrderID(orderID)
	if err != nil {
		log.Printf("[INVENTORY SERVICE] No reservation found for order %s, skip release", orderID)
		return nil
	}

	log.Printf("[INVENTORY SERVICE] 🔄 Releasing %d of product %s for order %s (compensation)",
		reservation.Quantity, reservation.ProductID, orderID)

	if err := s.repo.ReleaseStock(reservation.ProductID, reservation.Quantity); err != nil {
		return err
	}

	// Log the release
	s.repo.CreateLog(&model.InventoryLog{
		ID:        uuid.New().String(),
		OrderID:   orderID,
		ProductID: reservation.ProductID,
		Quantity:  reservation.Quantity,
		Action:    model.ActionRelease,
		CreatedAt: time.Now(),
	})

	// Publish inventory.released
	event := events.InventoryReleasedEvent{
		OrderID:   orderID,
		ProductID: reservation.ProductID,
		Quantity:  reservation.Quantity,
		Timestamp: events.Now(),
	}
	data, _ := events.Marshal(event)
	go func() {
		s.producer.Publish(context.Background(), events.TopicInventoryReleased, orderID, data)
	}()

	return nil
}

func (s *InventoryService) GetAllProducts() ([]model.Product, error) {
	return s.repo.GetAllProducts()
}

func (s *InventoryService) CreateProduct(req model.CreateProductRequest) (*model.Product, error) {
	product := &model.Product{
		ID:            uuid.New().String(),
		Name:          req.Name,
		Stock:         req.Stock,
		ReservedStock: 0,
		Price:         req.Price,
		CreatedAt:     time.Now(),
		UpdatedAt:     time.Now(),
	}
	if err := s.repo.CreateProduct(product); err != nil {
		return nil, err
	}
	return product, nil
}
