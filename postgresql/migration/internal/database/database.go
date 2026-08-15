package database

import (
	"context"
	"embed"
	"fmt"
	"log/slog"
	"time"

	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	"github.com/golang-migrate/migrate/v4/source/iofs"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/bsa/migration/internal/config"
)

// Database mengelola koneksi pool ke PostgreSQL.
type Database struct {
	Pool   *pgxpool.Pool
	config *config.Config
}

// New membuat koneksi database baru via PgBouncer.
func New(cfg *config.Config) (*Database, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Parse konfigurasi pool
	poolConfig, err := pgxpool.ParseConfig(cfg.AppDSN())
	if err != nil {
		return nil, fmt.Errorf("gagal parse DSN: %w", err)
	}

	// Konfigurasi pool
	poolConfig.MaxConns = 25
	poolConfig.MinConns = 5
	poolConfig.MaxConnLifetime = 30 * time.Minute
	poolConfig.MaxConnIdleTime = 5 * time.Minute

	// Buat connection pool
	pool, err := pgxpool.NewWithConfig(ctx, poolConfig)
	if err != nil {
		return nil, fmt.Errorf("gagal membuat connection pool: %w", err)
	}

	// Test koneksi
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("gagal ping database: %w", err)
	}

	slog.Info("Database terkoneksi",
		"host", cfg.DBHost,
		"port", cfg.DBPort,
		"database", cfg.DBName,
	)

	return &Database{
		Pool:   pool,
		config: cfg,
	}, nil
}

// Close menutup connection pool.
func (db *Database) Close() {
	if db.Pool != nil {
		db.Pool.Close()
		slog.Info("Database connection pool ditutup")
	}
}

// RunMigrations menjalankan semua migration ke versi terbaru.
// Migration dijalankan LANGSUNG ke PostgreSQL (bypass PgBouncer).
func (db *Database) RunMigrations(migrationFS embed.FS) error {
	return db.runMigrate(migrationFS, func(m *migrate.Migrate) error {
		if err := m.Up(); err != nil && err != migrate.ErrNoChange {
			return fmt.Errorf("gagal menjalankan migration up: %w", err)
		}
		return nil
	})
}

// RollbackMigrations melakukan rollback N migration.
func (db *Database) RollbackMigrations(migrationFS embed.FS, steps int) error {
	return db.runMigrate(migrationFS, func(m *migrate.Migrate) error {
		if err := m.Steps(-steps); err != nil && err != migrate.ErrNoChange {
			return fmt.Errorf("gagal rollback migration: %w", err)
		}
		return nil
	})
}

// GetMigrationVersion mengembalikan versi migration saat ini.
func (db *Database) GetMigrationVersion(migrationFS embed.FS) (uint, bool, error) {
	var version uint
	var dirty bool

	err := db.runMigrate(migrationFS, func(m *migrate.Migrate) error {
		v, d, err := m.Version()
		if err != nil {
			return err
		}
		version = v
		dirty = d
		return nil
	})

	return version, dirty, err
}

// runMigrate adalah helper internal untuk membuat instance migrate dan menjalankan operasi.
func (db *Database) runMigrate(migrationFS embed.FS, operation func(*migrate.Migrate) error) error {
	// Buat source driver dari embedded filesystem
	sourceDriver, err := iofs.New(migrationFS, "sql")
	if err != nil {
		return fmt.Errorf("gagal membuat source driver: %w", err)
	}

	// Buat migrate instance
	// PENTING: Gunakan MigrateDSN (langsung ke PostgreSQL)
	m, err := migrate.NewWithSourceInstance("iofs", sourceDriver, db.config.MigrateDSN())
	if err != nil {
		return fmt.Errorf("gagal membuat migrate instance: %w", err)
	}
	defer m.Close()

	// Jalankan operasi
	if err := operation(m); err != nil {
		return err
	}

	// Log versi saat ini
	version, dirty, verr := m.Version()
	if verr != nil && verr != migrate.ErrNoChange {
		slog.Warn("Gagal membaca versi migration", "error", verr)
	} else {
		slog.Info("Migration selesai",
			"version", version,
			"dirty", dirty,
		)
	}

	return nil
}
