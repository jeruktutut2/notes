package main

import (
	"log"
	"net/http"
	"os"
	"time"

	"distributed_cache/internal/cache"

	"github.com/labstack/echo/v4"
)

// Simulasi query lambat ke database
func ExpensiveDatabaseQuery(productID string) (any, error) {
	time.Sleep(2 * time.Second) // Simulasi loading berat
	
	// Data fiktif hasil query
	data := map[string]any{
		"id":          productID,
		"name":        "Laptop Gaming Gahar",
		"stock":       42,
		"price":       15000000,
		"description": "Barang langka, banyak yang cari!",
	}
	return data, nil
}

func main() {
	e := echo.New()

	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "redis://localhost:6379/0"
	}

	distCache := cache.NewDistributedCache(redisURL)

	e.GET("/product/:id", func(c echo.Context) error {
		productID := c.Param("id")
		cacheKey := "product:" + productID

		// Gunakan DistributedCache dengan durasi TTL 10 detik
		data, err := distCache.FetchData(c.Request().Context(), cacheKey, 10*time.Second, func() (any, error) {
			return ExpensiveDatabaseQuery(productID)
		})

		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{
				"error": "Gagal memproses data",
			})
		}

		return c.JSON(http.StatusOK, map[string]any{
			"message": "Sukses",
			"data":    data,
		})
	})

	log.Println("Server berjalan di port :8080")
	if err := e.Start(":8080"); err != nil {
		log.Fatalf("Server berhenti: %v", err)
	}
}
