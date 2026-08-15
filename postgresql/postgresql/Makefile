BINARY_NAME=server

.PHONY: build run dev docker-up docker-down tidy

# Build the binary
build:
	go build -o bin/$(BINARY_NAME) ./cmd/api

# Run locally (requires .env vars and docker services up)
run: build
	./bin/$(BINARY_NAME)

# Run with go run
dev:
	go run ./cmd/api

# Start all Docker services
docker-up:
	docker compose up -d

# Stop all Docker services
docker-down:
	docker compose down -v

# Tidy modules
tidy:
	go mod tidy
