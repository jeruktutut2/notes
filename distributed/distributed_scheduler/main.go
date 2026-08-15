package main

import (
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"distributed_scheduler/internal/scheduler"

	"github.com/go-co-op/gocron/v2"
)

func main() {
	nodeID := os.Getenv("NODE_ID")
	if nodeID == "" {
		nodeID = "Node-Unknown"
	}

	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "redis://localhost:6383/0"
	}

	distScheduler := scheduler.NewDistributedScheduler(redisURL, nodeID)

	// Inisiasi Gocron Scheduler
	s, err := gocron.NewScheduler()
	if err != nil {
		log.Fatalf("Error init gocron: %v", err)
	}

	log.Printf("🚀 Memulai Scheduler di [%s]", nodeID)

	// Definisikan Job: Dijalankan setiap 2 detik
	_, err = s.NewJob(
		gocron.DurationJob(2*time.Second),
		gocron.NewTask(func() {
			// Bungkus dengan Distributed Lock
			distScheduler.RunExclusiveJob("report_generator", func() {
				// Simulasi proses generate report berat selama 1 detik
				time.Sleep(1 * time.Second)
				log.Println("📊 [WORK] Report harian berhasil di-generate dan disimpan ke DB.")
			})
		}),
	)

	if err != nil {
		log.Fatalf("Error membuat job: %v", err)
	}

	// Mulai scheduler di background
	s.Start()

	// Handle graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Menutup scheduler...")
	err = s.Shutdown()
	if err != nil {
		log.Println("Error saat shutdown:", err)
	}
}
