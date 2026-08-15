package scheduler

import (
	"context"
	"log"
	"time"

	"github.com/bsm/redislock"
	"github.com/redis/go-redis/v9"
)

type DistributedScheduler struct {
	redisClient *redis.Client
	locker      *redislock.Client
	nodeID      string
}

func NewDistributedScheduler(redisURL, nodeID string) *DistributedScheduler {
	opts, err := redis.ParseURL(redisURL)
	if err != nil {
		log.Fatalf("Gagal mem-parse Redis URL: %v", err)
	}

	client := redis.NewClient(opts)
	locker := redislock.New(client)

	return &DistributedScheduler{
		redisClient: client,
		locker:      locker,
		nodeID:      nodeID,
	}
}

// RunExclusiveJob memastikan bahwa tugas cron hanya dijalankan oleh SATU node pada satu waktu.
func (s *DistributedScheduler) RunExclusiveJob(jobName string, taskFunc func()) {
	log.Printf("[Node %s] Menjalankan scheduler untuk %s...", s.nodeID, jobName)
	
	// Gunakan nama job sebagai kunci lock
	lockKey := "cron_lock:" + jobName
	
	// Coba ambil lock. TTL harus lebih pendek dari interval eksekusi cron
	// tapi cukup panjang untuk menyelesaikan taskFunc()
	lock, err := s.locker.Obtain(context.Background(), lockKey, 5*time.Second, nil)
	
	if err == redislock.ErrNotObtained {
		// Gagal dapat lock (karena sudah diambil node lain)
		log.Printf("[Node %s] ❌ Gagal mendapatkan lock. Node lain sedang mengerjakan %s", s.nodeID, jobName)
		return
	} else if err != nil {
		log.Printf("[Node %s] Error mengambil lock: %v", s.nodeID, err)
		return
	}

	// Jangan lupa release lock (walaupun TTL akan habis sendiri)
	// Kita taruh di defer agar pasti tereksekusi
	defer lock.Release(context.Background())

	// Kita yang dapat lock! Jalankan tugas eksklusifnya.
	log.Printf("[Node %s] 👑 MENDAPATKAN LOCK! Mengeksekusi tugas: %s", s.nodeID, jobName)
	
	// Eksekusi fungsi bisnis yang sebenarnya
	taskFunc()
	
	log.Printf("[Node %s] ✅ Selesai mengeksekusi %s", s.nodeID, jobName)
}
