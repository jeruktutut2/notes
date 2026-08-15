package service

import (
	"fmt"
	"log"
	"time"

	"distributed-transaction/services/notification-service/internal/model"
	"distributed-transaction/services/notification-service/internal/repository"

	"github.com/google/uuid"
)

type NotificationService struct {
	repo *repository.NotificationRepository
}

func NewNotificationService(repo *repository.NotificationRepository) *NotificationService {
	return &NotificationService{repo: repo}
}

// SendOrderCompletedNotification sends notification for completed order
func (s *NotificationService) SendOrderCompletedNotification(orderID string) error {
	message := fmt.Sprintf("🎉 Order %s telah BERHASIL! Pesanan Anda sedang dalam proses pengiriman.", orderID)

	notif := &model.Notification{
		ID:        uuid.New().String(),
		OrderID:   orderID,
		Type:      model.NotifTypeOrderCompleted,
		Message:   message,
		Status:    model.NotifStatusSent,
		CreatedAt: time.Now(),
	}

	if err := s.repo.Create(notif); err != nil {
		return err
	}

	// Simulasi kirim notifikasi (di real app, kirim email/push notification)
	log.Println("╔══════════════════════════════════════════════════════════╗")
	log.Println("║                  📧 NOTIFICATION SENT                   ║")
	log.Printf("║  Type: %s                           ║\n", notif.Type)
	log.Printf("║  Order: %s  ║\n", orderID)
	log.Printf("║  Message: %s  ║\n", message[:40])
	log.Println("╚══════════════════════════════════════════════════════════╝")

	return nil
}

// SendOrderFailedNotification sends notification for failed order
func (s *NotificationService) SendOrderFailedNotification(orderID string, reason string) error {
	message := fmt.Sprintf("❌ Order %s GAGAL! Alasan: %s. Silakan coba kembali.", orderID, reason)

	notif := &model.Notification{
		ID:        uuid.New().String(),
		OrderID:   orderID,
		Type:      model.NotifTypeOrderFailed,
		Message:   message,
		Status:    model.NotifStatusSent,
		CreatedAt: time.Now(),
	}

	if err := s.repo.Create(notif); err != nil {
		return err
	}

	log.Println("╔══════════════════════════════════════════════════════════╗")
	log.Println("║                  📧 NOTIFICATION SENT                   ║")
	log.Printf("║  Type: %s                               ║\n", notif.Type)
	log.Printf("║  Order: %s  ║\n", orderID)
	log.Printf("║  Reason: %s  ║\n", reason)
	log.Println("╚══════════════════════════════════════════════════════════╝")

	return nil
}

func (s *NotificationService) GetAllNotifications() ([]model.Notification, error) {
	return s.repo.GetAll()
}
