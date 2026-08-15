package database

import (
	"context"
	"fmt"
	"log"
	"time"

	"echo-otel-demo/internal/config"

	"github.com/exaring/otelpgx"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Database struct {
	pool *pgxpool.Pool
}

// NewPostgresql creates a new connection pool pointing to PgBouncer.
// PgBouncer then manages connections to the actual PostgreSQL instance.
func NewPostgresql(cfg *config.Config) *Database {
	dsn := fmt.Sprintf(
		"user=%s password=%s host=%s port=%s dbname=%s sslmode=disable application_name=%s",
		cfg.DBUser, cfg.DBPassword, cfg.DBHost, cfg.DBPort, cfg.DBName, cfg.AppName,
	)

	poolCfg, err := pgxpool.ParseConfig(dsn)
	if err != nil {
		log.Fatalf("database: error parsing config: %v", err)
	}

	// Pool settings
	poolCfg.MaxConns = int32(cfg.DBMaxOpenConns)
	poolCfg.MinConns = int32(cfg.DBMaxIdleConns)
	poolCfg.MaxConnIdleTime = time.Duration(cfg.DBConnMaxIdleTime) * time.Minute
	poolCfg.MaxConnLifetime = time.Duration(cfg.DBConnMaxLifetime) * time.Minute

	// OpenTelemetry tracing for all SQL queries
	poolCfg.ConnConfig.Tracer = otelpgx.NewTracer()

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	pool, err := pgxpool.NewWithConfig(ctx, poolCfg)
	if err != nil {
		log.Fatalf("database: error creating pool: %v", err)
	}

	if err := pool.Ping(ctx); err != nil {
		log.Fatalf("database: error pinging: %v", err)
	}

	log.Printf("✅ Database connected via %s:%s", cfg.DBHost, cfg.DBPort)
	return &Database{pool: pool}
}

func (d *Database) GetPool() *pgxpool.Pool {
	return d.pool
}

func (d *Database) Close() {
	d.pool.Close()
	log.Println("✅ Database connection closed")
}
