package config

import (
	"fmt"
	"os"
)

type DBConfig struct {
	Host     string
	Port     string
	User     string
	Password string
	DBName   string
}

func (c DBConfig) DSN() string {
	return fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		c.User, c.Password, c.Host, c.Port, c.DBName)
}

type Config struct {
	Port     string
	ActiveDB string // "dc" or "drc"
	DCDB     DBConfig
	DRCDB    DBConfig
}

func LoadConfig() *Config {
	return &Config{
		Port:     getEnv("APP_PORT", "8080"),
		ActiveDB: getEnv("ACTIVE_DB", "dc"),
		DCDB: DBConfig{
			Host:     getEnv("DC_DB_HOST", "pgbouncer-dc"),
			Port:     getEnv("DC_DB_PORT", "6432"),
			User:     getEnv("DC_DB_USER", "appuser"),
			Password: getEnv("DC_DB_PASSWORD", "apppassword"),
			DBName:   getEnv("DC_DB_NAME", "appdb"),
		},
		DRCDB: DBConfig{
			Host:     getEnv("DRC_DB_HOST", "pgbouncer-drc"),
			Port:     getEnv("DRC_DB_PORT", "6432"),
			User:     getEnv("DRC_DB_USER", "appuser"),
			Password: getEnv("DRC_DB_PASSWORD", "apppassword"),
			DBName:   getEnv("DRC_DB_NAME", "appdb"),
		},
	}
}

func getEnv(key, defaultValue string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return defaultValue
}
