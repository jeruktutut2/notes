package service

import (
	"context"
	"log"
	"math/rand"
	"time"

	"distributed-transaction/pkg/events"
	pkgkafka "distributed-transaction/pkg/kafka"
	"distributed-transaction/services/payment-service/internal/model"
	"distributed-transaction/services/payment-service/internal/repository"

	"github.com/google/uuid"
)

// PaymentService handles payment business logic
type PaymentService struct {
	repo     *repository.PaymentRepository
	producer *pkgkafka.Producer
}

func NewPaymentService(repo *repository.PaymentRepository, producer *pkgkafka.Producer) *PaymentService {
	return &PaymentService{
		repo:     repo,
		producer: producer,
	}
}

// ProcessPayment processes payment for an order
// Simulasi: 20% chance gagal untuk demo compensation flow
func (s *PaymentService) ProcessPayment(orderID string, amount float64) error {
	payment := &model.Payment{
		ID:        uuid.New().String(),
		OrderID:   orderID,
		Amount:    amount,
		Status:    model.PaymentStatusPending,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	// Simpan payment ke database
	if err := s.repo.Create(payment); err != nil {
		return err
	}

	log.Printf("[PAYMENT SERVICE] Processing payment %s for order %s amount: %.2f", payment.ID, orderID, amount)

	// Simulasi proses payment (delay 1 detik)
	time.Sleep(1 * time.Second)

	// Simulasi random failure 20%
	if rand.Float64() < 0.2 {
		log.Printf("[PAYMENT SERVICE] ❌ Payment FAILED for order %s (simulated failure)", orderID)

		s.repo.UpdateStatus(payment.ID, model.PaymentStatusFailed, "Insufficient funds (simulated)")

		// Publish payment.failed → Inventory Service (release stock) + Order Service (update status)
		event := events.PaymentFailedEvent{
			OrderID:   orderID,
			Reason:    "Insufficient funds (simulated)",
			Timestamp: events.Now(),
		}
		data, _ := events.Marshal(event)
		go func() {
			s.producer.Publish(context.Background(), events.TopicPaymentFailed, orderID, data)
		}()
		return nil
	}

	// Payment berhasil
	log.Printf("[PAYMENT SERVICE] ✅ Payment COMPLETED for order %s", orderID)
	s.repo.UpdateStatus(payment.ID, model.PaymentStatusCompleted, "")

	// Publish payment.completed → Shipping Service + Order Service
	event := events.PaymentCompletedEvent{
		OrderID:   orderID,
		PaymentID: payment.ID,
		Amount:    amount,
		Timestamp: events.Now(),
	}
	data, _ := events.Marshal(event)
	go func() {
		s.producer.Publish(context.Background(), events.TopicPaymentCompleted, orderID, data)
	}()

	return nil
}

// RefundPayment refunds a payment (compensation action)
func (s *PaymentService) RefundPayment(orderID string) error {
	payment, err := s.repo.GetByOrderID(orderID)
	if err != nil {
		log.Printf("[PAYMENT SERVICE] No payment found for order %s to refund", orderID)
		return nil
	}

	if payment.Status != model.PaymentStatusCompleted {
		log.Printf("[PAYMENT SERVICE] Payment %s not in COMPLETED status, skip refund", payment.ID)
		return nil
	}

	log.Printf("[PAYMENT SERVICE] 💰 Refunding payment %s for order %s", payment.ID, orderID)
	return s.repo.UpdateStatus(payment.ID, model.PaymentStatusRefunded, "Refunded due to shipping failure")
}

func (s *PaymentService) GetAllPayments() ([]model.Payment, error) {
	return s.repo.GetAll()
}
