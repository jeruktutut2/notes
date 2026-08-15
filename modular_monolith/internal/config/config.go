package config

import (
	"fmt"
	"os"
)

// Config holds all application configuration.
type Config struct {
	ServerPort   string
	DatabaseURL  string
	OtelEndpoint string
	ServiceName  string
}

// Load reads configuration from environment variables with defaults.
func Load() *Config {
	return &Config{
		ServerPort:   getEnv("SERVER_PORT", "8080"),
		DatabaseURL:  getEnv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/modular_monolith?sslmode=disable"),
		OtelEndpoint: getEnv("OTEL_ENDPOINT", "localhost:4317"),
		ServiceName:  getEnv("SERVICE_NAME", "modular-monolith"),
	}
}

// String returns a human-readable representation (hides sensitive values).
func (c *Config) String() string {
	return fmt.Sprintf(
		"Config{Port=%s, DB=***masked***, OTel=%s, Service=%s}",
		c.ServerPort, c.OtelEndpoint, c.ServiceName,
	)
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
