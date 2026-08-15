package repository

import (
	"database/sql"
	"fmt"
	"time"

	"distributed-transaction/services/inventory-service/internal/model"
)

type InventoryRepository struct {
	db *sql.DB
}

func NewInventoryRepository(db *sql.DB) *InventoryRepository {
	return &InventoryRepository{db: db}
}

// GetProductByID retrieves a product by ID
func (r *InventoryRepository) GetProductByID(id string) (*model.Product, error) {
	query := `
		SELECT id, name, stock, reserved_stock, price, created_at, updated_at
		FROM products WHERE id = $1
	`
	p := &model.Product{}
	err := r.db.QueryRow(query, id).Scan(
		&p.ID, &p.Name, &p.Stock, &p.ReservedStock, &p.Price, &p.CreatedAt, &p.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("product not found: %w", err)
	}
	return p, nil
}

// GetAllProducts retrieves all products
func (r *InventoryRepository) GetAllProducts() ([]model.Product, error) {
	query := `
		SELECT id, name, stock, reserved_stock, price, created_at, updated_at
		FROM products ORDER BY name
	`
	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var products []model.Product
	for rows.Next() {
		var p model.Product
		err := rows.Scan(&p.ID, &p.Name, &p.Stock, &p.ReservedStock, &p.Price, &p.CreatedAt, &p.UpdatedAt)
		if err != nil {
			return nil, err
		}
		products = append(products, p)
	}
	return products, nil
}

// ReserveStock reserves stock for an order (increment reserved_stock)
// Menggunakan SELECT FOR UPDATE untuk prevent race condition
func (r *InventoryRepository) ReserveStock(productID string, quantity int) error {
	tx, err := r.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Lock the row
	var stock, reservedStock int
	err = tx.QueryRow(
		"SELECT stock, reserved_stock FROM products WHERE id = $1 FOR UPDATE",
		productID,
	).Scan(&stock, &reservedStock)
	if err != nil {
		return fmt.Errorf("product not found: %w", err)
	}

	available := stock - reservedStock
	if available < quantity {
		return fmt.Errorf("insufficient stock: available=%d requested=%d", available, quantity)
	}

	// Update reserved_stock
	_, err = tx.Exec(
		"UPDATE products SET reserved_stock = reserved_stock + $1, updated_at = $2 WHERE id = $3",
		quantity, time.Now(), productID,
	)
	if err != nil {
		return err
	}

	return tx.Commit()
}

// ReleaseStock releases reserved stock (decrement reserved_stock) - compensation
func (r *InventoryRepository) ReleaseStock(productID string, quantity int) error {
	_, err := r.db.Exec(
		"UPDATE products SET reserved_stock = GREATEST(reserved_stock - $1, 0), updated_at = $2 WHERE id = $3",
		quantity, time.Now(), productID,
	)
	return err
}

// CreateProduct creates a new product
func (r *InventoryRepository) CreateProduct(p *model.Product) error {
	query := `
		INSERT INTO products (id, name, stock, reserved_stock, price, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7)
	`
	_, err := r.db.Exec(query, p.ID, p.Name, p.Stock, p.ReservedStock, p.Price, p.CreatedAt, p.UpdatedAt)
	return err
}

// CreateLog creates an inventory log entry
func (r *InventoryRepository) CreateLog(logEntry *model.InventoryLog) error {
	query := `
		INSERT INTO inventory_logs (id, order_id, product_id, quantity, action, created_at)
		VALUES ($1, $2, $3, $4, $5, $6)
	`
	_, err := r.db.Exec(query, logEntry.ID, logEntry.OrderID, logEntry.ProductID, logEntry.Quantity, logEntry.Action, logEntry.CreatedAt)
	return err
}

// GetReservationByOrderID finds the RESERVE log for an order to know what to release
func (r *InventoryRepository) GetReservationByOrderID(orderID string) (*model.InventoryLog, error) {
	query := `
		SELECT id, order_id, product_id, quantity, action, created_at
		FROM inventory_logs
		WHERE order_id = $1 AND action = 'RESERVE'
		ORDER BY created_at DESC LIMIT 1
	`
	logEntry := &model.InventoryLog{}
	err := r.db.QueryRow(query, orderID).Scan(
		&logEntry.ID, &logEntry.OrderID, &logEntry.ProductID,
		&logEntry.Quantity, &logEntry.Action, &logEntry.CreatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("reservation not found for order %s: %w", orderID, err)
	}
	return logEntry, nil
}
