package config

import (
	"os"
	"strconv"
)

type Config struct {
	AppPort  string
	AppName  string

	// Database (connects to PgBouncer)
	DBHost     string
	DBPort     string
	DBUser     string
	DBPassword string
	DBName     string

	// Pool
	DBMaxOpenConns     int
	DBMaxIdleConns     int
	DBConnMaxIdleTime  int // minutes
	DBConnMaxLifetime  int // minutes

	// OpenTelemetry
	OtelEndpoint    string
	OtelServiceName string
}

func Load() *Config {
	return &Config{
		AppPort:  getEnv("APP_PORT", "8080"),
		AppName:  getEnv("APP_NAME", "echo-otel-demo"),

		DBHost:     getEnv("DB_HOST", "localhost"),
		DBPort:     getEnv("DB_PORT", "6432"), // PgBouncer port
		DBUser:     getEnv("DB_USER", "appuser"),
		DBPassword: getEnv("DB_PASSWORD", "apppassword"),
		DBName:     getEnv("DB_NAME", "appdb"),

		DBMaxOpenConns:    getEnvInt("DB_MAX_OPEN_CONNS", 10),
		DBMaxIdleConns:    getEnvInt("DB_MAX_IDLE_CONNS", 5),
		DBConnMaxIdleTime: getEnvInt("DB_CONN_MAX_IDLE_TIME", 5),
		DBConnMaxLifetime: getEnvInt("DB_CONN_MAX_LIFETIME", 30),

		OtelEndpoint:    getEnv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317"),
		OtelServiceName: getEnv("OTEL_SERVICE_NAME", "echo-otel-demo"),
	}
}

func getEnv(key, fallback string) string {
	if val, ok := os.LookupEnv(key); ok {
		return val
	}
	return fallback
}

func getEnvInt(key string, fallback int) int {
	if val, ok := os.LookupEnv(key); ok {
		if i, err := strconv.Atoi(val); err == nil {
			return i
		}
	}
	return fallback
}
