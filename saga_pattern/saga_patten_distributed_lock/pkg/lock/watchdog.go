package lock

import (
	"context"
	"errors"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
)

var (
	ErrLockAcquireFailed = errors.New("failed to acquire distributed lock")
	
	// Lua script to extend lock TTL only if the value (owner token) matches
	extendScript = redis.NewScript(`
		if redis.call("get", KEYS[1]) == ARGV[1] then
			return redis.call("pexpire", KEYS[1], ARGV[2])
		else
			return 0
		end
	`)

	// Lua script to safely release lock only if owner token matches
	releaseScript = redis.NewScript(`
		if redis.call("get", KEYS[1]) == ARGV[1] then
			return redis.call("del", KEYS[1])
		else
			return 0
		end
	`)
)

type Lock struct {
	client            *redis.Client
	key               string
	value             string
	ttl               time.Duration
	heartbeatInterval time.Duration
	stopChan          chan struct{}
	doneChan          chan struct{}
	mu                sync.Mutex
	isUnlocked        bool
}

type WatchdogManager struct {
	client *redis.Client
}

func NewWatchdogManager(client *redis.Client) *WatchdogManager {
	return &WatchdogManager{client: client}
}

// Acquire acquires a distributed lock in Redis and starts a background Watchdog Heartbeat.
// The Watchdog periodically extends the lock's TTL while the critical work is actively executing.
func (wm *WatchdogManager) Acquire(ctx context.Context, key string, initialTTL time.Duration, heartbeatInterval time.Duration) (*Lock, error) {
	token := uuid.New().String()

	// Try acquiring key with NX (Only set if Not eXists) and initial TTL
	success, err := wm.client.SetNX(ctx, key, token, initialTTL).Result()
	if err != nil {
		return nil, fmt.Errorf("redis setnx error: %w", err)
	}
	if !success {
		return nil, ErrLockAcquireFailed
	}

	l := &Lock{
		client:            wm.client,
		key:               key,
		value:             token,
		ttl:               initialTTL,
		heartbeatInterval: heartbeatInterval,
		stopChan:          make(chan struct{}),
		doneChan:          make(chan struct{}),
	}

	// Start background Watchdog Heartbeat goroutine
	go l.startWatchdog()

	log.Printf("[DISTRIBUTED LOCK] Acquired lock '%s' (Token: %s) with initial TTL %v", key, token[:8], initialTTL)
	return l, nil
}

func (l *Lock) startWatchdog() {
	defer close(l.doneChan)

	ticker := time.NewTicker(l.heartbeatInterval)
	defer ticker.Stop()

	for {
		select {
		case <-l.stopChan:
			log.Printf("[WATCHDOG] Stopping heartbeat watchdog for lock '%s'", l.key)
			return
		case <-ticker.C:
			ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
			ttlMs := int64(l.ttl / time.Millisecond)

			res, err := extendScript.Run(ctx, l.client, []string{l.key}, l.value, ttlMs).Result()
			cancel()

			if err != nil {
				log.Printf("[WATCHDOG ERROR] Failed to send heartbeat for lock '%s': %v", l.key, err)
			} else if res.(int64) == 1 {
				log.Printf("[WATCHDOG HEARTBEAT ♥] Extended TTL for lock '%s' to %v", l.key, l.ttl)
			} else {
				log.Printf("[WATCHDOG WARNING] Lock '%s' lost or taken over by another process!", l.key)
				return
			}
		}
	}
}

// Unlock stops the watchdog heartbeat and safely releases the lock in Redis.
func (l *Lock) Unlock(ctx context.Context) error {
	l.mu.Lock()
	if l.isUnlocked {
		l.mu.Unlock()
		return nil
	}
	l.isUnlocked = true
	l.mu.Unlock()

	// Signal watchdog goroutine to stop and wait until done
	close(l.stopChan)
	<-l.doneChan

	res, err := releaseScript.Run(ctx, l.client, []string{l.key}, l.value).Result()
	if err != nil {
		return fmt.Errorf("failed to execute release script: %w", err)
	}

	if res.(int64) == 1 {
		log.Printf("[DISTRIBUTED LOCK] Released lock '%s' successfully", l.key)
	} else {
		log.Printf("[DISTRIBUTED LOCK WARNING] Lock '%s' was already expired or released", l.key)
	}

	return nil
}
