package limiter

import (
	"context"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

// Script Lua untuk mengeksekusi logika Token Bucket secara Atomic di Redis.
// Hal ini mencegah race condition saat ratusan instance mengakses bucket yang sama.
const luaTokenBucket = `
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refillRate = tonumber(ARGV[2]) -- token per detik
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- Ambil data bucket (tokens dan timestamp terakhir diupdate)
local bucket = redis.call("HMGET", key, "tokens", "last_update")
local tokens = tonumber(bucket[1])
local last_update = tonumber(bucket[2])

if tokens == nil then
    tokens = capacity
    last_update = now
end

-- Hitung token yang harus di-refill sejak update terakhir
local time_passed = math.max(0, now - last_update)
local new_tokens = math.floor(time_passed * refillRate)

tokens = math.min(capacity, tokens + new_tokens)

-- Jika token mencukupi, potong token
local allowed = 0
if tokens >= requested then
    tokens = tokens - requested
    allowed = 1
end

-- Simpan state bucket kembali
redis.call("HMSET", key, "tokens", tokens, "last_update", now)
redis.call("EXPIRE", key, math.ceil(capacity / refillRate) * 2)

return {allowed, tokens}
`

type TokenBucketLimiter struct {
	client *redis.Client
	script *redis.Script
}

func NewTokenBucketLimiter(redisURL string) *TokenBucketLimiter {
	opts, err := redis.ParseURL(redisURL)
	if err != nil {
		log.Fatalf("Gagal mem-parse Redis URL: %v", err)
	}

	client := redis.NewClient(opts)

	// Pre-load Lua Script ke memory Redis (meningkatkan performa)
	script := redis.NewScript(luaTokenBucket)

	return &TokenBucketLimiter{
		client: client,
		script: script,
	}
}

// Allow mengecek apakah request diizinkan berdasarkan sisa token.
func (l *TokenBucketLimiter) Allow(ctx context.Context, key string, capacity, refillRate, requested int) (bool, int, error) {
	now := time.Now().Unix()

	// Eksekusi script Lua
	result, err := l.script.Run(ctx, l.client, []string{key}, capacity, refillRate, now, requested).Result()
	if err != nil {
		return false, 0, err
	}

	// Parsing hasil Lua Script (mengembalikan array: [allowed(0/1), tokens_left])
	resArr := result.([]interface{})
	allowedInt := resArr[0].(int64)
	tokensLeft := resArr[1].(int64)

	return allowedInt == 1, int(tokensLeft), nil
}
