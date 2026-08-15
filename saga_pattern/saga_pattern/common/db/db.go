package db

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	_ "github.com/lib/pq"
)

type DB struct {
	*sql.DB
}

func ConnectDB() (*DB, error) {
	host := getEnv("DB_HOST", "pgbouncer")
	port := getEnv("DB_PORT", "6432")
	user := getEnv("DB_USER", "postgres")
	password := getEnv("DB_PASSWORD", "postgres")
	dbname := getEnv("DB_NAME", "saga_db")

	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		host, port, user, password, dbname)

	var database *sql.DB
	var err error

	// Retry connection to wait for DB & PgBouncer to be ready
	for i := 0; i < 15; i++ {
		database, err = sql.Open("postgres", dsn)
		if err == nil {
			err = database.Ping()
			if err == nil {
				log.Println("Connected to PostgreSQL via PgBouncer successfully!")
				return &DB{database}, nil
			}
		}
		log.Printf("Waiting for DB connection... attempt %d/15 (error: %v)\n", i+1, err)
		time.Sleep(2 * time.Second)
	}

	return nil, fmt.Errorf("failed to connect to DB after retries: %w", err)
}

func getEnv(key, fallback string) string {
	if val, ok := os.LookupEnv(key); ok {
		return val
	}
	return fallback
}

func (db *DB) LogSagaStep(orderID, serviceName, stepName, status, details string) error {
	query := `INSERT INTO saga_logs (order_id, service_name, step_name, status, details) VALUES ($1, $2, $3, $4, $5)`
	_, err := db.Exec(query, orderID, serviceName, stepName, status, details)
	return err
}

func (db *DB) CreateOrder(id, itemID string, qty int, amount float64, sagaType string) error {
	query := `INSERT INTO orders (id, item_id, quantity, total_amount, status, saga_type) VALUES ($1, $2, $3, $4, 'PENDING', $5)`
	_, err := db.Exec(query, id, itemID, qty, amount, sagaType)
	return err
}

func (db *DB) UpdateOrderStatus(id, status string) error {
	query := `UPDATE orders SET status = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2`
	_, err := db.Exec(query, status, id)
	return err
}

func (db *DB) DeductStock(itemID string, qty int) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	var stock int
	err = tx.QueryRow(`SELECT stock FROM inventory WHERE item_id = $1 FOR UPDATE`, itemID).Scan(&stock)
	if err != nil {
		return fmt.Errorf("item not found: %w", err)
	}

	if stock < qty {
		return fmt.Errorf("insufficient stock: current %d, requested %d", stock, qty)
	}

	_, err = tx.Exec(`UPDATE inventory SET stock = stock - $1, updated_at = CURRENT_TIMESTAMP WHERE item_id = $2`, qty, itemID)
	if err != nil {
		return err
	}

	return tx.Commit()
}

func (db *DB) RestoreStock(itemID string, qty int) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	var stock int
	err = tx.QueryRow(`SELECT stock FROM inventory WHERE item_id = $1 FOR UPDATE`, itemID).Scan(&stock)
	if err != nil {
		return fmt.Errorf("item not found: %w", err)
	}

	_, err = tx.Exec(`UPDATE inventory SET stock = stock + $1, updated_at = CURRENT_TIMESTAMP WHERE item_id = $2`, qty, itemID)
	if err != nil {
		return err
	}

	return tx.Commit()
}

func (db *DB) CreatePayment(id, orderID string, amount float64, status string) error {
	query := `INSERT INTO payments (id, order_id, amount, status) VALUES ($1, $2, $3, $4)`
	_, err := db.Exec(query, id, orderID, amount, status)
	return err
}
