package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"drc-app/config"
	"drc-app/handler"
	appMiddleware "drc-app/middleware"
	"drc-app/repository"

	"github.com/labstack/echo/v5"
)

var version = "1.0.0"

func main() {
	log.Printf("==================================================")
	log.Printf("  Data Recovery Center (DRC) - Golang Echo v5 App")
	log.Printf("  Version: %s", version)
	log.Printf("==================================================")

	cfg := config.LoadConfig()

	repo, err := repository.NewRepository(cfg)
	if err != nil {
		log.Fatalf("Failed to initialize repository: %v", err)
	}
	defer repo.Close()

	h := handler.NewHandler(repo)

	e := echo.New()
	e.HideBanner = true

	// Custom Middleware
	e.Use(appMiddleware.Logger())

	// Routes
	e.GET("/", func(c echo.Context) error {
		return c.JSON(http.StatusOK, echo.Map{
			"app":           "Data Recovery Center Learning App",
			"version":       version,
			"framework":     "Echo v5",
			"active_target": repo.GetActiveTarget(),
			"endpoints": []string{
				"GET  /health",
				"GET  /api/status",
				"GET  /api/replication",
				"GET  /api/data",
				"POST /api/data",
				"GET  /api/data/:id",
				"GET  /api/logs",
				"POST /api/failover",
				"POST /api/failback",
			},
		})
	})

	e.GET("/health", h.Health)

	api := e.Group("/api")
	api.GET("/status", h.GetStatus)
	api.GET("/replication", h.GetReplication)
	api.GET("/data", h.ListData)
	api.POST("/data", h.CreateData)
	api.GET("/data/:id", h.GetDataByID)
	api.GET("/logs", h.GetLogs)
	api.POST("/failover", h.Failover)
	api.POST("/failback", h.Failback)

	// Graceful shutdown
	go func() {
		addr := ":" + cfg.Port
		log.Printf("[INFO] Server starting on %s (Active Target: %s)", addr, cfg.ActiveDB)
		if err := e.Start(addr); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Shutting down server: %v", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	<-quit

	log.Println("[INFO] Shutting down gracefully...")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := e.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("[INFO] Server stopped clean")
}
