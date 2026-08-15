package main

import (
	"context"
	"database/sql"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	_ "github.com/lib/pq"
	"github.com/redis/go-redis/v9"
)

type PayRequest struct {
	PaymentMethod string `json:"payment_method"` // e.g. "CREDIT_CARD", "E_WALLET", "BANK_TRANSFER"
	Action        string `json:"action"`         // "SUCCESS" or "FAIL"
}

var (
	db               *sql.DB
	rdb              *redis.Client
	ctx              = context.Background()
	restoreLuaScript *redis.Script
)

const restoreLua = `
local new_stock = redis.call('INCR', KEYS[1])
redis.call('SREM', KEYS[2], ARGV[1])

local status = redis.call('GET', KEYS[3])
if status == 'SOLD_OUT' and new_stock > 0 then
    redis.call('SET', KEYS[3], 'ACTIVE')
end

return {new_stock, 'RESTORED'}
`

func main() {
	var err error
	dbHost := getEnv("DB_HOST", "pgbouncer")
	dbPort := getEnv("DB_PORT", "6432")
	connStr := fmt.Sprintf("host=%s port=%s user=postgres password=postgres dbname=flash_sale_db sslmode=disable", dbHost, dbPort)

	for i := 0; i < 10; i++ {
		db, err = sql.Open("postgres", connStr)
		if err == nil && db.Ping() == nil {
			break
		}
		time.Sleep(2 * time.Second)
	}

	redisAddr := getEnv("REDIS_ADDR", "redis:6379")
	rdb = redis.NewClient(&redis.Options{Addr: redisAddr})

	restoreLuaScript = redis.NewScript(restoreLua)

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP", "service": "payment_service"})
	})

	e.POST("/api/v1/orders/:id/pay", processPayment)
	e.POST("/api/v1/orders/:id/cancel", cancelOrder)
	e.POST("/api/v1/payments/pay/:id", processPayment)
	e.POST("/api/v1/payments/cancel/:id", cancelOrder)

	port := getEnv("PORT", "8084")
	e.Logger.Fatal(e.Start(":" + port))
}

func getEnv(key, fallback string) string {
	val := os.Getenv(key)
	if val == "" {
		return fallback
	}
	return val
}

func processPayment(c echo.Context) error {
	orderID := c.Param("id")
	var req PayRequest
	if err := c.Bind(&req); err != nil {
		req.Action = "SUCCESS"
		req.PaymentMethod = "E_WALLET"
	}
	if req.Action == "" {
		req.Action = "SUCCESS"
	}
	if req.PaymentMethod == "" {
		req.PaymentMethod = "E_WALLET"
	}

	var userID, flashSaleID, orderStatus string
	var price float64
	err := db.QueryRow("SELECT user_id, flash_sale_id, price, status FROM orders WHERE id = $1", orderID).
		Scan(&userID, &flashSaleID, &price, &orderStatus)

	if err != nil {
		if err == sql.ErrNoRows {
			return c.JSON(http.StatusNotFound, map[string]string{"error": "Order not found"})
		}
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}

	if orderStatus == "PAID" {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Order is already paid"})
	}

	paymentID := uuid.New().String()
	gatewayRef := fmt.Sprintf("PAY-%s", uuid.New().String()[:8])

	if req.Action == "SUCCESS" {
		tx, _ := db.Begin()
		_, err1 := tx.Exec("UPDATE orders SET status = 'PAID', updated_at = NOW() WHERE id = $1", orderID)
		_, err2 := tx.Exec(`
			INSERT INTO payments (id, order_id, amount, payment_method, gateway_ref_id, status, paid_at)
			VALUES ($1, $2, $3, $4, $5, 'SUCCESS', NOW())
		`, paymentID, orderID, price, req.PaymentMethod, gatewayRef)

		if err1 != nil || err2 != nil {
			tx.Rollback()
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Database update failed"})
		}
		tx.Commit()

		return c.JSON(http.StatusOK, map[string]interface{}{
			"status":         "SUCCESS",
			"message":        "Pembayaran berhasil",
			"order_id":       orderID,
			"payment_id":     paymentID,
			"gateway_ref_id": gatewayRef,
		})
	}

	// Action == "FAIL" or Expired
	tx, _ := db.Begin()
	tx.Exec("UPDATE orders SET status = 'PAYMENT_FAILED', updated_at = NOW() WHERE id = $1", orderID)
	tx.Exec(`
		INSERT INTO payments (id, order_id, amount, payment_method, gateway_ref_id, status)
		VALUES ($1, $2, $3, $4, $5, 'FAILED')
	`, paymentID, orderID, price, req.PaymentMethod, gatewayRef)
	tx.Commit()

	// Restore stock in Redis
	stockKey := fmt.Sprintf("flash_sale:%s:stock", flashSaleID)
	purchasedKey := fmt.Sprintf("flash_sale:%s:purchased", flashSaleID)
	statusKey := fmt.Sprintf("flash_sale:%s:status", flashSaleID)

	res, err := restoreLuaScript.Run(ctx, rdb, []string{stockKey, purchasedKey, statusKey}, userID).Result()
	newStock := int64(0)
	if err == nil {
		if resSlice, ok := res.([]interface{}); ok && len(resSlice) > 0 {
			newStock = resSlice[0].(int64)
		}
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"status":          "PAYMENT_FAILED",
		"message":         "Pembayaran gagal, stok telah dikembalikan",
		"order_id":        orderID,
		"restored_stock":  newStock,
	})
}

func cancelOrder(c echo.Context) error {
	orderID := c.Param("id")

	var userID, flashSaleID string
	err := db.QueryRow("SELECT user_id, flash_sale_id FROM orders WHERE id = $1", orderID).Scan(&userID, &flashSaleID)
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "Order not found"})
	}

	db.Exec("UPDATE orders SET status = 'CANCELLED', updated_at = NOW() WHERE id = $1", orderID)

	stockKey := fmt.Sprintf("flash_sale:%s:stock", flashSaleID)
	purchasedKey := fmt.Sprintf("flash_sale:%s:purchased", flashSaleID)
	statusKey := fmt.Sprintf("flash_sale:%s:status", flashSaleID)

	res, _ := restoreLuaScript.Run(ctx, rdb, []string{stockKey, purchasedKey, statusKey}, userID).Result()
	newStock := int64(0)
	if resSlice, ok := res.([]interface{}); ok && len(resSlice) > 0 {
		newStock = resSlice[0].(int64)
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"status":         "CANCELLED",
		"message":        "Order dibatalkan, stok dikembalikan",
		"order_id":       orderID,
		"restored_stock": newStock,
	})
}
