# ==========================================
# MAKEFILE - Shortcut Commands
# ==========================================
# Gunakan: make <target>
# Contoh:  make up
# ==========================================

.PHONY: help setup up down down-all fresh version status create cleanup demo build run docker-up docker-down

# Default
help: ## Tampilkan help
	@echo ""
	@echo "📦 Migration Demo - Makefile Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ==========================================
# DOCKER
# ==========================================

setup: ## Start PostgreSQL + PgBouncer
	./scripts/migration.sh setup

cleanup: ## Stop semua Docker services
	./scripts/migration.sh cleanup

docker-build: ## Build Docker image app
	docker compose build app

docker-up: ## Start semua services (termasuk app)
	docker compose up -d

docker-down: ## Stop semua services
	docker compose down

docker-logs: ## Lihat logs semua services
	docker compose logs -f

docker-ps: ## Lihat status services
	docker compose ps

# ==========================================
# MIGRATION (CLI lokal)
# ==========================================

up: ## Apply semua migration
	./scripts/migration.sh up

down: ## Rollback 1 migration
	./scripts/migration.sh down 1

down-all: ## Rollback SEMUA migration
	./scripts/migration.sh down-all

fresh: ## Drop semua & apply ulang
	./scripts/migration.sh fresh

version: ## Lihat versi migration saat ini
	./scripts/migration.sh version

status: ## Lihat status database & migration
	./scripts/migration.sh status

create: ## Buat migration baru (usage: make create name=nama_migration)
	./scripts/migration.sh create $(name)

force: ## Force versi migration (usage: make force v=3)
	./scripts/migration.sh force $(v)

goto: ## Goto versi migration (usage: make goto v=3)
	./scripts/migration.sh goto $(v)

demo: ## Jalankan demo interaktif (basic)
	./scripts/migration.sh demo

demo-real: ## Jalankan demo real-world (lengkap + data)
	./scripts/demo_realworld.sh

# ==========================================
# MIGRATION (via Docker)
# ==========================================

migrate-docker-up: ## Apply migration via Docker
	./scripts/migration.sh docker-up

migrate-docker-down: ## Rollback migration via Docker
	./scripts/migration.sh docker-down 1

# ==========================================
# DEVELOPMENT
# ==========================================

build: ## Build Go binary
	go build -o bin/server ./cmd/api

run: ## Jalankan server lokal
	go run ./cmd/api

tidy: ## go mod tidy
	go mod tidy

test: ## Jalankan tests
	go test ./... -v

lint: ## Jalankan linter
	golangci-lint run ./...

# ==========================================
# DATABASE (direct access)
# ==========================================

psql: ## Akses PostgreSQL shell
	docker compose exec postgres psql -U postgres -d migration_db

psql-tables: ## Lihat daftar tabel
	docker compose exec postgres psql -U postgres -d migration_db -c "\dt"

psql-desc: ## Describe tabel users
	docker compose exec postgres psql -U postgres -d migration_db -c "\d+ users"

pgbouncer-stats: ## Lihat stats PgBouncer
	docker compose exec pgbouncer psql -p 6432 -U postgres pgbouncer -c "SHOW POOLS;"
