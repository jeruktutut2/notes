package service

import (
	"context"
	"log"
	"time"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/order-service/internal/model"
	"distributed-transaction/services/order-service/internal/repository"

	"github.com/google/uuid"
)

// OrderService handles business logic for orders
type OrderService struct {
	repo     *repository.OrderRepository
	producer *pkgkafka.Producer
}

// NewOrderService creates a new OrderService
func NewOrderService(repo *repository.OrderRepository, producer *pkgkafka.Producer) *OrderService {
	return &OrderService{
		repo:     repo,
		producer: producer,
	}
}

// CreateOrder creates a new order and publishes order.created event
func (s *OrderService) CreateOrder(req model.CreateOrderRequest) (*model.Order, error) {
	order := &model.Order{
		ID:           uuid.New().String(),
		CustomerName: req.CustomerName,
		ProductID:    req.ProductID,
		Quantity:     req.Quantity,
		TotalPrice:   req.TotalPrice,
		Status:       model.OrderStatusPending,
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}

	// Simpan order ke database
	if err := s.repo.Create(order); err != nil {
		return nil, err
	}

	log.Printf("[ORDER SERVICE] Order created: %s (status: %s)", order.ID, order.Status)

	// Publish event order.created ke Kafka → akan di-consume oleh Inventory Service
	event := events.OrderCreatedEvent{
		OrderID:      order.ID,
		CustomerName: order.CustomerName,
		ProductID:    order.ProductID,
		Quantity:     order.Quantity,
		TotalPrice:   order.TotalPrice,
		Timestamp:    events.Now(),
	}

	data, err := events.Marshal(event)
	if err != nil {
		log.Printf("[ORDER SERVICE] Failed to marshal event: %v", err)
		return order, nil
	}

	go func() {
		if err := s.producer.Publish(context.Background(), events.TopicOrderCreated, order.ID, data); err != nil {
			log.Printf("[ORDER SERVICE] Failed to publish order.created: %v", err)
		}
	}()

	return order, nil
}

// GetOrder retrieves an order by ID
func (s *OrderService) GetOrder(id string) (*model.Order, error) {
	return s.repo.GetByID(id)
}

// GetAllOrders retrieves all orders
func (s *OrderService) GetAllOrders() ([]model.Order, error) {
	return s.repo.GetAll()
}

// HandleInventoryReserved handles when inventory is successfully reserved
func (s *OrderService) HandleInventoryReserved(orderID string) error {
	log.Printf("[ORDER SERVICE] Inventory reserved for order: %s", orderID)
	return s.repo.UpdateStatus(orderID, model.OrderStatusInventoryReserved, "")
}

// HandlePaymentCompleted handles when payment is completed
func (s *OrderService) HandlePaymentCompleted(orderID string) error {
	log.Printf("[ORDER SERVICE] Payment completed for order: %s", orderID)
	return s.repo.UpdateStatus(orderID, model.OrderStatusPaymentCompleted, "")
}

// HandleShippingCreated handles when shipping is created - saga complete!
func (s *OrderService) HandleShippingCreated(orderID string) error {
	log.Printf("[ORDER SERVICE] Shipping created for order: %s → SAGA COMPLETED!", orderID)

	// Update status ke COMPLETED
	if err := s.repo.UpdateStatus(orderID, model.OrderStatusCompleted, ""); err != nil {
		return err
	}

	// Publish order.completed → Notification Service
	event := events.OrderCompletedEvent{
		OrderID:   orderID,
		Timestamp: events.Now(),
	}
	data, _ := events.Marshal(event)
	go func() {
		s.producer.Publish(context.Background(), events.TopicOrderCompleted, orderID, data)
	}()

	return nil
}

// HandleSagaFailure handles any saga failure
func (s *OrderService) HandleSagaFailure(orderID string, reason string) error {
	log.Printf("[ORDER SERVICE] Saga FAILED for order: %s reason: %s", orderID, reason)

	// Update status ke FAILED
	if err := s.repo.UpdateStatus(orderID, model.OrderStatusFailed, reason); err != nil {
		return err
	}

	// Publish order.failed → Notification Service
	event := events.OrderFailedEvent{
		OrderID:   orderID,
		Reason:    reason,
		Timestamp: events.Now(),
	}
	data, _ := events.Marshal(event)
	go func() {
		s.producer.Publish(context.Background(), events.TopicOrderFailed, orderID, data)
	}()

	return nil
}
