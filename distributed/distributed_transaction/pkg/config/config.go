package config

import (
	"fmt"
	"os"
)

// Config holds all configuration for a service
type Config struct {
	DBHost      string
	DBPort      string
	DBUser      string
	DBPassword  string
	DBName      string
	KafkaBrokers string
	ServicePort string
}

// Load reads configuration from environment variables
func Load() *Config {
	return &Config{
		DBHost:       getEnv("DB_HOST", "localhost"),
		DBPort:       getEnv("DB_PORT", "5432"),
		DBUser:       getEnv("DB_USER", "postgres"),
		DBPassword:   getEnv("DB_PASSWORD", "postgres123"),
		DBName:       getEnv("DB_NAME", "order_db"),
		KafkaBrokers: getEnv("KAFKA_BROKERS", "localhost:9094"),
		ServicePort:  getEnv("SERVICE_PORT", "8081"),
	}
}

// DSN returns the PostgreSQL connection string
func (c *Config) DSN() string {
	return fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		c.DBHost, c.DBPort, c.DBUser, c.DBPassword, c.DBName,
	)
}

func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}
