package config

import (
	"fmt"
	"os"
	"strconv"
)

// Config menyimpan semua konfigurasi aplikasi.
// Semua nilai dibaca dari environment variables.
type Config struct {
	// Server
	ServerPort string

	// Database - koneksi melalui PgBouncer (untuk aplikasi)
	DBHost     string
	DBPort     int
	DBUser     string
	DBPassword string
	DBName     string
	DBSSLMode  string

	// Database - koneksi langsung ke PostgreSQL (untuk migration)
	// Migration HARUS langsung ke PostgreSQL, BUKAN melalui PgBouncer
	// karena golang-migrate menggunakan advisory lock yang tidak didukung
	// oleh PgBouncer dalam mode transaction pooling.
	MigrateDBHost string
	MigrateDBPort int
}

// NewConfig membuat Config baru dari environment variables.
func NewConfig() *Config {
	return &Config{
		ServerPort: getEnv("SERVER_PORT", "8080"),

		// Koneksi via PgBouncer (default port 6432)
		DBHost:     getEnv("DB_HOST", "pgbouncer"),
		DBPort:     getEnvAsInt("DB_PORT", 6432),
		DBUser:     getEnv("DB_USER", "postgres"),
		DBPassword: getEnv("DB_PASSWORD", "postgres"),
		DBName:     getEnv("DB_NAME", "migration_db"),
		DBSSLMode:  getEnv("DB_SSLMODE", "disable"),

		// Koneksi langsung ke PostgreSQL (default port 5432)
		MigrateDBHost: getEnv("MIGRATE_DB_HOST", "postgres"),
		MigrateDBPort: getEnvAsInt("MIGRATE_DB_PORT", 5432),
	}
}

// AppDSN mengembalikan connection string untuk aplikasi (via PgBouncer).
func (c *Config) AppDSN() string {
	return fmt.Sprintf(
		"postgres://%s:%s@%s:%d/%s?sslmode=%s",
		c.DBUser, c.DBPassword, c.DBHost, c.DBPort, c.DBName, c.DBSSLMode,
	)
}

// MigrateDSN mengembalikan connection string untuk migration (langsung ke PostgreSQL).
// PENTING: Migration harus bypass PgBouncer karena:
// 1. golang-migrate menggunakan advisory lock (pg_advisory_lock)
// 2. PgBouncer mode transaction tidak mendukung advisory lock
// 3. Advisory lock bisa "hilang" saat koneksi dikembalikan ke pool
func (c *Config) MigrateDSN() string {
	return fmt.Sprintf(
		"postgres://%s:%s@%s:%d/%s?sslmode=%s",
		c.DBUser, c.DBPassword, c.MigrateDBHost, c.MigrateDBPort, c.DBName, c.DBSSLMode,
	)
}

// getEnv membaca environment variable atau mengembalikan default value.
func getEnv(key, defaultVal string) string {
	if val, exists := os.LookupEnv(key); exists {
		return val
	}
	return defaultVal
}

// getEnvAsInt membaca environment variable sebagai integer.
func getEnvAsInt(key string, defaultVal int) int {
	valStr := getEnv(key, "")
	if val, err := strconv.Atoi(valStr); err == nil {
		return val
	}
	return defaultVal
}
