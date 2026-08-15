package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	_ "github.com/lib/pq"
)

type User struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

type NodeStatus struct {
	InRecovery bool   `json:"in_recovery"`
	ServerAddr string `json:"server_addr"`
}

type StatusResponse struct {
	WriteNode NodeStatus `json:"write_node"`
	ReadNode  NodeStatus `json:"read_node"`
}

var (
	dbWrite *sql.DB
	dbRead  *sql.DB
)

func initDB() {
	writeDSN := os.Getenv("DB_WRITE_DSN")
	if writeDSN == "" {
		writeDSN = "postgres://appuser:apppassword@pgbouncer:6432/db_write?sslmode=disable"
	}

	readDSN := os.Getenv("DB_READ_DSN")
	if readDSN == "" {
		readDSN = "postgres://appuser:apppassword@pgbouncer:6432/db_read?sslmode=disable"
	}

	var err error
	dbWrite, err = sql.Open("postgres", writeDSN)
	if err != nil {
		log.Fatalf("Failed to open write DB connection: %v", err)
	}

	dbRead, err = sql.Open("postgres", readDSN)
	if err != nil {
		log.Fatalf("Failed to open read DB connection: %v", err)
	}

	dbWrite.SetMaxOpenConns(10)
	dbWrite.SetMaxIdleConns(5)
	dbRead.SetMaxOpenConns(10)
	dbRead.SetMaxIdleConns(5)
}

func getNodeStatus(db *sql.DB) (NodeStatus, error) {
	var status NodeStatus
	query := "SELECT pg_is_in_recovery(), COALESCE(inet_server_addr()::text, 'localhost')"
	err := db.QueryRow(query).Scan(&status.InRecovery, &status.ServerAddr)
	return status, err
}

func main() {
	initDB()
	defer dbWrite.Close()
	defer dbRead.Close()

	e := echo.New()
	e.Use(middleware.Recover())

	e.GET("/health", func(c *echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP"})
	})

	e.GET("/api/status", func(c *echo.Context) error {
		writeStatus, errW := getNodeStatus(dbWrite)
		if errW != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error_write": errW.Error()})
		}
		readStatus, errR := getNodeStatus(dbRead)
		if errR != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error_read": errR.Error()})
		}

		return c.JSON(http.StatusOK, StatusResponse{
			WriteNode: writeStatus,
			ReadNode:  readStatus,
		})
	})

	e.POST("/api/users", func(c *echo.Context) error {
		u := new(User)
		if err := c.Bind(u); err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid request payload"})
		}

		query := "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, created_at"
		err := dbWrite.QueryRow(query, u.Name, u.Email).Scan(&u.ID, &u.CreatedAt)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": fmt.Sprintf("Failed to write to Master: %v", err)})
		}

		return c.JSON(http.StatusCreated, u)
	})

	e.GET("/api/users", func(c *echo.Context) error {
		rows, err := dbRead.Query("SELECT id, name, email, created_at FROM users ORDER BY id DESC")
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": fmt.Sprintf("Failed to read from Replica: %v", err)})
		}
		defer rows.Close()

		users := []User{}
		for rows.Next() {
			var u User
			if err := rows.Scan(&u.ID, &u.Name, &u.Email, &u.CreatedAt); err != nil {
				return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
			}
			users = append(users, u)
		}

		return c.JSON(http.StatusOK, users)
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Starting Echo v5 server on port %s", port)
	if err := e.Start(":" + port); err != nil {
		log.Fatalf("Server stopped with error: %v", err)
	}
}
