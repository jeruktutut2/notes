.PHONY: run build docker-up docker-down migrate clean

# Run the server
run:
	go run cmd/server/main.go

# Build binary
build:
	go build -o bin/server cmd/server/main.go

# Start infrastructure (PostgreSQL + Jaeger)
docker-up:
	docker compose up -d

# Stop infrastructure
docker-down:
	docker compose down

# Run migrations manually (requires psql)
migrate:
	PGPASSWORD=postgres psql -h localhost -U postgres -d modular_monolith -f migrations/001_init.sql

# Clean build artifacts
clean:
	rm -rf bin/

# Run all checks
check:
	go vet ./...
	go build ./...

# Show logs
logs:
	docker compose logs -f
