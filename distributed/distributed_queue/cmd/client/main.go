package main

import (
	"log"
	"os"
	"time"

	"distributed_queue/internal/tasks"

	"github.com/hibiken/asynq"
)

func main() {
	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "localhost:6382"
	}

	client := asynq.NewClient(asynq.RedisClientOpt{Addr: redisURL})
	defer client.Close()

	// 1. Task yang akan langsung dieksekusi (Enqueued immediately)
	task1, err := tasks.NewEmailDeliveryTask(42, "welcome_email")
	if err != nil {
		log.Fatalf("Gagal membuat task: %v", err)
	}
	info, err := client.Enqueue(task1)
	if err != nil {
		log.Fatalf("Gagal enqueue task: %v", err)
	}
	log.Printf("📥 Berhasil enqueue task: id=%s queue=%s", info.ID, info.Queue)

	// 2. Task yang akan dieksekusi di masa depan (Delayed Task)
	// Misalnya: Kirim email pengingat 5 detik dari sekarang
	task2, err := tasks.NewEmailDeliveryTask(42, "reminder_email")
	if err != nil {
		log.Fatalf("Gagal membuat task: %v", err)
	}
	info, err = client.Enqueue(task2, asynq.ProcessIn(5*time.Second))
	if err != nil {
		log.Fatalf("Gagal enqueue task: %v", err)
	}
	log.Printf("📥 Berhasil enqueue DELAYED task (5 detik lagi): id=%s queue=%s", info.ID, info.Queue)

	// 3. Task dengan custom Queue (prioritas/segregasi)
	task3, err := tasks.NewImageResizeTask("https://example.com/image.jpg", 800, 600)
	if err != nil {
		log.Fatalf("Gagal membuat task: %v", err)
	}
	// Masukkan ke antrean khusus bernama "critical"
	info, err = client.Enqueue(task3, asynq.Queue("critical"))
	if err != nil {
		log.Fatalf("Gagal enqueue task: %v", err)
	}
	log.Printf("📥 Berhasil enqueue CRITICAL task: id=%s queue=%s", info.ID, info.Queue)

	log.Println("✅ Semua task berhasil di-enqueue oleh Client. Menunggu worker mengambilnya...")
}
