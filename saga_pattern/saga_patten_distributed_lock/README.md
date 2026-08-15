# Saga Pattern & Distributed Lock Watchdog Heartbeat

Implementasi lengkap dan teruji mengenai **Saga Pattern (Orchestration dengan Compensating Transactions)** dan **Distributed Lock Watchdog Heartbeat** menggunakan stack teknologi modern:
- **Golang** dengan Framework **Echo v5**
- **PostgreSQL** dengan **PgBouncer** (Connection Pooling)
- **Redis** (Distributed Mutex & Watchdog Renewal)
- **Apache Kafka** (Event-Driven Stream Audit Logging)
- **RabbitMQ** (AMQP Command Queue)
- **Docker Compose** & **Dockerfile**
- **Scenario Shell Script (`scenario.sh`)**

---

## 📚 1. Penjelasan Lengkap Saga Pattern

Dalam sistem terdistribusi (microservices), **ACID Transaction** tradisional (seperti 2PC / Two-Phase Commit) berkinerja buruk dan menghambat skalabilitas. **Saga Pattern** adalah pola arsitektur yang memecah satu transaksi bisnis terdistribusi menjadi sekumpulan transaksi lokal (*local transactions*) yang dieksekusi secara berurutan.

```
[Start Saga] ──► [Step 1: Order Pending (Postgres)]
                      │
                      ▼
                 [Step 2: Reserve Stock (RabbitMQ)]
                      │
                      ├─────────────────────────┐
                      │ SUCCESS                 │ FAIL
                      ▼                         ▼
                 [Step 3: Process Payment]   [Compensating Action Step 1: Cancel Order]
                      │
                      ├─────────────────────────┐
                      │ SUCCESS                 │ FAIL
                      ▼                         ▼
                 [Step 4: Complete Order]    [Compensating Action Step 2: Cancel Stock]
                                             [Compensating Action Step 1: Cancel Order]
```

### Konsep Utama Saga Pattern:
1. **Forward Transactions**: Langkah-langkah transaksi normal yang harus dijalankan berurutan (misal: Create Order ➔ Reserve Inventory ➔ Process Payment ➔ Complete Order).
2. **Compensating Transactions (Rollback)**: Jika salah satu langkah di tengah jalan mengalami kegagalan (misal: Payment gagal), sistem **TIDAK** bisa melakukan `ROLLBACK` database otomatis di service lain. Sebaliknya, Saga Orchestrator mengirimkan *Command Kompensasi* secara eksplisit untuk membatalkan langkah-langkah yang sudah terlanjur sukses sebelumnya (misal: `CANCEL_INVENTORY` ke RabbitMQ dan memutakhirkan status Order di PostgreSQL menjadi `CANCELLED_DUE_TO_PAYMENT_FAILURE`).
3. **Kafka vs RabbitMQ dalam Saga**:
   - **RabbitMQ**: Digunakan untuk *Command Queuing* berkecepatan tinggi antar microservices (`inventory-service-queue`, `payment-service-queue`).
   - **Apache Kafka**: Digunakan untuk mempublikasikan *Event Stream* audit log (`order-events`) secara real-time yang dapat dibaca oleh service analytics/notifications.

---

## 🔒 2. Penjelasan Lengkap Distributed Lock Watchdog Heartbeat

Ketika beberapa instance aplikasi mencoba memproses sumber daya kritis yang sama (misal: memproses stok barang atau pesanan yang sama secara bersamaan), kita memerlukan **Distributed Lock** di Redis (set key dengan flag `NX`).

### Masalah Utama Distributed Lock Tanpa Watchdog:
Jika kita menentukan TTL (Time-to-Live) awal yang terlalu singkat (misal: 3 detik) untuk mengantisipasi crash server, tetapi proses bisnis memakan waktu lebih lama (misal: 8 detik), maka:
- Redis akan menghapus lock secara prematur saat proses masih berjalan.
- Process B akan berhasil mengambil lock padahal Process A belum selesai (terjadi *Race Condition* dan data korup).

