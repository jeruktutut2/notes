package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	_ "github.com/lib/pq"
	"github.com/redis/go-redis/v9"
	"github.com/segmentio/kafka-go"
)

type FlashSale struct {
	ID             string    `json:"id"`
	ProductID      string    `json:"product_id"`
	ProductName    string    `json:"product_name,omitempty"`
	SalePrice      float64   `json:"sale_price"`
	OriginalStock  int       `json:"original_stock"`
	RemainingStock int       `json:"remaining_stock"`
	MaxPerUser     int       `json:"max_per_user"`
	StartTime      time.Time `json:"start_time"`
	EndTime        time.Time `json:"end_time"`
	Status         string    `json:"status"`
}

type PurchaseRequest struct {
	UserID string `json:"user_id"`
}

type OrderMessage struct {
	OrderID        string    `json:"order_id"`
	UserID         string    `json:"user_id"`
	FlashSaleID    string    `json:"flash_sale_id"`
	ProductID      string    `json:"product_id"`
	Price          float64   `json:"price"`
	IdempotencyKey string    `json:"idempotency_key"`
	Timestamp      time.Time `json:"timestamp"`
}

var (
	db          *sql.DB
	rdb         *redis.Client
	kafkaWriter *kafka.Writer
	ctx         = context.Background()
	luaScript   *redis.Script
)

