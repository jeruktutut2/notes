package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
)

type Transaction struct {
	ID        int       `json:"id"`
	Amount    float64   `json:"amount"`
	Notes     string    `json:"notes"`
	CreatedAt time.Time `json:"created_at"`
}

func main() {
	e := echo.New()
	e.Use(middleware.Recover())

	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		dbURL = "postgres://myuser:mypassword@localhost:6432/mydb"
	}

	// Connect to database (PgBouncer)
	dbpool, err := pgxpool.New(context.Background(), dbURL)
	if err != nil {
		log.Fatalf("Unable to create connection pool: %v\n", err)
	}
	defer dbpool.Close()

	// Initialize Table if not exists
	initSQL := `
	CREATE TABLE IF NOT EXISTS transactions (
		id SERIAL PRIMARY KEY,
		amount NUMERIC(10, 2) NOT NULL,
		notes TEXT,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);
	`
	_, err = dbpool.Exec(context.Background(), initSQL)
	if err != nil {
		log.Fatalf("Unable to initialize table: %v\n", err)
	}

	e.POST("/transactions", func(c *echo.Context) error {
		var req struct {
			Amount float64 `json:"amount"`
			Notes  string  `json:"notes"`
		}
		if err := c.Bind(&req); err != nil {
			return err
		}

		var id int
		err := dbpool.QueryRow(context.Background(),
			"INSERT INTO transactions (amount, notes) VALUES ($1, $2) RETURNING id",
			req.Amount, req.Notes).Scan(&id)

		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}

		return c.JSON(http.StatusCreated, map[string]interface{}{
			"message": "Transaction created",
			"id":      id,
		})
	})

	e.GET("/transactions", func(c *echo.Context) error {
		rows, err := dbpool.Query(context.Background(), "SELECT id, amount, notes, created_at FROM transactions ORDER BY created_at DESC LIMIT 50")
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
		}
		defer rows.Close()

		var txs []Transaction
		for rows.Next() {
			var t Transaction
			if err := rows.Scan(&t.ID, &t.Amount, &t.Notes, &t.CreatedAt); err != nil {
				return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
			}
			txs = append(txs, t)
		}

		return c.JSON(http.StatusOK, txs)
	})

	log.Fatal(e.Start(":8080"))
}