### Solusi: Watchdog Heartbeat (Goroutine background):
Watchdog adalah goroutine latar belakang yang secara periodik mengirimkan heartbeat (skrip Lua `PEXPIRE`) ke Redis untuk memperpanjang nilai TTL lock (misal: setiap 1 detik diperpanjang kembali ke 3 detik) **selama dan hanya jika** proses bisnis masih aktif bekerja.

```
Process A                        Redis                            Watchdog (Goroutine)
    │                              │                                      │
    ├── Acquire Lock (TTL 3s) ────►│ SET lock_key token NX PX 3000        │
    │   (Success)                  │                                      │
    │                              │◄── Spawns Watchdog ──────────────────┤
    ├── Starts Heavy Work (8s) ───►│                                      │
    │                              │◄── Heartbeat 1s: PEXPIRE lock_key 3s ┤
    │                              │◄── Heartbeat 1s: PEXPIRE lock_key 3s ┤
    │                              │◄── Heartbeat 1s: PEXPIRE lock_key 3s ┤
    ├── Work Finished ────────────►│                                      │
    └── Unlock() ─────────────────►│ DEL lock_key (Lua Check Token)       ├── Stops Ticker
```

#### Kenapa Aman Terhadap Service Crash?
Jika instance aplikasi panik / mati tiba-tiba, Goroutine Watchdog otomatis berhenti. Redis akan membiarkan lock kadaluarsa secara alami sesuai TTL awal (3 detik), sehingga sumber daya terbebas dari kebuntuan (*deadlock*) tanpa perlu campur tangan manual.

---

## 🏗️ 3. Stuktur Proyek

```
.
├── Dockerfile                   # Multi-stage Dockerfile Go
├── docker-compose.yml           # Stack: Postgres, PgBouncer, Redis, Kafka, RabbitMQ, App
├── go.mod                       # Dependensi Go
├── main.go                      # Echo v5 Server & HTTP Routes
├── pgbouncer/
│   ├── pgbouncer.ini            # Konfigurasi PgBouncer connection pooler
│   └── userlist.txt             # Autentikasi PgBouncer
├── pkg/
│   ├── db/db.go                 # Inisialisasi DB PostgreSQL via PgBouncer
│   ├── lock/watchdog.go         # Implementation Distributed Lock Watchdog Heartbeat
│   └── saga/orchestrator.go     # Saga Orchestrator engine
└── scenario.sh                  # Script pengujian otomatis
```

---

## 🚀 4. Cara Menjalankan Skenario Pengujian

Cukup jalankan script `scenario.sh`:

```bash
./scenario.sh
```

Script `scenario.sh` akan:
1. Menjalankan `docker compose up -d --build` di awal script.
2. Menunggu hingga semua service (Postgres, PgBouncer, Redis, Kafka, RabbitMQ, dan Echo v5 API) dalam kondisi *healthy*.
3. **Uji Coba 1**: Alur transaksi Saga Berhasil (Status Order menjadi `COMPLETED`).
4. **Uji Coba 2**: Alur kompensasi Saga saat Payment Gagal (Melakukan Rollback pembatalan inventory & merubah status Order menjadi `CANCELLED_DUE_TO_PAYMENT_FAILURE`).
5. **Uji Coba 3**: Pengujian Distributed Lock Watchdog Heartbeat (Task berjalan 8 detik dengan TTL awal 3s, membuktikan request konkuren ditolak dengan HTTP 423 Locked).
6. Menjalankan `docker compose down -v` di akhir script untuk membersihkan resource.

---

## 🛠️ REST API Endpoints

- `GET /health` - Healthcheck service
- `POST /api/orders` - Membuat Order baru dengan Saga Transaction & Distributed Lock
  ```json
  {
    "product_id": "PROD-101",
    "quantity": 2,
    "total_price": 150.00,
    "simulate_fail_at": "" // opsi: "", "inventory", "payment"
  }
  ```
- `GET /api/orders/:id` - Memeriksa status Order di PostgreSQL via PgBouncer
- `POST /api/lock/demo` - Demonstrasi langsung Distributed Lock Watchdog Heartbeat
