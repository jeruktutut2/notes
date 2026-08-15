package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/labstack/echo/v5"
	"golang.org/x/time/rate"
)

type IPRateLimiter struct {
	limiters map[string]*rate.Limiter
	mu       sync.Mutex
	rate     rate.Limit
	burst    int
}

func NewIPRateLimiter(r rate.Limit, b int) *IPRateLimiter {
	return &IPRateLimiter{
		limiters: make(map[string]*rate.Limiter),
		rate:     r,
		burst:    b,
	}
}

func (i *IPRateLimiter) getLimiter(ip string) *rate.Limiter {
	i.mu.Lock()
	defer i.mu.Unlock()

	limiter, exists := i.limiters[ip]
	if !exists {
		limiter = rate.NewLimiter(i.rate, i.burst)
		i.limiters[ip] = limiter
	}

	return limiter
}

func RateLimitMiddleware(limiter *IPRateLimiter) echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c *echo.Context) error {
			ip := c.RealIP()

			l := limiter.getLimiter(ip)
			if !l.Allow() {
				return c.JSON(http.StatusTooManyRequests, map[string]string{
					"error": "too many requests",
				})
			}

			return next(c)
		}
	}
}

func main() {
	// fmt.Println("Hello World")
	e := echo.New()

	// Create rate limiter: 1 request per second, burst of 5
	limiter := NewIPRateLimiter(1, 5)

	// Apply rate limiting middleware to all routes
	e.Use(RateLimitMiddleware(limiter))

	// Test endpoint
	e.POST("/api/v1/test", func(c *echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{
			"message": "success",
		})
	})

	// e.Start(":8080")

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	sc := echo.StartConfig{
		Address:         ":8080",
		GracefulTimeout: 10 * time.Second,
	}

	if err := sc.Start(ctx, e); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Server stopped")
}