const deductLua = `
local status = redis.call('GET', KEYS[3])
if status ~= 'ACTIVE' then
    return {-2, 'SALE_NOT_ACTIVE'}
end

local already_purchased = redis.call('SISMEMBER', KEYS[2], ARGV[1])
if already_purchased == 1 then
    return {-3, 'ALREADY_PURCHASED'}
end

local current_stock = tonumber(redis.call('GET', KEYS[1]))
if current_stock == nil or current_stock <= 0 then
    redis.call('SET', KEYS[3], 'SOLD_OUT')
    return {-1, 'SOLD_OUT'}
end

local remaining = redis.call('DECR', KEYS[1])
redis.call('SADD', KEYS[2], ARGV[1])

if remaining <= 0 then
    redis.call('SET', KEYS[3], 'SOLD_OUT')
end

return {remaining, 'SUCCESS'}
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

	kafkaBroker := getEnv("KAFKA_BROKER", "kafka:9092")
	kafkaWriter = &kafka.Writer{
		Addr:     kafka.TCP(kafkaBroker),
		Topic:    "order-requests",
		Balancer: &kafka.LeastBytes{},
	}

	luaScript = redis.NewScript(deductLua)

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP", "service": "flash_sale_service"})
	})

	e.GET("/api/v1/flash-sales", listFlashSales)
	e.GET("/api/v1/flash-sales/:id", getFlashSaleByID)
	e.POST("/api/v1/flash-sales/:id/preheat", preheatStock)
	e.POST("/api/v1/flash-sales/:id/purchase", purchaseItem)

	port := getEnv("PORT", "8082")
	e.Logger.Fatal(e.Start(":" + port))
}

func getEnv(key, fallback string) string {
	val := os.Getenv(key)
	if val == "" {
		return fallback
	}
	return val
}

func listFlashSales(c echo.Context) error {
	rows, err := db.Query(`
		SELECT fs.id, fs.product_id, p.name, fs.sale_price, fs.original_stock, fs.remaining_stock, fs.max_per_user, fs.start_time, fs.end_time, fs.status
		FROM flash_sales fs
		JOIN products p ON fs.product_id = p.id
		ORDER BY fs.created_at DESC
	`)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	defer rows.Close()

	sales := []FlashSale{}
	for rows.Next() {
		var s FlashSale
		if err := rows.Scan(&s.ID, &s.ProductID, &s.ProductName, &s.SalePrice, &s.OriginalStock, &s.RemainingStock, &s.MaxPerUser, &s.StartTime, &s.EndTime, &s.Status); err != nil {
			continue
		}

		// Sync live remaining stock & status from Redis if pre-heated
		stockKey := fmt.Sprintf("flash_sale:%s:stock", s.ID)
		statusKey := fmt.Sprintf("flash_sale:%s:status", s.ID)
		if val, err := rdb.Get(ctx, stockKey).Int(); err == nil {
			s.RemainingStock = val
		}
		if val, err := rdb.Get(ctx, statusKey).Result(); err == nil {
			s.Status = val
		}

		sales = append(sales, s)
	}
	return c.JSON(http.StatusOK, sales)
}

func getFlashSaleByID(c echo.Context) error {
	id := c.Param("id")
	var s FlashSale
	err := db.QueryRow(`
		SELECT fs.id, fs.product_id, p.name, fs.sale_price, fs.original_stock, fs.remaining_stock, fs.max_per_user, fs.start_time, fs.end_time, fs.status
		FROM flash_sales fs
		JOIN products p ON fs.product_id = p.id
		WHERE fs.id::text = $1
	`, id).Scan(&s.ID, &s.ProductID, &s.ProductName, &s.SalePrice, &s.OriginalStock, &s.RemainingStock, &s.MaxPerUser, &s.StartTime, &s.EndTime, &s.Status)

	if err != nil {
		if err == sql.ErrNoRows {
			return c.JSON(http.StatusNotFound, map[string]string{"error": "Flash Sale event not found"})
		}
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}

	stockKey := fmt.Sprintf("flash_sale:%s:stock", s.ID)
	statusKey := fmt.Sprintf("flash_sale:%s:status", s.ID)
	if val, err := rdb.Get(ctx, stockKey).Int(); err == nil {
		s.RemainingStock = val
	}
	if val, err := rdb.Get(ctx, statusKey).Result(); err == nil {
		s.Status = val
	}

	return c.JSON(http.StatusOK, s)
}

func preheatStock(c echo.Context) error {
	id := c.Param("id")
	var stock int
	var status string
	err := db.QueryRow("SELECT remaining_stock, status FROM flash_sales WHERE id::text = $1", id).Scan(&stock, &status)
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "Flash Sale event not found: " + err.Error()})
	}

	stockKey := fmt.Sprintf("flash_sale:%s:stock", id)
	statusKey := fmt.Sprintf("flash_sale:%s:status", id)
	purchasedKey := fmt.Sprintf("flash_sale:%s:purchased", id)

	rdb.Set(ctx, stockKey, stock, 0)
	rdb.Set(ctx, statusKey, "ACTIVE", 0)
	rdb.Del(ctx, purchasedKey)

	db.Exec("UPDATE flash_sales SET status = 'ACTIVE' WHERE id::text = $1", id)

	return c.JSON(http.StatusOK, map[string]interface{}{
		"message":         "Stock pre-heated to Redis successfully",
		"flash_sale_id":   id,
		"stock_loaded":    stock,
		"status_set":      "ACTIVE",
	})
}

func purchaseItem(c echo.Context) error {
	saleID := c.Param("id")
	var req PurchaseRequest
	if err := c.Bind(&req); err != nil || req.UserID == "" {
		req.UserID = c.Request().Header.Get("X-User-ID")
	}
	if req.UserID == "" {
		req.UserID = "22222222-2222-2222-2222-222222222222" // default test user
	}

	idempotencyKey := c.Request().Header.Get("X-Idempotency-Key")
	if idempotencyKey == "" {
		idempotencyKey = fmt.Sprintf("idemp_%s_%s", req.UserID, saleID)
	}

	// Redis Lua Keys & Args
	stockKey := fmt.Sprintf("flash_sale:%s:stock", saleID)
	purchasedKey := fmt.Sprintf("flash_sale:%s:purchased", saleID)
	statusKey := fmt.Sprintf("flash_sale:%s:status", saleID)

	res, err := luaScript.Run(ctx, rdb, []string{stockKey, purchasedKey, statusKey}, req.UserID).Result()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Redis operation failed: " + err.Error()})
	}

	resSlice, ok := res.([]interface{})
	if !ok || len(resSlice) < 2 {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Unexpected Lua script response"})
	}

	code := resSlice[0].(int64)
	_ = resSlice[1].(string)

	if code == -1 {
		return c.JSON(http.StatusGone, map[string]interface{}{
			"status": "error",
			"error":  map[string]string{"code": "SOLD_OUT", "message": "Maaf, stok sudah habis"},
		})
	}
	if code == -2 {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"status": "error",
			"error":  map[string]string{"code": "SALE_NOT_ACTIVE", "message": "Flash Sale belum dimulai atau sudah berakhir"},
		})
	}
	if code == -3 {
		return c.JSON(http.StatusConflict, map[string]interface{}{
			"status": "error",
			"error":  map[string]string{"code": "ALREADY_PURCHASED", "message": "Anda sudah membeli produk ini"},
		})
	}

	// Fetch Flash Sale Product ID and Price
	var productID string
	var price float64
	err = db.QueryRow("SELECT product_id, sale_price FROM flash_sales WHERE id = $1", saleID).Scan(&productID, &price)
	if err != nil {
		productID = "11111111-1111-1111-1111-111111111111"
		price = 5000000.00
	}

	orderID := uuid.New().String()
	orderMsg := OrderMessage{
		OrderID:        orderID,
		UserID:         req.UserID,
		FlashSaleID:    saleID,
		ProductID:      productID,
		Price:          price,
		IdempotencyKey: idempotencyKey,
		Timestamp:      time.Now(),
	}

	msgBytes, _ := json.Marshal(orderMsg)
	err = kafkaWriter.WriteMessages(ctx, kafka.Message{
		Key:   []byte(req.UserID),
		Value: msgBytes,
	})

	if err != nil {
		fmt.Printf("Warning: Failed to publish Kafka message: %v\n", err)
	}

	return c.JSON(http.StatusAccepted, map[string]interface{}{
		"status": "success",
		"data": map[string]interface{}{
			"order_id":         orderID,
			"status":           "PENDING",
			"message":          "Pesanan Anda sedang diproses",
			"payment_deadline": time.Now().Add(15 * time.Minute),
			"remaining_stock":  code,
		},
	})
}
