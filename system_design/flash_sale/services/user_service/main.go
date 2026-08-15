package main

import (
	"database/sql"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	_ "github.com/lib/pq"
)

type User struct {
	ID        string    `json:"id"`
	Email     string    `json:"email"`
	Name      string    `json:"name"`
	Phone     string    `json:"phone"`
	CreatedAt time.Time `json:"created_at"`
}

type CreateUserRequest struct {
	Email string `json:"email"`
	Name  string `json:"name"`
	Phone string `json:"phone"`
}

var db *sql.DB

func main() {
	var err error
	dbHost := os.Getenv("DB_HOST")
	if dbHost == "" {
		dbHost = "pgbouncer"
	}
	dbPort := os.Getenv("DB_PORT")
	if dbPort == "" {
		dbPort = "6432"
	}
	connStr := fmt.Sprintf("host=%s port=%s user=postgres password=postgres dbname=flash_sale_db sslmode=disable", dbHost, dbPort)

	for i := 0; i < 10; i++ {
		db, err = sql.Open("postgres", connStr)
		if err == nil && db.Ping() == nil {
			break
		}
		time.Sleep(2 * time.Second)
	}

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP", "service": "user_service"})
	})

	e.GET("/api/v1/users", listUsers)
	e.GET("/api/v1/users/:id", getUserByID)
	e.POST("/api/v1/users", createUser)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}
	e.Logger.Fatal(e.Start(":" + port))
}

func listUsers(c echo.Context) error {
	rows, err := db.Query("SELECT id, email, name, phone, created_at FROM users ORDER BY created_at DESC")
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	defer rows.Close()

	users := []User{}
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Email, &u.Name, &u.Phone, &u.CreatedAt); err != nil {
			continue
		}
		users = append(users, u)
	}
	return c.JSON(http.StatusOK, users)
}

func getUserByID(c echo.Context) error {
	id := c.Param("id")
	var u User
	err := db.QueryRow("SELECT id, email, name, phone, created_at FROM users WHERE id = $1", id).
		Scan(&u.ID, &u.Email, &u.Name, &u.Phone, &u.CreatedAt)
	if err != nil {
		if err == sql.ErrNoRows {
			return c.JSON(http.StatusNotFound, map[string]string{"error": "User not found"})
		}
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, u)
}

func createUser(c echo.Context) error {
	var req CreateUserRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request body"})
	}

	newID := uuid.New().String()
	_, err := db.Exec("INSERT INTO users (id, email, name, phone, password_hash) VALUES ($1, $2, $3, $4, 'hashed_default')",
		newID, req.Email, req.Name, req.Phone)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}

	return c.JSON(http.StatusCreated, map[string]string{"id": newID, "email": req.Email, "name": req.Name})
}
