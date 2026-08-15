# Modular Monolith — Go Backend

Contoh implementasi **Modular Monolith** backend menggunakan Go dengan arsitektur clean per module.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | [Echo v5](https://github.com/labstack/echo) |
| Database | PostgreSQL 16 + [pgxpool](https://github.com/jackc/pgx) |
| Tracing | [OpenTelemetry](https://opentelemetry.io/) → [Jaeger](https://www.jaegertracing.io/) (OTLP gRPC) |
| DB Tracing | [otelpgx](https://github.com/exaring/otelpgx) |
| Logging | `log/slog` (stdlib) |

## Modules

| Module | Path | Deskripsi |
|---|---|---|
| **User** | `/api/v1/users` | Manajemen user & login |
| **Product** | `/api/v1/products` | Katalog produk |
| **Order** | `/api/v1/orders` | Pemesanan |
| **Inventory** | `/api/v1/inventory` | Manajemen stok |
| **Notification** | `/api/v1/notifications` | Notifikasi in-app |

## Quick Start

### 1. Start Infrastructure

```bash
docker compose up -d
```

Ini akan menjalankan:
- **PostgreSQL** di `localhost:5432` (auto-run migrations)
- **Jaeger UI** di `http://localhost:16686`

### 2. Run Server

```bash
go run cmd/server/main.go
```

Server berjalan di `http://localhost:8080`

### 3. Test Health Check

```bash
curl http://localhost:8080/health
```

## API Endpoints

### User Module

```bash
# Create user
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"secret123"}'

# List users
curl http://localhost:8080/api/v1/users?page=1&limit=10

# Get user by ID
curl http://localhost:8080/api/v1/users/{id}

# Update user
curl -X PUT http://localhost:8080/api/v1/users/{id} \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com"}'

# Delete user
curl -X DELETE http://localhost:8080/api/v1/users/{id}

# Login
curl -X POST http://localhost:8080/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"secret123"}'
```

### Product Module

```bash
# Create product
curl -X POST http://localhost:8080/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"Gaming laptop","price":15000000,"category":"electronics"}'

# List products (with optional category filter)
curl http://localhost:8080/api/v1/products?page=1&limit=10&category=electronics

# Get product by ID
curl http://localhost:8080/api/v1/products/{id}

# Update product
curl -X PUT http://localhost:8080/api/v1/products/{id} \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop Pro","price":20000000}'

# Delete product
curl -X DELETE http://localhost:8080/api/v1/products/{id}
```

### Order Module

```bash
# Create order
curl -X POST http://localhost:8080/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id":"{user_id}","items":[{"product_id":"{product_id}","quantity":2,"price":15000000}]}'

# List orders (with optional user_id filter)
curl http://localhost:8080/api/v1/orders?page=1&limit=10&user_id={user_id}

# Get order by ID (includes items)
curl http://localhost:8080/api/v1/orders/{id}

# Update order status
curl -X PUT http://localhost:8080/api/v1/orders/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status":"confirmed"}'
# Valid statuses: pending, confirmed, processing, shipped, delivered, cancelled
```

### Inventory Module

```bash
# Initialize inventory for a product
curl -X POST http://localhost:8080/api/v1/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_id":"{product_id}","quantity":100}'

# Get inventory by product ID
curl http://localhost:8080/api/v1/inventory/{product_id}

# List all inventory
curl http://localhost:8080/api/v1/inventory?page=1&limit=10

# Adjust inventory (positive = add, negative = subtract)
curl -X PUT http://localhost:8080/api/v1/inventory/{product_id}/adjust \
  -H "Content-Type: application/json" \
  -d '{"adjustment":-5,"reason":"sold 5 units"}'
```

### Notification Module

```bash
# Create notification
curl -X POST http://localhost:8080/api/v1/notifications \
  -H "Content-Type: application/json" \
  -d '{"user_id":"{user_id}","title":"Order Confirmed","message":"Your order has been confirmed"}'

# List notifications for a user
curl http://localhost:8080/api/v1/notifications?user_id={user_id}&page=1&limit=10

# Get notification by ID
curl http://localhost:8080/api/v1/notifications/{id}

# Mark as read
curl -X PUT http://localhost:8080/api/v1/notifications/{id}/read
```

## Project Structure

```
modular_monolith/
├── cmd/server/main.go              # Entry point & module wiring
├── internal/
│   ├── config/                     # Configuration
│   ├── platform/
│   │   ├── database/               # pgxpool + OTel tracing
│   │   ├── telemetry/              # OTel TracerProvider
│   │   └── server/                 # Echo v5 setup
│   ├── shared/
│   │   ├── response/               # JSON response helpers
│   │   └── middleware/             # OTel HTTP tracing middleware
│   └── modules/
│       ├── user/                   # User module
│       ├── product/                # Product module
│       ├── order/                  # Order module
│       ├── inventory/              # Inventory module
│       └── notification/           # Notification module
├── migrations/                     # SQL migrations
├── docker-compose.yml              # PostgreSQL + Jaeger
├── Makefile
└── README.md
```

Setiap module mengikuti pola:
```
module/
├── model.go         # Domain model + DTOs
├── repository.go    # Data access (pgxpool)
├── service.go       # Business logic + OTel spans
├── handler.go       # HTTP handlers (Echo v5)
└── module.go        # Route registration & dependency wiring
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SERVER_PORT` | `8080` | HTTP server port |
| `DATABASE_URL` | `postgres://postgres:postgres@localhost:5432/modular_monolith?sslmode=disable` | PostgreSQL connection string |
| `OTEL_ENDPOINT` | `localhost:4317` | Jaeger OTLP gRPC endpoint |
| `SERVICE_NAME` | `modular-monolith` | OpenTelemetry service name |

## Observability

Buka Jaeger UI di `http://localhost:16686` untuk melihat:
- **Trace per HTTP request** — span dari middleware
- **Database queries** — span dari otelpgx
- **Business logic** — span dari service layer

## Makefile Commands

```bash
make run          # Run the server
make build        # Build binary
make docker-up    # Start PostgreSQL + Jaeger
make docker-down  # Stop containers
make migrate      # Run migrations manually
make check        # Run go vet + go build
make logs         # Show container logs
```
