package main

import (
	"context"
	"net/http"
	"strconv"
	"time"

	"github.com/labstack/echo/v5"
	"github.com/redis/go-redis/v9"
)

const luaScript = `
-- KEYS[1] = key
-- ARGV[1] = capacity
-- ARGV[2] = refill_rate_per_ms
-- ARGV[3] = now_ms

local data = redis.call("HMGET", KEYS[1], "tokens", "ts")

local tokens = tonumber(data[1])
local ts = tonumber(data[2])

if tokens == nil then
  tokens = tonumber(ARGV[1])
  ts = tonumber(ARGV[3])
end

local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local delta = math.max(0, now - ts)
local refill = delta * rate

tokens = math.min(capacity, tokens + refill)

local allowed = 0
if tokens >= 1 then
  tokens = tokens - 1
  allowed = 1
end

redis.call("HMSET", KEYS[1], "tokens", tokens, "ts", now)
redis.call("PEXPIRE", KEYS[1], 60000)

return allowed
`

func RedisRateLimitMiddleware(
	rdb *redis.Client,
	capacity int,
	refillPerSecond float64,
) echo.MiddlewareFunc {

	script := redis.NewScript(luaScript)

	// token per ms
	refillPerMs := refillPerSecond / 1000.0

	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c *echo.Context) error {

			ip := c.RealIP()
			key := "rl:ip:" + ip

			nowMs := time.Now().UnixMilli()

			ctx, cancel := context.WithTimeout(
				c.Request().Context(),
				200*time.Millisecond,
			)
			defer cancel()

			res, err := script.Run(
				ctx,
				rdb,
				[]string{key},
				strconv.Itoa(capacity),
				strconv.FormatFloat(refillPerMs, 'f', -1, 64),
				strconv.FormatInt(nowMs, 10),
			).Int()

			if err != nil {
				// kalau Redis error, biasanya lebih aman fail-open
				return next(c)
			}

			if res == 0 {
				return c.JSON(http.StatusTooManyRequests, map[string]string{
					"error": "too many requests",
				})
			}

			return next(c)
		}
	}
}

func main() {
	e := echo.New()

	rdb := redis.NewClient(&redis.Options{
		Addr: "localhost:6380",
	})

	e.Use(RedisRateLimitMiddleware(rdb, 10, 1.0))

	e.GET("/", func(c *echo.Context) error {
		return c.String(http.StatusOK, "Hello, World!")
	})

	// e.Logger.Fatal(e.Start(":1323"))
	// if err := e.Start(":1323"); err != nil {
	if err := e.Start(":8080"); err != nil {
		e.Logger.Error("failed to start server", "error", err)
	}
}
