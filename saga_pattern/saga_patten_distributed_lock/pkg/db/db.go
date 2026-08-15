package db

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/lib/pq"
)

type Order struct {
	ID         string    `json:"id"`
	ProductID  string    `json:"product_id"`
	Quantity   int       `json:"quantity"`
	TotalPrice float64   `json:"total_price"`
	Status     string    `json:"status"`
	CreatedAt  time.Time `json:"created_at"`
}

type DB struct {
	SQL *sql.DB
}

func InitDB(dsn string) (*DB, error) {
	sqlDB, err := sql.Open("postgres", dsn)
	if err != nil {
		return nil, fmt.Errorf("sql open error: %w", err)
	}

	sqlDB.SetMaxOpenConns(25)
	sqlDB.SetMaxIdleConns(5)
	sqlDB.SetConnMaxLifetime(5 * time.Minute)

	if err := sqlDB.Ping(); err != nil {
		return nil, fmt.Errorf("sql ping error: %w", err)
	}

	database := &DB{SQL: sqlDB}
	if err := database.migrate(); err != nil {
		return nil, fmt.Errorf("migration error: %w", err)
	}

	log.Println("[DB] PostgreSQL initialized successfully via PgBouncer connection pool")
	return database, nil
}

func (d *DB) migrate() error {
	queries := []string{
		`CREATE TABLE IF NOT EXISTS orders (
			id VARCHAR(64) PRIMARY KEY,
			product_id VARCHAR(64) NOT NULL,
			quantity INT NOT NULL,
			total_price NUMERIC(10,2) NOT NULL,
			status VARCHAR(64) NOT NULL,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		);`,
		`CREATE TABLE IF NOT EXISTS inventory (
			product_id VARCHAR(64) PRIMARY KEY,
			stock INT NOT NULL
		);`,
		`INSERT INTO inventory (product_id, stock) 
		 VALUES ('PROD-101', 50) 
		 ON CONFLICT (product_id) DO UPDATE SET stock = 50;`,
	}

	for _, q := range queries {
		if _, err := d.SQL.Exec(q); err != nil {
			return err
		}
	}
	return nil
}

func (d *DB) CreateOrder(order Order) error {
	query := `INSERT INTO orders (id, product_id, quantity, total_price, status, created_at) VALUES ($1, $2, $3, $4, $5, $6)`
	_, err := d.SQL.Exec(query, order.ID, order.ProductID, order.Quantity, order.TotalPrice, order.Status, order.CreatedAt)
	return err
}

func (d *DB) UpdateOrderStatus(id string, status string) error {
	query := `UPDATE orders SET status = $1 WHERE id = $2`
	_, err := d.SQL.Exec(query, status, id)
	return err
}

func (d *DB) GetOrder(id string) (*Order, error) {
	query := `SELECT id, product_id, quantity, total_price, status, created_at FROM orders WHERE id = $1`
	row := d.SQL.QueryRow(query, id)
	var o Order
	if err := row.Scan(&o.ID, &o.ProductID, &o.Quantity, &o.TotalPrice, &o.Status, &o.CreatedAt); err != nil {
		return nil, err
	}
	return &o, nil
}
