package db

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

type Client struct {
	DB *sql.DB
}

func InitDB() (*Client, error) {
	dbHost := os.Getenv("DB_HOST")
	if dbHost == "" {
		dbHost = "haproxy" // Connects to HAProxy which load-balances to ProxySQL
	}
	dbPort := os.Getenv("DB_PORT")
	if dbPort == "" {
		dbPort = "3306" // HAProxy MySQL port
	}
	dbUser := os.Getenv("DB_USER")
	if dbUser == "" {
		dbUser = "root"
	}
	dbPass := os.Getenv("DB_PASS")
	if dbPass == "" {
		dbPass = "rootpassword"
	}
	dbName := os.Getenv("DB_NAME")
	if dbName == "" {
		dbName = "company_db"
	}

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?parseTime=true", dbUser, dbPass, dbHost, dbPort, dbName)

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	db.SetMaxOpenConns(50)
	db.SetMaxIdleConns(10)
	db.SetConnMaxLifetime(5 * time.Minute)

	if err := db.Ping(); err != nil {
		log.Printf("Warning: initial db ping via HAProxy failed: %v", err)
	}

	return &Client{DB: db}, nil
}
