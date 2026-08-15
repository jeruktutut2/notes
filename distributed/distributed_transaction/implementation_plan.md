# Distributed Transaction - Belajar Saga Pattern dengan Golang, Echo, PostgreSQL & Kafka

## Deskripsi

Membangun sistem e-commerce sederhana dengan 5 microservices yang mendemonstrasikan **Saga Choreography Pattern** untuk distributed transaction. Setiap service memiliki database sendiri (Database per Service pattern) dan berkomunikasi via Apache Kafka events.

## Arsitektur

![Diagram](https://mermaid.ink/img/Z3JhcGggVEIKICAgIENsaWVudFsiQ2xpZW50IC8gQVBJIEdhdGV3YXkiXQogICAgCiAgICBzdWJncmFwaCBTZXJ2aWNlcwogICAgICAgIE9TWyJPcmRlciBTZXJ2aWNlIDo4MDgxIl0KICAgICAgICBQU1siUGF5bWVudCBTZXJ2aWNlIDo4MDgyIl0KICAgICAgICBJU1siSW52ZW50b3J5IFNlcnZpY2UgOjgwODMiXQogICAgICAgIFNTWyJTaGlwcGluZyBTZXJ2aWNlIDo4MDg0Il0KICAgICAgICBOU1siTm90aWZpY2F0aW9uIFNlcnZpY2UgOjgwODUiXQogICAgZW5kCiAgICAKICAgIHN1YmdyYXBoIEluZnJhc3RydWN0dXJlCiAgICAgICAgS1siQXBhY2hlIEthZmthIl0KICAgICAgICBQRzFbIlBvc3RncmVTUUwgLSBvcmRlcl9kYiJdCiAgICAgICAgUEcyWyJQb3N0Z3JlU1FMIC0gcGF5bWVudF9kYiJdCiAgICAgICAgUEczWyJQb3N0Z3JlU1FMIC0gaW52ZW50b3J5X2RiIl0KICAgICAgICBQRzRbIlBvc3RncmVTUUwgLSBzaGlwcGluZ19kYiJdCiAgICAgICAgUEc1WyJQb3N0Z3JlU1FMIC0gbm90aWZpY2F0aW9uX2RiIl0KICAgIGVuZAogICAgCiAgICBDbGllbnQgLS0+IE9TCiAgICBPUyAtLT4gSwogICAgSyAtLT4gUFMKICAgIEsgLS0+IElTCiAgICBLIC0tPiBTUwogICAgSyAtLT4gTlMKICAgIAogICAgT1MgLS0+IFBHMQogICAgUFMgLS0+IFBHMgogICAgSVMgLS0+IFBHMwogICAgU1MgLS0+IFBHNAogICAgTlMgLS0+IFBHNQo=)

## Saga Flow (Happy Path)

![Diagram](https://mermaid.ink/img/c2VxdWVuY2VEaWFncmFtCiAgICBwYXJ0aWNpcGFudCBDIGFzIENsaWVudAogICAgcGFydGljaXBhbnQgTyBhcyBPcmRlciBTZXJ2aWNlCiAgICBwYXJ0aWNpcGFudCBLIGFzIEthZmthCiAgICBwYXJ0aWNpcGFudCBQIGFzIFBheW1lbnQgU2VydmljZQogICAgcGFydGljaXBhbnQgSSBhcyBJbnZlbnRvcnkgU2VydmljZQogICAgcGFydGljaXBhbnQgUyBhcyBTaGlwcGluZyBTZXJ2aWNlCiAgICBwYXJ0aWNpcGFudCBOIGFzIE5vdGlmaWNhdGlvbiBTZXJ2aWNlCgogICAgQy0+Pk86IFBPU1QgL29yZGVycyAoY3JlYXRlIG9yZGVyKQogICAgTy0+Pk86IFNhdmUgb3JkZXIgKHN0YXR1czogUEVORElORykKICAgIE8tPj5LOiBQdWJsaXNoOiBvcmRlci5jcmVhdGVkCiAgICAKICAgIEstPj5JOiBDb25zdW1lOiBvcmRlci5jcmVhdGVkCiAgICBJLT4+STogUmVzZXJ2ZSBzdG9jawogICAgSS0+Pks6IFB1Ymxpc2g6IGludmVudG9yeS5yZXNlcnZlZAogICAgCiAgICBLLT4+UDogQ29uc3VtZTogaW52ZW50b3J5LnJlc2VydmVkCiAgICBQLT4+UDogUHJvY2VzcyBwYXltZW50CiAgICBQLT4+SzogUHVibGlzaDogcGF5bWVudC5jb21wbGV0ZWQKICAgIAogICAgSy0+PlM6IENvbnN1bWU6IHBheW1lbnQuY29tcGxldGVkCiAgICBTLT4+UzogQ3JlYXRlIHNoaXBtZW50CiAgICBTLT4+SzogUHVibGlzaDogc2hpcHBpbmcuY3JlYXRlZAogICAgCiAgICBLLT4+TzogQ29uc3VtZTogc2hpcHBpbmcuY3JlYXRlZAogICAgTy0+Pk86IFVwZGF0ZSBvcmRlciAoc3RhdHVzOiBDT01QTEVURUQpCiAgICBPLT4+SzogUHVibGlzaDogb3JkZXIuY29tcGxldGVkCiAgICAKICAgIEstPj5OOiBDb25zdW1lOiBvcmRlci5jb21wbGV0ZWQKICAgIE4tPj5OOiBTZW5kIG5vdGlmaWNhdGlvbgo=)

## Saga Flow (Compensation / Rollback)

![Diagram](https://mermaid.ink/img/c2VxdWVuY2VEaWFncmFtCiAgICBwYXJ0aWNpcGFudCBPIGFzIE9yZGVyIFNlcnZpY2UKICAgIHBhcnRpY2lwYW50IEsgYXMgS2Fma2EKICAgIHBhcnRpY2lwYW50IFAgYXMgUGF5bWVudCBTZXJ2aWNlCiAgICBwYXJ0aWNpcGFudCBJIGFzIEludmVudG9yeSBTZXJ2aWNlCiAgICBwYXJ0aWNpcGFudCBOIGFzIE5vdGlmaWNhdGlvbiBTZXJ2aWNlCgogICAgTm90ZSBvdmVyIFA6IFBheW1lbnQgRkFJTEVEIQogICAgUC0+Pks6IFB1Ymxpc2g6IHBheW1lbnQuZmFpbGVkCiAgICAKICAgIEstPj5JOiBDb25zdW1lOiBwYXltZW50LmZhaWxlZAogICAgSS0+Pkk6IFJlbGVhc2UgcmVzZXJ2ZWQgc3RvY2sgKGNvbXBlbnNhdGUpCiAgICBJLT4+SzogUHVibGlzaDogaW52ZW50b3J5LnJlbGVhc2VkCiAgICAKICAgIEstPj5POiBDb25zdW1lOiBwYXltZW50LmZhaWxlZAogICAgTy0+Pk86IFVwZGF0ZSBvcmRlciAoc3RhdHVzOiBGQUlMRUQpCiAgICBPLT4+SzogUHVibGlzaDogb3JkZXIuZmFpbGVkCiAgICAKICAgIEstPj5OOiBDb25zdW1lOiBvcmRlci5mYWlsZWQKICAgIE4tPj5OOiBTZW5kIGZhaWx1cmUgbm90aWZpY2F0aW9uCg==)

## 5 Services

| # | Service | Port | Database | Tanggung Jawab |
|---|---------|------|----------|---------------|
| 1 | **Order Service** | 8081 | order_db | Menerima order, orkestrator saga, track status |
| 2 | **Payment Service** | 8082 | payment_db | Proses pembayaran, refund (compensation) |
| 3 | **Inventory Service** | 8083 | inventory_db | Cek & reserve stok, release stok (compensation) |
| 4 | **Shipping Service** | 8084 | shipping_db | Buat pengiriman, cancel pengiriman (compensation) |
| 5 | **Notification Service** | 8085 | notification_db | Kirim notifikasi (email/log), catat history |

## Kafka Topics

| Topic | Producer | Consumer(s) | Deskripsi |
|-------|----------|-------------|-----------|
| `order.created` | Order Service | Inventory Service | Order baru dibuat |
| `order.completed` | Order Service | Notification Service | Order selesai |
| `order.failed` | Order Service | Notification Service | Order gagal |
| `inventory.reserved` | Inventory Service | Payment Service | Stok berhasil direserve |
| `inventory.failed` | Inventory Service | Order Service | Stok tidak cukup |
| `inventory.released` | Inventory Service | (log only) | Stok di-release (compensation) |
| `payment.completed` | Payment Service | Shipping Service, Order Service | Pembayaran berhasil |
| `payment.failed` | Payment Service | Inventory Service, Order Service | Pembayaran gagal |
| `shipping.created` | Shipping Service | Order Service | Pengiriman dibuat |
| `shipping.failed` | Shipping Service | Payment Service, Order Service | Pengiriman gagal |

## Struktur Folder per Service

```
services/
├── order-service/
│   ├── cmd/
│   │   └── main.go
│   ├── internal/
│   │   ├── handler/
│   │   │   └── order_handler.go
│   │   ├── model/
│   │   │   └── order.go
│   │   ├── repository/
│   │   │   └── order_repository.go
│   │   ├── service/
│   │   │   └── order_service.go
│   │   └── kafka/
│   │       ├── producer.go
│   │       └── consumer.go
│   ├── migrations/
│   │   └── 001_create_orders.sql
│   ├── Dockerfile
│   ├── go.mod
│   └── go.sum
├── payment-service/
│   └── ... (sama strukturnya)
├── inventory-service/
│   └── ...
├── shipping-service/
│   └── ...
└── notification-service/
    └── ...
```

## Proposed Changes

### Infrastructure (Docker)

#### [NEW] docker-compose.yml
- PostgreSQL instance dengan 5 database
- Apache Kafka + Zookeeper (menggunakan KRaft mode via Bitnami image)
- Build & run semua 5 service
- Network dan volume configuration
- Health checks

#### [NEW] scripts/init-db.sh
- Script untuk membuat 5 database saat PostgreSQL pertama kali start

---

### Service 1: Order Service (Port 8081)

#### [NEW] services/order-service/*
- **REST API**: `POST /orders`, `GET /orders/:id`, `GET /orders`
- **Kafka Producer**: Publish `order.created`, `order.completed`, `order.failed`
- **Kafka Consumer**: Consume `payment.completed`, `payment.failed`, `inventory.failed`, `shipping.created`, `shipping.failed`
- **Model**: Order (id, customer_name, product_id, quantity, total_price, status, created_at, updated_at)
- **Status Flow**: PENDING → INVENTORY_RESERVED → PAYMENT_COMPLETED → COMPLETED / FAILED

---

### Service 2: Payment Service (Port 8082)

#### [NEW] services/payment-service/*
- **Kafka Consumer**: Consume `inventory.reserved`, `shipping.failed`
- **Kafka Producer**: Publish `payment.completed`, `payment.failed`
- **Model**: Payment (id, order_id, amount, status, created_at)
- **Simulasi**: Random failure 20% untuk demo compensation
- **Compensation**: Refund payment saat `shipping.failed`

---

### Service 3: Inventory Service (Port 8083)

#### [NEW] services/inventory-service/*
- **REST API**: `GET /products`, `POST /products` (seed data)
- **Kafka Consumer**: Consume `order.created`, `payment.failed`
- **Kafka Producer**: Publish `inventory.reserved`, `inventory.failed`, `inventory.released`
- **Model**: Product (id, name, stock, reserved_stock), InventoryLog (id, order_id, product_id, quantity, action, created_at)
- **Compensation**: Release reserved stock saat `payment.failed`

---

### Service 4: Shipping Service (Port 8084)

#### [NEW] services/shipping-service/*
- **Kafka Consumer**: Consume `payment.completed`
- **Kafka Producer**: Publish `shipping.created`, `shipping.failed`
- **Model**: Shipment (id, order_id, address, status, tracking_number, created_at)
- **Simulasi**: Random failure 10% untuk demo compensation

---

### Service 5: Notification Service (Port 8085)

#### [NEW] services/notification-service/*
- **REST API**: `GET /notifications` (view history)
- **Kafka Consumer**: Consume `order.completed`, `order.failed`
- **Model**: Notification (id, order_id, type, message, status, created_at)
- **Action**: Log notification ke database & console

---

### Shared Package

#### [NEW] pkg/events/events.go
- Shared event types/structs yang digunakan semua service
- Serialization/Deserialization helpers

## Verification Plan

### Manual Verification
1. `docker-compose up --build` — semua service berjalan tanpa error
2. Seed product data via Inventory Service API
3. Buat order via Order Service API — cek saga flow complete
4. Cek semua database — data konsisten
5. Trigger failure scenario — cek compensation berjalan
6. Cek notification log — notifikasi tercatat

### Test Scenarios
1. **Happy Path**: Order → Inventory Reserved → Payment Success → Shipping Created → Order Completed → Notification Sent
2. **Inventory Failed**: Order → Inventory tidak cukup → Order Failed → Notification Sent
3. **Payment Failed**: Order → Inventory Reserved → Payment Failed → Inventory Released → Order Failed → Notification Sent
4. **Shipping Failed**: Order → Inventory Reserved → Payment Success → Shipping Failed → Payment Refunded → Inventory Released → Order Failed → Notification Sent
