package cache

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
	"golang.org/x/sync/singleflight"
)

type DistributedCache struct {
	client       *redis.Client
	requestGroup singleflight.Group
}

func NewDistributedCache(redisURL string) *DistributedCache {
	opts, err := redis.ParseURL(redisURL)
	if err != nil {
		log.Fatalf("Gagal mem-parse Redis URL: %v", err)
	}

	client := redis.NewClient(opts)

	// Ping tes koneksi
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := client.Ping(ctx).Err(); err != nil {
		log.Fatalf("Gagal terhubung ke Redis: %v", err)
	}

	return &DistributedCache{
		client: client,
	}
}

// FetchData menggunakan pola Cache-Aside dipadukan dengan Singleflight
// untuk mencegah Cache Stampede / Thundering Herd.
func (c *DistributedCache) FetchData(ctx context.Context, key string, ttl time.Duration, fetchFunc func() (any, error)) (any, error) {
	// 1. Cek cache dulu (Fast path)
	cachedData, err := c.client.Get(ctx, key).Result()
	if err == nil {
		log.Printf("[CACHE HIT] %s", key)
		var result any
		if err := json.Unmarshal([]byte(cachedData), &result); err != nil {
			return nil, fmt.Errorf("gagal unmarshal cache: %w", err)
		}
		return result, nil
	}

	if err != redis.Nil {
		log.Printf("[CACHE ERROR] Gagal membaca Redis: %v", err)
		// Lanjut ke database (fetchFunc) agar sistem tetap berjalan walau cache down
	}

	// 2. Cache Miss! Gunakan Singleflight untuk mencegah thundering herd.
	// Jika ada 1000 request dengan key yang sama pada saat bersamaan,
	// fetchFunc hanya akan dieksekusi 1 kali!
	v, err, shared := c.requestGroup.Do(key, func() (any, error) {
		log.Printf("[DB FETCH] Mengambil data asli untuk %s dari Database...", key)
		
		// Panggil fungsi asli untuk ambil data dari DB
		data, err := fetchFunc()
		if err != nil {
			return nil, err
		}

		// Simpan ke Cache
		dataBytes, err := json.Marshal(data)
		if err == nil {
			if err := c.client.Set(ctx, key, dataBytes, ttl).Err(); err != nil {
				log.Printf("[CACHE SET ERROR] Gagal menyimpan ke cache: %v", err)
			} else {
				log.Printf("[CACHE SET] Berhasil menyimpan %s ke Redis", key)
			}
		}

		return data, nil
	})

	if err != nil {
		return nil, err
	}

	if shared {
		log.Printf("[SINGLEFLIGHT] %s dilayani dari hasil share Goroutine lain!", key)
	}

	return v, nil
}
