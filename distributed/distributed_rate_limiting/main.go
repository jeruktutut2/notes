package main

import (
	"log"
	"net/http"
	"os"

	"distributed_rate_limiting/internal/limiter"

	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()

	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "redis://localhost:6380/0"
	}

	tokenBucket := limiter.NewTokenBucketLimiter(redisURL)

	// Middleware Rate Limiter (Token Bucket)
	e.Use(func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			// Kita batasi berdasarkan IP Address
			ip := c.RealIP()
			limitKey := "rate_limit:ip:" + ip

			// Konfigurasi Token Bucket:
			// Capacity (Max Burst) = 5 token
			// Refill Rate = 1 token per detik
			capacity := 5
			refillRate := 1
			requestedToken := 1

			allowed, tokensLeft, err := tokenBucket.Allow(c.Request().Context(), limitKey, capacity, refillRate, requestedToken)
			if err != nil {
				log.Printf("Error rate limiter: %v", err)
				return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Internal Server Error"})
			}

			// Masukkan info sisa token ke HTTP Header (Best Practice API)
			c.Response().Header().Set("X-RateLimit-Limit", "5")
			c.Response().Header().Set("X-RateLimit-Remaining", string(rune(tokensLeft+'0')))

			if !allowed {
				return c.JSON(http.StatusTooManyRequests, map[string]string{
					"error": "Terlalu banyak request. Silakan coba lagi nanti.",
				})
			}

			return next(c)
		}
	})

	e.GET("/api/data", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{
			"message": "Berhasil mengakses data penting!",
		})
	})

	log.Println("Server berjalan di port :8080")
	if err := e.Start(":8080"); err != nil {
		log.Fatalf("Server berhenti: %v", err)
	}
}
