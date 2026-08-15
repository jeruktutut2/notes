package main

import (
	"log"
	"os"

	"distributed_queue/internal/tasks"

	"github.com/hibiken/asynq"
)

func main() {
	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "localhost:6382"
	}

	// Buat server Worker Asynq. 
	// Kita set Concurrency ke 10 agar bisa memproses 10 tugas sekaligus.
	// Kita juga me-listen ke 2 queue berbeda ("default" dan "critical").
	srv := asynq.NewServer(
		asynq.RedisClientOpt{Addr: redisURL},
		asynq.Config{
			Concurrency: 10,
			Queues: map[string]int{
				"critical": 6, // 60% waktu/resource untuk antrean critical
				"default":  4, // 40% waktu/resource untuk antrean default
			},
		},
	)

	// Routing Task: Memetakan tipe task ke fungsi handler
	mux := asynq.NewServeMux()
	mux.HandleFunc(tasks.TypeEmailDelivery, tasks.HandleEmailDeliveryTask)
	mux.HandleFunc(tasks.TypeImageResize, tasks.HandleImageResizeTask)

	log.Println("👷 Menjalankan Background Worker...")
	if err := srv.Run(mux); err != nil {
		log.Fatalf("Gagal menjalankan worker server: %v", err)
	}
}
