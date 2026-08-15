# Distributed Transaction - Saga Pattern dengan Golang

Proyek ini adalah implementasi pembelajaran **Distributed Transaction** menggunakan **Saga Choreography Pattern** dengan 5 microservices.

## 🏗️ Tech Stack

- **Language**: Go 1.22
- **Framework**: Echo v4
- **Database**: PostgreSQL 16
- **Message Broker**: Apache Kafka (KRaft mode, tanpa Zookeeper)
- **Container**: Docker & Docker Compose

## 📦 Arsitektur

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Order     │     │   Payment    │     │  Inventory   │
│   Service    │     │   Service    │     │   Service    │
│   :8081      │     │   :8082      │     │   :8083      │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────┬───────┴────────────────────┘
                    │
              ┌─────┴─────┐
              │   Kafka   │
              │  Broker   │
              └─────┬─────┘
                    │
       ┌────────────┴────────────┐
       │                         │
┌──────┴───────┐     ┌──────────┴───┐
│  Shipping    │     │ Notification │
│  Service     │     │   Service    │
│  :8084       │     │   :8085      │
└──────────────┘     └──────────────┘
```

## 🔄 Saga Flow

### Happy Path
```
Order Created → Inventory Reserved → Payment Completed → Shipping Created → Order Completed → Notification Sent
```

### Compensation (Payment Failed)
```
Payment Failed → Inventory Released → Order Failed → Notification Sent
```

### Compensation (Shipping Failed)
```
Shipping Failed → Payment Refunded → Inventory Released → Order Failed → Notification Sent
```

## 🚀 Quick Start

### Prasyarat
- Docker & Docker Compose

### Jalankan Semua Service
```bash
docker-compose up --build
```

### Tunggu sampai semua service ready, lalu test:

#### 1. Cek Products (Inventory Service)
```bash
curl http://localhost:8083/products | jq
```

#### 2. Buat Order (Happy Path)
```bash
curl -X POST http://localhost:8081/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "product_id": "prod-001",
    "quantity": 2,
    "total_price": 30000000
  }' | jq
```

#### 3. Cek Status Order
```bash
# Ganti ORDER_ID dengan ID dari response sebelumnya
curl http://localhost:8081/orders/ORDER_ID | jq
```

#### 4. Cek Semua Orders
```bash
curl http://localhost:8081/orders | jq
```

#### 5. Cek Payments
```bash
curl http://localhost:8082/payments | jq
```

#### 6. Cek Shipments
```bash
curl http://localhost:8084/shipments | jq
```

#### 7. Cek Notifications
```bash
curl http://localhost:8085/notifications | jq
```

### Health Check
```bash
curl http://localhost:8081/health  # Order Service
curl http://localhost:8082/health  # Payment Service
curl http://localhost:8083/health  # Inventory Service
curl http://localhost:8084/health  # Shipping Service
curl http://localhost:8085/health  # Notification Service
```

## 🧪 Test Scenarios

### Scenario 1: Happy Path
Buat order dengan quantity yang cukup. Order akan melewati semua step dan berakhir `COMPLETED`.

### Scenario 2: Inventory Failed
Buat order dengan quantity yang sangat besar (melebihi stock). Order akan langsung `FAILED` dengan reason inventory.

```bash
curl -X POST http://localhost:8081/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Doe",
    "product_id": "prod-004",
    "quantity": 999,
    "total_price": 999000000
  }' | jq
```

### Scenario 3: Payment Failed (Random)
Payment service memiliki **20% chance gagal** (simulasi). Coba buat beberapa order, beberapa akan gagal di step payment, dan stok akan otomatis di-release.

### Scenario 4: Shipping Failed (Random)
Shipping service memiliki **10% chance gagal** (simulasi). Jika gagal, payment akan di-refund dan stok di-release.

## 📁 Struktur Folder

```
distributed_transaction/
├── docker-compose.yml
├── go.mod
├── go.sum
├── .env
├── scripts/
│   └── init-db.sh
├── pkg/                          # Shared packages
│   ├── config/config.go
│   ├── events/events.go
│   └── kafka/
│       ├── producer.go
│       └── consumer.go
└── services/
    ├── order-service/            # Port 8081
    ├── payment-service/          # Port 8082
    ├── inventory-service/        # Port 8083
    ├── shipping-service/         # Port 8084
    └── notification-service/     # Port 8085
```

## 📝 Kafka Topics

| Topic | Producer | Consumer |
|-------|----------|----------|
| `order.created` | Order | Inventory |
| `order.completed` | Order | Notification |
| `order.failed` | Order | Notification |
| `inventory.reserved` | Inventory | Payment |
| `inventory.failed` | Inventory | Order |
| `inventory.released` | Inventory | (log) |
| `payment.completed` | Payment | Shipping, Order |
| `payment.failed` | Payment | Inventory, Order |
| `shipping.created` | Shipping | Order |
| `shipping.failed` | Shipping | Payment, Inventory, Order |

## 🎓 Konsep yang Dipelajari

1. **Saga Pattern (Choreography)** - Setiap service publish event, service lain react
2. **Compensation Transaction** - Rollback distributed dengan compensating actions
3. **Event-Driven Architecture** - Komunikasi antar service via events
4. **Database per Service** - Setiap service punya database sendiri
5. **Eventual Consistency** - Data konsisten secara eventual, bukan immediate
