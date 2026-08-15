package tasks

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/hibiken/asynq"
)

// Task Types
const (
	TypeEmailDelivery = "email:deliver"
	TypeImageResize   = "image:resize"
)

// Payloads
type EmailDeliveryPayload struct {
	UserID     int
	TemplateID string
}

type ImageResizePayload struct {
	ImageURL string
	Width    int
	Height   int
}

// ==========================================
// TASK CREATORS (Digunakan oleh Client)
// ==========================================

func NewEmailDeliveryTask(userID int, tmplID string) (*asynq.Task, error) {
	payload, err := json.Marshal(EmailDeliveryPayload{UserID: userID, TemplateID: tmplID})
	if err != nil {
		return nil, err
	}
	return asynq.NewTask(TypeEmailDelivery, payload), nil
}

func NewImageResizeTask(src string, w, h int) (*asynq.Task, error) {
	payload, err := json.Marshal(ImageResizePayload{ImageURL: src, Width: w, Height: h})
	if err != nil {
		return nil, err
	}
	// Task ini akan di-retry maksimal 5 kali jika gagal, dengan timeout 10 detik
	return asynq.NewTask(TypeImageResize, payload, asynq.MaxRetry(5), asynq.Timeout(10*time.Second)), nil
}

// ==========================================
// TASK HANDLERS (Digunakan oleh Worker)
// ==========================================

func HandleEmailDeliveryTask(ctx context.Context, t *asynq.Task) error {
	var p EmailDeliveryPayload
	if err := json.Unmarshal(t.Payload(), &p); err != nil {
		return fmt.Errorf("json.Unmarshal failed: %v: %w", err, asynq.SkipRetry) // Skip retry if JSON is invalid
	}
	log.Printf("📧 [*] Mengirim email ke User_ID=%d dengan Template=%s", p.UserID, p.TemplateID)
	// Simulasi kerja lambat (mengirim email)
	time.Sleep(2 * time.Second)
	log.Printf("✅ Email berhasil terkirim ke User_ID=%d", p.UserID)
	return nil
}

func HandleImageResizeTask(ctx context.Context, t *asynq.Task) error {
	var p ImageResizePayload
	if err := json.Unmarshal(t.Payload(), &p); err != nil {
		return fmt.Errorf("json.Unmarshal failed: %v: %w", err, asynq.SkipRetry)
	}
	log.Printf("🖼️  [*] Memproses gambar %s menjadi %dx%d", p.ImageURL, p.Width, p.Height)
	// Simulasi kerja CPU intensive
	time.Sleep(3 * time.Second)
	log.Printf("✅ Gambar %s selesai diproses", p.ImageURL)
	return nil
}
