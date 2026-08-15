# Distributed Transaction - Master Checklist

> **PENTING**: Checklist ini digunakan untuk tracking progress.
> Jika token habis, baca file ini dan lanjutkan dari item yang belum di-check `[ ]`.

---

## 1. Infrastructure & Docker

- [x] `docker-compose.yml` — PostgreSQL, Kafka (KRaft), 5 services
- [x] `scripts/init-db.sh` — Script init 5 database
- [x] `.env` — Environment variables

---

## 2. Shared Package

- [x] `pkg/events/events.go` — Event types & constants (topic names, event structs)
- [x] `pkg/kafka/producer.go` — Kafka producer wrapper (reusable)
- [x] `pkg/kafka/consumer.go` — Kafka consumer wrapper (reusable)
- [x] `pkg/config/config.go` — Shared config loader

---

## 3. Order Service (Port 8081)

- [x] `go.mod` & `go.sum` — Dependencies resolved
- [x] `services/order-service/cmd/main.go` — Entry point, init Echo + Kafka
- [x] `services/order-service/internal/model/order.go` — Order model & status constants
- [x] `services/order-service/internal/repository/order_repository.go` — CRUD database
- [x] `services/order-service/internal/service/order_service.go` — Business logic
- [x] `services/order-service/internal/handler/order_handler.go` — REST endpoints
- [x] `services/order-service/internal/kafka/consumer.go` — Consume & handle saga events
- [x] `services/order-service/migrations/001_create_orders.sql`
- [x] `services/order-service/Dockerfile`

---

## 4. Payment Service (Port 8082)

- [x] `services/payment-service/cmd/main.go`
- [x] `services/payment-service/internal/model/payment.go`
- [x] `services/payment-service/internal/repository/payment_repository.go`
- [x] `services/payment-service/internal/service/payment_service.go` — Simulasi payment + random failure 20%
- [x] `services/payment-service/internal/handler/payment_handler.go`
- [x] `services/payment-service/internal/kafka/consumer.go`
- [x] `services/payment-service/migrations/001_create_payments.sql`
- [x] `services/payment-service/Dockerfile`

---

## 5. Inventory Service (Port 8083)

- [x] `services/inventory-service/cmd/main.go`
- [x] `services/inventory-service/internal/model/product.go` — Product & InventoryLog
- [x] `services/inventory-service/internal/repository/inventory_repository.go`
- [x] `services/inventory-service/internal/service/inventory_service.go` — Reserve/release stock
- [x] `services/inventory-service/internal/handler/inventory_handler.go`
- [x] `services/inventory-service/internal/kafka/consumer.go`
- [x] `services/inventory-service/migrations/001_create_products.sql`
- [x] `services/inventory-service/Dockerfile`

---

## 6. Shipping Service (Port 8084)

- [x] `services/shipping-service/cmd/main.go`
- [x] `services/shipping-service/internal/model/shipment.go`
- [x] `services/shipping-service/internal/repository/shipping_repository.go`
- [x] `services/shipping-service/internal/service/shipping_service.go` — Simulasi shipping + random failure 10%
- [x] `services/shipping-service/internal/handler/shipping_handler.go`
- [x] `services/shipping-service/internal/kafka/consumer.go`
- [x] `services/shipping-service/migrations/001_create_shipments.sql`
- [x] `services/shipping-service/Dockerfile`

---

## 7. Notification Service (Port 8085)

- [x] `services/notification-service/cmd/main.go`
- [x] `services/notification-service/internal/model/notification.go`
- [x] `services/notification-service/internal/repository/notification_repository.go`
- [x] `services/notification-service/internal/service/notification_service.go`
- [x] `services/notification-service/internal/handler/notification_handler.go`
- [x] `services/notification-service/internal/kafka/consumer.go`
- [x] `services/notification-service/migrations/001_create_notifications.sql`
- [x] `services/notification-service/Dockerfile`

---

## 8. Verifikasi Build

- [x] `go mod tidy` — Dependencies resolved successfully
- [x] `go build ./...` — Semua service compile tanpa error

---

## 9. Testing & Deploy

- [ ] `docker-compose up --build` — Semua service jalan tanpa error
- [ ] Test Happy Path — `POST /orders` → cek status jadi `COMPLETED`
- [ ] Test Inventory Failed — Order dengan qty > stock
- [ ] Test Payment Failed — Buat beberapa order, cek ada yang `FAILED` (20% chance)
- [ ] Test Shipping Failed — Buat beberapa order, cek compensation chain (10% chance)

---

## 10. Dokumentasi

- [x] `README.md` — Cara setup, run, dan test
- [x] `checklist.md` — File ini
