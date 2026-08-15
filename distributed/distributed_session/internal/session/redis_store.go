package session

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

type UserSession struct {
	UserID    string `json:"user_id"`
	Username  string `json:"username"`
	Role      string `json:"role"`
	LoginTime string `json:"login_time"`
}

type RedisSessionStore struct {
	client *redis.Client
}

func NewRedisSessionStore(redisURL string) *RedisSessionStore {
	opts, err := redis.ParseURL(redisURL)
	if err != nil {
		log.Fatalf("Gagal mem-parse Redis URL: %v", err)
	}

	client := redis.NewClient(opts)
	return &RedisSessionStore{client: client}
}

// CreateSession menyimpan data session ke Redis dengan Time-To-Live (TTL).
func (s *RedisSessionStore) CreateSession(ctx context.Context, sessionID string, data UserSession, ttl time.Duration) error {
	dataBytes, err := json.Marshal(data)
	if err != nil {
		return err
	}
	
	key := "session:" + sessionID
	return s.client.Set(ctx, key, dataBytes, ttl).Err()
}

// GetSession mengambil dan memvalidasi session dari Redis.
func (s *RedisSessionStore) GetSession(ctx context.Context, sessionID string) (*UserSession, error) {
	key := "session:" + sessionID
	val, err := s.client.Get(ctx, key).Result()
	if err != nil {
		return nil, err // Mengembalikan redis.Nil jika session expired/tidak ada
	}

	var data UserSession
	if err := json.Unmarshal([]byte(val), &data); err != nil {
		return nil, err
	}
	return &data, nil
}

// DestroySession menghapus session secara eksplisit (Logout).
func (s *RedisSessionStore) DestroySession(ctx context.Context, sessionID string) error {
	key := "session:" + sessionID
	return s.client.Del(ctx, key).Err()
}

// RefreshSession (Sliding Expiration) mereset TTL agar user tetap login jika aktif.
func (s *RedisSessionStore) RefreshSession(ctx context.Context, sessionID string, ttl time.Duration) error {
	key := "session:" + sessionID
	return s.client.Expire(ctx, key, ttl).Err()
}
