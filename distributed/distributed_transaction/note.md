# Panduan Belajar Distributed Transaction (Saga/Outbox Pattern)

**Stack:** Golang (Echo), PostgreSQL, Kafka, OpenTelemetry (Otel), Jaeger
**Arsitektur:** 5 Microservices (misal: Order, Payment, Inventory, Shipping, Notification)

Catatan ini menggunakan format checklist. Beri tanda `[x]` jika sudah dijalankan, dan biarkan `[ ]` jika belum.

## Tahap 1: Persiapan Lingkungan (Environment Setup)
- [ ] Install Go (versi 1.20+)
- [ ] Install Docker & Docker Compose (untuk Kafka, PostgreSQL, Jaeger)
- [ ] Buat file `docker-compose.yml` yang berisi:
  - [ ] Zookeeper & Kafka broker
  - [ ] PostgreSQL (5 database untuk masing-masing service)
  - [ ] Jaeger all-in-one (untuk tracing)
- [ ] Jalankan `docker-compose up -d` dan pastikan semua container running.

## Tahap 2: Inisialisasi Proyek & Struktur Repositori
- [ ] Buat Go workspace atau repo utama (monorepo/multirepo).
- [ ] Buat folder untuk 5 services:
  - [ ] `order-service`
  - [ ] `payment-service`
  - [ ] `inventory-service`
  - [ ] `shipping-service`
  - [ ] `notification-service`
- [ ] Jalankan `go mod init` pada masing-masing service.
- [ ] Install framework Echo (`go get github.com/labstack/echo/v4`) di tiap service.
- [ ] Buat *skeleton* API dasar (Hello World) untuk ke-5 service dan pastikan jalan di port yang berbeda (misal: 8081-8085).

## Tahap 3: Konfigurasi Database (PostgreSQL)
- [ ] Install driver PostgreSQL (misal: `gorm` atau `pgx`).
- [ ] Buat koneksi database di masing-masing service.
- [ ] Buat schema/tabel dasar:
  - [ ] Order: tabel `orders`
  - [ ] Payment: tabel `payments`
  - [ ] Inventory: tabel `products`, `stock_reservations`
  - [ ] Shipping: tabel `deliveries`
  - [ ] Notification: tabel `notification_logs`
- [ ] Buat tabel khusus untuk **Outbox Pattern** (tabel `outbox_events`) di tiap service yang mem-publish event.

## Tahap 4: Implementasi Message Broker (Kafka)
- [ ] Install library Kafka untuk Golang (misal: `github.com/confluentinc/confluent-kafka-go` atau `segmentio/kafka-go`).
- [ ] Buat Kafka Producer di service yang membutuhkan (misal: Order service publish `OrderCreated`).
- [ ] Buat Kafka Consumer di service yang mendengarkan (misal: Payment listen `OrderCreated`).
- [ ] Tentukan topic Kafka yang jelas (contoh: `order-events`, `payment-events`).

## Tahap 5: Implementasi Distributed Tracing (Otel & Jaeger)
- [ ] Install package OpenTelemetry Go (`go.opentelemetry.io/otel`).
- [ ] Konfigurasi Otel provider di fungsi `main()` tiap service untuk mengirim trace ke endpoint Jaeger.
- [ ] Tambahkan middleware Otel untuk Echo agar request HTTP otomatis ter-trace.
- [ ] Inject `context` Otel ke dalam Kafka Producer (menggunakan Kafka Headers) agar trace tidak terputus saat melewati message broker.
- [ ] Ekstrak `context` Otel di Kafka Consumer untuk melanjutkan trace span.

## Tahap 6: Implementasi Logika Distributed Transaction (Saga Pattern - Choreography)
- [ ] **Step 1 (Order):** User hit API Create Order -> Simpan status `PENDING` -> Insert event `OrderCreated` ke tabel Outbox -> Outbox relay publish ke Kafka.
- [ ] **Step 2 (Inventory):** Consume `OrderCreated` -> Cek stok. 
  - [ ] Jika sukses: Kurangi stok -> Publish `InventoryReserved`.
  - [ ] Jika gagal: Publish `InventoryFailed` (memicu Order di-cancel).
- [ ] **Step 3 (Payment):** Consume `InventoryReserved` -> Potong saldo.
  - [ ] Jika sukses: Publish `PaymentProcessed`.
  - [ ] Jika gagal: Publish `PaymentFailed` (memicu kompensasi/pengembalian stok dan cancel order).
- [ ] **Step 4 (Shipping):** Consume `PaymentProcessed` -> Buat resi -> Publish `OrderShipped`.
- [ ] **Step 5 (Notification):** Consume berbagai event (`OrderShipped`, `OrderCancelled`, dll) -> Kirim notif/email mock.
- [ ] **Step 6 (Order - Finalize):** Order consume `OrderShipped` -> Ubah status jadi `COMPLETED`.

## Tahap 7: Testing & Simulasi Failure (Rollback/Kompensasi)
- [ ] Tes *Happy Path*: Semua step sukses sampai pengiriman. Cek di Jaeger apakah satu alur *trace* utuh melewati 5 service.
- [ ] Tes *Failure di Payment*: Buat agar saldo tidak cukup -> Cek apakah Inventory mengembalikan stok (Kompensasi) dan status Order menjadi `FAILED`/`CANCELLED`.
- [ ] Tes *Failure di Inventory*: Buat agar stok habis -> Cek apakah Order dibatalkan otomatis.
- [ ] Tes *Eventual Consistency*: Matikan salah satu service (misal Notification), lalu nyalakan lagi, pastikan ia tetap membaca pesan yang tertinggal di Kafka.

saya ingin belajar membuat distributed transaction pada microservices 5 services, saya ingin menggunakan golang echo postgresql kafka otel jeager, buatkan catatan langkah-langkah lengkap mengenai itu beserta tanda bahwa langkah itu sudah dijalankan dan langkah itu belum dijalankan, agar ke depannya tinggal implementasi saja