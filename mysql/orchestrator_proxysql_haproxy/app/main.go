package main

import (
	"log"
	"net/http"
	"os"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"

	"orchestrator_proxysql_haproxy/app/db"
	"orchestrator_proxysql_haproxy/app/handlers"
)

func main() {
	log.Println("🚀 Initializing Golang Echo v5 REST API Application (HAProxy + ProxySQL + Orchestrator)...")

	dbClient, err := db.InitDB()
	if err != nil {
		log.Fatalf("❌ Database initialization error: %v", err)
	}

	e := echo.New()

	// Middleware
	e.Use(middleware.RequestLogger())
	e.Use(middleware.Recover())

	// Handlers
	handler := handlers.NewEmployeeHandler(dbClient)

	// Routes
	e.GET("/api/health", handler.HealthCheck)
	e.GET("/api/employees", handler.GetEmployees)
	e.POST("/api/employees", handler.CreateEmployee)
	e.POST("/api/employees/transaction", handler.ExecuteTransaction)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("⚡ Server running on http://0.0.0.0:%s", port)
	if err := e.Start(":" + port); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server shutdown error: %v", err)
	}
}
