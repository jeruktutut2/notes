package lock

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"time"

	"github.com/redis/go-redis/v9"
)

// Lua script atomic release lock
// Memastikan hanya pemilik token yang dapat menghapus lock tersebut.
var unlockLuaScript = redis.NewScript(`
if redis.call("get", KEYS[1]) == ARGV[1] then
	return redis.call("del", KEYS[1])
else
	return 0
end
`)

type RedisLockManager struct {
	client *redis.Client
}

func NewRedisLockManager(client *redis.Client) *RedisLockManager {
	return &RedisLockManager{client: client}
}

// AcquireLock mencoba mendapatkan lock menggunakan SET key value NX PX ttl
func (r *RedisLockManager) AcquireLock(ctx context.Context, key string, ttl time.Duration) (string, bool, error) {
	// Generate random token unik untuk goroutine/request ini
	tokenBytes := make([]byte, 16)
	if _, err := rand.Read(tokenBytes); err != nil {
		return "", false, err
	}
	token := hex.EncodeToString(tokenBytes)

	// SET key token NX PX ttl
	success, err := r.client.SetNX(ctx, key, token, ttl).Result()
	if err != nil {
		return "", false, err
	}

	if !success {
		return "", false, nil
	}

	return token, true, nil
}

// ReleaseLock melepas lock secara atomic menggunakan Lua Script
func (r *RedisLockManager) ReleaseLock(ctx context.Context, key string, token string) (bool, error) {
	res, err := unlockLuaScript.Run(ctx, r.client, []string{key}, token).Int64()
	if err != nil {
		return false, err
	}
	return res == 1, nil
}

// LockGuard mengelola lifecycle lock beserta background Watchdog Goroutine
type LockGuard struct {
	key      string
	token    string
	mgr      *RedisLockManager
	stopChan chan struct{}
}

// AcquireLockWithWatchdog mengambil lock dan menjalankan Watchdog Heartbeat
// yang secara berkala memperpanjang TTL kunci di Redis selama proses Go masih berjalan.
func (r *RedisLockManager) AcquireLockWithWatchdog(ctx context.Context, key string, ttl time.Duration) (*LockGuard, bool, error) {
	token, acquired, err := r.AcquireLock(ctx, key, ttl)
	if err != nil || !acquired {
		return nil, acquired, err
	}

	guard := &LockGuard{
		key:      key,
		token:    token,
		mgr:      r,
		stopChan: make(chan struct{}),
	}

	// Menjalankan Watchdog Heartbeat di background goroutine
	// Memperpanjang TTL setiap 1/3 dari durasi TTL (misal: tiap ~1.6 detik untuk TTL 5 detik)
	interval := ttl / 3
	go func() {
		ticker := time.NewTicker(interval)
		defer ticker.Stop()

		for {
			select {
			case <-ticker.C:
				// Perpanjang TTL kunci di Redis jika token masih sesuai
				r.client.Expire(context.Background(), key, ttl)
			case <-guard.stopChan:
				return
			}
		}
	}()

	return guard, true, nil
}

// Release menghentikan Watchdog Heartbeat dan melepas lock di Redis
func (g *LockGuard) Release(ctx context.Context) (bool, error) {
	close(g.stopChan)
	return g.mgr.ReleaseLock(ctx, g.key, g.token)
}
