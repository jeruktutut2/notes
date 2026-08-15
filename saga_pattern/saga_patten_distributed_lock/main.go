package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"time"

	"saga-watchdog-demo/pkg/db"
	"saga-watchdog-demo/pkg/lock"
	"saga-watchdog-demo/pkg/saga"

	"github.com/google/uuid"
	"github.com/labstack/echo/v5"
	"github.com/redis/go-redis/v9"
)

type App struct {
	db           *db.DB
	redisClient  *redis.Client
	watchdogMgr  *lock.WatchdogManager
	orchestrator *saga.SagaOrchestrator
}

func main() {
	pgDSN := getEnv("POSTGRES_DSN", "postgres://postgres:postgres@pgbouncer:6436/saga_db?sslmode=disable&extra_float_digits=0")
	redisAddr := getEnv("REDIS_ADDR", "redis:6379")
	kafkaBroker := getEnv("KAFKA_BROKERS", "kafka:9092")
	rabbitURL := getEnv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

	log.Println("[MAIN] Starting Saga & Watchdog Demo Server...")

	// 1. Initialize DB via PgBouncer
	var database *db.DB
	var err error
	for i := 0; i < 15; i++ {
		database, err = db.InitDB(pgDSN)
		if err == nil {
			break
		}
		log.Printf("[DB WAIT] Waiting for Postgres/PgBouncer... (%v)", err)
		time.Sleep(2 * time.Second)
	}
	if err != nil {
		log.Fatalf("Fatal: Failed to connect to DB: %v", err)
	}

	// 2. Initialize Redis Client
	rdb := redis.NewClient(&redis.Options{Addr: redisAddr})
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	if err := rdb.Ping(ctx).Err(); err != nil {
		cancel()
		log.Fatalf("Fatal: Failed to connect to Redis: %v", err)
	}
	cancel()
	log.Println("[REDIS] Redis client connected")

	// 3. Initialize Distributed Lock Watchdog Manager
	watchdogMgr := lock.NewWatchdogManager(rdb)

	// 4. Initialize Saga Orchestrator
	var orchestrator *saga.SagaOrchestrator
	for i := 0; i < 15; i++ {
		orchestrator, err = saga.NewSagaOrchestrator(database, []string{kafkaBroker}, rabbitURL)
		if err == nil {
			break
		}
		log.Printf("[SAGA WAIT] Waiting for Kafka & RabbitMQ... (%v)", err)
		time.Sleep(2 * time.Second)
	}
	if err != nil {
		log.Fatalf("Fatal: Failed to initialize Saga Orchestrator: %v", err)
	}
	defer orchestrator.Close()

	app := &App{
		db:           database,
		redisClient:  rdb,
		watchdogMgr:  watchdogMgr,
		orchestrator: orchestrator,
	}

	// 5. Initialize Echo v5
	e := echo.New()

	e.GET("/health", app.handleHealth)
	e.POST("/api/orders", app.handleCreateOrder)
	e.GET("/api/orders/:id", app.handleGetOrder)
	e.POST("/api/lock/demo", app.handleLockWatchdogDemo)

	port := getEnv("PORT", "8080")
	log.Printf("[HTTP SERVER] Listening on port %s", port)
	if err := e.Start(":" + port); err != nil {
		log.Fatalf("Server stopped: %v", err)
	}
}

func (a *App) handleHealth(c *echo.Context) error {
	return c.JSON(http.StatusOK, map[string]interface{}{
		"status":    "healthy",
		"timestamp": time.Now(),
		"services": map[string]string{
			"pgbouncer": "UP",
			"redis":     "UP",
			"kafka":     "UP",
			"rabbitmq":  "UP",
		},
	})
}

// handleCreateOrder executes Saga transaction wrapped inside a Distributed Lock with Watchdog Heartbeat.
func (a *App) handleCreateOrder(c *echo.Context) error {
	var req saga.OrderRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request body"})
	}

	if req.ProductID == "" {
		req.ProductID = "PROD-101"
	}
	if req.Quantity <= 0 {
		req.Quantity = 1
	}
	if req.TotalPrice <= 0 {
		req.TotalPrice = 99.99
	}

	lockKey := "lock:product:" + req.ProductID
	ctx := c.Request().Context()

	// Acquire Distributed Lock with 3 seconds TTL and 1 second Watchdog Heartbeat interval
	distributedLock, err := a.watchdogMgr.Acquire(ctx, lockKey, 3*time.Second, 1*time.Second)
	if err != nil {
		return c.JSON(http.StatusConflict, map[string]string{
			"error":   "Conflict: Product is currently locked by another active transaction",
			"lockKey": lockKey,
		})
	}
	defer distributedLock.Unlock(ctx)

	orderID := "ORD-" + uuid.New().String()[:8]
	result, err := a.orchestrator.ExecuteSaga(ctx, orderID, req)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}

	return c.JSON(http.StatusOK, result)
}

func (a *App) handleGetOrder(c *echo.Context) error {
	id := c.Param("id")
	order, err := a.db.GetOrder(id)
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "Order not found"})
	}
	return c.JSON(http.StatusOK, order)
}

// handleLockWatchdogDemo explicitly demonstrates Distributed Lock with Heartbeat Watchdog.
// It acquires a lock with 3 seconds initial TTL and holds it for 8 seconds while background Watchdog renews it.
func (a *App) handleLockWatchdogDemo(c *echo.Context) error {
	lockKey := "demo:critical-resource"
	durationStr := c.QueryParam("duration")
	holdDuration := 8 * time.Second
	if durationStr == "long" {
		holdDuration = 12 * time.Second
	}

	ctx := c.Request().Context()
	log.Printf("[DEMO] Attempting to acquire distributed lock for %s...", lockKey)

	// Acquire lock with 3s TTL and 1s Watchdog heartbeat
	l, err := a.watchdogMgr.Acquire(ctx, lockKey, 3*time.Second, 1*time.Second)
	if err != nil {
		log.Printf("[DEMO REJECTED ✖] Failed to acquire lock %s: %v", lockKey, err)
		return c.JSON(http.StatusLocked, map[string]string{
			"status":  "LOCKED",
			"message": "Resource is currently locked by Watchdog. Try again after the processing finishes.",
			"lockKey": lockKey,
		})
	}
	defer l.Unlock(ctx)

	log.Printf("[DEMO PROCESSING] Lock acquired! Processing critical section for %v (Watchdog extending TTL every 1s)...", holdDuration)
	
	// Simulate long-running task longer than original 3s TTL
	time.Sleep(holdDuration)

	log.Printf("[DEMO COMPLETED] Finished critical work for %s", lockKey)

	return c.JSON(http.StatusOK, map[string]interface{}{
		"status":       "SUCCESS",
		"message":      "Critical section executed safely. Distributed Lock Watchdog renewed lock continuously.",
		"lockKey":      lockKey,
		"heldDuration": holdDuration.String(),
	})
}

func getEnv(key, defaultVal string) string {
	if val, ok := os.LookupEnv(key); ok {
		return val
	}
	return defaultVal
}
