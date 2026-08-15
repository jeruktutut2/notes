# 🔥 System Design: Flash Sale Platform

## Daftar Isi

1. [Gambaran Umum](#1-gambaran-umum)
2. [Functional & Non-Functional Requirements](#2-functional--non-functional-requirements)
3. [Estimasi Kapasitas (Capacity Estimation)](#3-estimasi-kapasitas)
4. [High-Level Architecture](#4-high-level-architecture)
5. [Komponen & Tools yang Digunakan](#5-komponen--tools-yang-digunakan)
6. [Alur Kerja (Detailed Flow)](#6-alur-kerja-detailed-flow)
7. [Database Design](#7-database-design)
8. [API Design](#8-api-design)
9. [Strategi Inventory Management](#9-strategi-inventory-management)
10. [Rate Limiting & Anti-Bot](#10-rate-limiting--anti-bot)
11. [Failure Handling & Consistency](#11-failure-handling--consistency)
12. [Monitoring & Observability](#12-monitoring--observability)
13. [Scaling Strategy](#13-scaling-strategy)
14. [Security Considerations](#14-security-considerations)
15. [Catatan & Trade-offs](#15-catatan--trade-offs)

---

## 1. Gambaran Umum

Flash sale adalah event penjualan singkat di mana sejumlah kecil produk ditawarkan dengan diskon besar dalam waktu terbatas. Tantangan utamanya:

| Tantangan | Penjelasan |
|-----------|------------|
| **Traffic Spike Ekstrem** | Jutaan user mengakses bersamaan dalam hitungan detik |
| **Overselling Prevention** | Stok 1.000 unit TIDAK boleh terjual 1.001 |
| **Fairness** | Bot tidak boleh mengambil alih, user real harus punya kesempatan |
| **Low Latency** | Response time harus < 200ms di peak load |
| **High Availability** | System tidak boleh down saat event berlangsung |

### Contoh Skenario
- **Produk:** iPhone 16 Pro — 500 unit
- **Harga diskon:** Rp 5.000.000 (dari Rp 20.000.000)
- **Durasi:** 10 menit
- **Prediksi traffic:** 5 juta request dalam 10 menit pertama

---

## 2. Functional & Non-Functional Requirements

### Functional Requirements

| # | Requirement | Detail |
|---|-------------|--------|
| F1 | Registrasi Flash Sale | Admin bisa membuat event flash sale dengan produk, harga, stok, dan jadwal |
| F2 | Countdown Timer | User melihat countdown sebelum sale dimulai |
| F3 | Purchase Flow | User bisa klik "Beli" → validasi stok → proses order |
| F4 | Queue System | Virtual waiting room saat traffic terlalu tinggi |
| F5 | Order Confirmation | User mendapat konfirmasi order (pending → confirmed) |
| F6 | Payment Window | User punya waktu 15 menit untuk bayar, jika tidak stok dikembalikan |
| F7 | Inventory Tracking | Real-time stok tersisa (atau indikator "Hampir Habis") |

### Non-Functional Requirements

| # | Requirement | Target |
|---|-------------|--------|
| NF1 | **Throughput** | 500.000 request/detik di peak |
| NF2 | **Latency** | p99 < 200ms untuk endpoint purchase |
| NF3 | **Availability** | 99.99% selama event |
| NF4 | **Consistency** | Zero overselling (stok tidak boleh negatif) |
| NF5 | **Scalability** | Horizontal scaling untuk handle lonjakan |
| NF6 | **Durability** | Zero data loss untuk transaksi yang berhasil |

---

## 3. Estimasi Kapasitas

### Traffic Estimation

```
Concurrent Users     : 5.000.000
Flash Sale Duration  : 10 menit = 600 detik
Request per User     : ~3 request (page load + API calls)
Total Requests       : 15.000.000
Peak RPS             : ~500.000 req/sec (burst di detik pertama)
Sustained RPS        : ~25.000 req/sec (setelah burst)
```

### Storage Estimation

```
Order Record Size    : ~500 bytes
Max Orders           : 500 (= stok produk)
Order Storage        : 500 × 500 bytes = 250 KB (minimal)
Event Log per req    : ~200 bytes
Total Event Logs     : 15.000.000 × 200 bytes = ~3 GB
Redis Memory         : ~50 MB (inventory + session + rate limit counters)
```

### Bandwidth Estimation

```
Avg Response Size    : ~2 KB
Peak Bandwidth       : 500.000 × 2 KB = ~1 GB/sec (peak)
CDN Offload          : ~80% static content → origin hanya ~200 MB/sec
```

---

## 4. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                         │
│  │ Web App  │  │Mobile App│  │   Bot    │                         │
│  │ (React)  │  │(Flutter) │  │ (Block!) │                         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                         │
│       │              │             │                                │
└───────┼──────────────┼─────────────┼────────────────────────────────┘
        │              │             │
        ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       EDGE LAYER                                    │
│  ┌────────────┐  ┌───────────────┐  ┌────────────────────┐        │
│  │    CDN     │  │   WAF/DDoS    │  │  Virtual Waiting   │        │
│  │(CloudFront)│  │  Protection   │  │      Room          │        │
│  └────┬───────┘  └──────┬────────┘  └─────────┬──────────┘        │
│       │                 │                      │                    │
└───────┼─────────────────┼──────────────────────┼────────────────────┘
        │                 │                      │
        ▼                 ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GATEWAY LAYER                                    │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │              API Gateway (Kong / AWS ALB)                │       │
│  │  • Rate Limiting    • Auth/JWT Validation               │       │
│  │  • Request Routing  • SSL Termination                   │       │
│  │  • Circuit Breaker  • Request Deduplication             │       │
│  └──────────────────────────┬──────────────────────────────┘       │
│                             │                                       │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                                 │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Flash Sale   │  │   Order      │  │   Payment    │             │
│  │  Service     │  │  Service     │  │   Service    │             │
│  │  (Go/Rust)   │  │  (Go/Java)   │  │  (Go/Java)   │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                 │                  │                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Notification │  │   User       │  │  Inventory   │             │
│  │  Service     │  │  Service     │  │   Service    │             │
│  │  (Node.js)   │  │  (Go/Java)   │  │  (Go/Rust)   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
└──────────┬──────────────────┬──────────────────┬────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  DATA & MESSAGING LAYER                             │
│                                                                     │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │  Redis   │  │    Kafka     │  │  PostgreSQL  │                 │
│  │ Cluster  │  │   Cluster    │  │   (Primary)  │                 │
│  │          │  │              │  │              │                 │
│  │• Stok    │  │• Order Queue │  │• Orders      │                 │
│  │• Rate    │  │• Payment     │  │• Users       │                 │
│  │  Limit   │  │  Events      │  │• Products    │                 │
│  │• Session │  │• Notification│  │• Payments    │                 │
│  │• Lock    │  │  Events      │  │              │                 │
│  └──────────┘  └──────────────┘  └──────┬───────┘                 │
│                                         │                          │
│                                  ┌──────┴───────┐                  │
│                                  │  PostgreSQL  │                  │
│                                  │  (Read       │                  │
│                                  │   Replicas)  │                  │
│                                  └──────────────┘                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Komponen & Tools yang Digunakan

### 5.1 Infrastructure & Cloud

| Komponen | Tool | Alasan Pemilihan |
|----------|------|------------------|
| **Cloud Provider** | AWS / GCP | Global infrastructure, auto-scaling, managed services |
| **Container Orchestration** | Kubernetes (EKS/GKE) | Auto-scaling pods saat traffic spike |
| **Container Runtime** | Docker | Konsistensi environment dev → prod |
| **IaC** | Terraform | Infrastructure reproducibility |
| **CI/CD** | GitHub Actions + ArgoCD | GitOps deployment workflow |

### 5.2 Edge & Networking

| Komponen | Tool | Alasan Pemilihan |
|----------|------|------------------|
| **CDN** | CloudFront / CloudFlare | Cache static assets, edge caching, DDoS protection |
| **WAF** | AWS WAF / CloudFlare WAF | Bot protection, IP filtering, geo-blocking |
| **Load Balancer** | AWS ALB / Nginx | L7 load balancing, health checks |
| **DNS** | Route 53 / CloudFlare DNS | Geo-routing, failover |
| **Virtual Waiting Room** | CloudFlare Waiting Room / Custom | Mengantri user secara adil sebelum masuk |

### 5.3 API Gateway

| Komponen | Tool | Alasan Pemilihan |
|----------|------|------------------|
| **Gateway** | Kong / AWS API Gateway | Rate limiting, auth, routing, plugins ecosystem |
| **Service Mesh** | Istio / Linkerd | mTLS, traffic management, observability antar service |

### 5.4 Application Services

| Service | Bahasa | Framework | Tanggung Jawab |
|---------|--------|-----------|----------------|
| **Flash Sale Service** | Go / Rust | Gin / Actix | Core logic: validasi stok, deduct inventory via Redis |
| **Order Service** | Go / Java | Gin / Spring Boot | Consume order dari Kafka, persist ke DB |
| **Payment Service** | Go / Java | Gin / Spring Boot | Integrasi payment gateway, handle callback |
| **User Service** | Go / Java | Gin / Spring Boot | Auth, profile, session management |
| **Inventory Service** | Go / Rust | Gin / Actix | Sync Redis ↔ DB, reconciliation |
| **Notification Service** | Node.js | Express + Socket.io | Push notification, email, WebSocket updates |

> **Kenapa Go/Rust untuk Flash Sale Service?**
> Karena butuh throughput tinggi dengan memory footprint rendah. Go dan Rust unggul di concurrency model (goroutines / async) dan performa raw dibanding Java/Node.js.

### 5.5 Data Layer

| Komponen | Tool | Konfigurasi | Alasan |
|----------|------|-------------|--------|
| **In-Memory Cache** | Redis Cluster (7.x) | 6 nodes (3 master + 3 replica) | Atomic operations, Lua scripting, < 1ms latency |
| **Message Queue** | Apache Kafka | 3+ brokers, replication factor 3 | High throughput, durable, ordered processing |
| **Primary Database** | PostgreSQL 16 | Primary + 2 Read Replicas | ACID compliance, proven reliability |
| **Search/Analytics** | Elasticsearch | 3-node cluster | Real-time analytics, event search |
| **Object Storage** | S3 / GCS | Multi-region | Product images, static assets |

### 5.6 Monitoring & Observability

| Komponen | Tool | Fungsi |
|----------|------|--------|
| **Metrics** | Prometheus + Grafana | Dashboards, alerting (RPS, latency, error rate) |
| **Logging** | ELK Stack (Elasticsearch + Logstash + Kibana) | Centralized logging, log analysis |
| **Tracing** | Jaeger / OpenTelemetry | Distributed tracing antar microservices |
| **Alerting** | PagerDuty / OpsGenie | On-call rotation, incident management |
| **Uptime** | Pingdom / UptimeRobot | External availability monitoring |

### 5.7 Frontend

| Komponen | Tool | Alasan |
|----------|------|--------|
| **Web Framework** | React / Next.js | SSR untuk SEO, fast hydration |
| **State Management** | Zustand / Redux Toolkit | Lightweight, predictable state |
| **Real-time Updates** | WebSocket (Socket.io) | Live stok counter, order status updates |
| **Styling** | Tailwind CSS | Rapid UI development |
| **Mobile** | Flutter / React Native | Cross-platform, single codebase |

---

## 6. Alur Kerja (Detailed Flow)

### 6.1 Pre-Sale Flow (Persiapan Sebelum Event)

```
┌──────────────────────────────────────────────────────────────┐
│                    PRE-SALE (H-1 sampai H-0)                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Admin membuat Flash Sale Event via Admin Dashboard       │
│     └─→ Insert ke DB: product_id, sale_price, stock,        │
│         start_time, end_time                                 │
│                                                              │
│  2. Inventory Pre-heating (T-30 menit)                       │
│     └─→ Load stock ke Redis:                                 │
│         SET flash_sale:{sale_id}:stock 500                   │
│         SET flash_sale:{sale_id}:status "UPCOMING"           │
│                                                              │
│  3. CDN Warming                                              │
│     └─→ Pre-cache product page, images, CSS/JS di edge      │
│                                                              │
│  4. Auto-Scaling Trigger (T-15 menit)                        │
│     └─→ Scale up pods: Flash Sale Service → 50 replicas      │
│     └─→ Scale up pods: Order Service → 20 replicas           │
│     └─→ Warm up DB connection pools                          │
│                                                              │
│  5. Virtual Waiting Room Activated (T-5 menit)               │
│     └─→ User yang masuk page → masuk antrian                 │
│     └─→ Dapat posisi antrian + estimated wait time           │
│                                                              │
│  6. Sale Activation (T-0)                                    │
│     └─→ SET flash_sale:{sale_id}:status "ACTIVE"             │
│     └─→ Broadcast via WebSocket: "SALE STARTED!"             │
│     └─→ Waiting Room mulai release user secara bertahap      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 6.2 Purchase Flow (Alur Pembelian)

```
User clicks "BELI SEKARANG"
        │
        ▼
┌─── [1] CDN / Edge ───┐
│  Static assets served │
│  from edge cache      │
└──────────┬────────────┘
           │ API Request: POST /api/v1/flash-sale/purchase
           ▼
┌─── [2] API Gateway (Kong) ───────────────────────────┐
│                                                       │
│  ✓ JWT Token Validation                               │
│  ✓ Rate Limit Check (100 req/user/min)                │
│  ✓ Idempotency Key Check (user_id + sale_id + sku_id) │
│  ✓ CAPTCHA Token Validation (anti-bot)                │
│                                                       │
│  ✗ Rate exceeded? → 429 Too Many Requests             │
│  ✗ Invalid token? → 401 Unauthorized                  │
│  ✗ Duplicate?     → 200 OK (return existing order)    │
│                                                       │
└──────────┬────────────────────────────────────────────┘
           │
           ▼
┌─── [3] Flash Sale Service ───────────────────────────┐
│                                                       │
│  Step 3a: Validasi Sale Status                        │
│  ┌─────────────────────────────────────────────┐     │
│  │ GET flash_sale:{sale_id}:status              │     │
│  │ if status != "ACTIVE" → 400 "Sale belum/    │     │
│  │                          sudah berakhir"     │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  Step 3b: Cek User Eligibility                        │
│  ┌─────────────────────────────────────────────┐     │
│  │ SISMEMBER flash_sale:{sale_id}:purchased     │     │
│  │          {user_id}                           │     │
│  │ if member → 400 "Anda sudah membeli"         │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  Step 3c: Atomic Stock Deduction (Redis Lua Script)   │
│  ┌─────────────────────────────────────────────┐     │
│  │ local stock = redis.call('GET', KEYS[1])     │     │
│  │ if tonumber(stock) <= 0 then                 │     │
│  │   return -1  -- SOLD OUT                     │     │
│  │ end                                          │     │
│  │ redis.call('DECR', KEYS[1])                  │     │
│  │ redis.call('SADD', KEYS[2], ARGV[1])         │     │
│  │ return tonumber(stock) - 1                   │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  if result == -1 → 410 "Stok Habis"                  │
│                                                       │
│  Step 3d: Publish ke Kafka                            │
│  ┌─────────────────────────────────────────────┐     │
│  │ Topic: order-requests                        │     │
│  │ Key: user_id (partitioning)                  │     │
│  │ Value: {                                     │     │
│  │   order_id, user_id, sale_id,                │     │
│  │   product_id, price, timestamp,              │     │
│  │   idempotency_key                            │     │
│  │ }                                            │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  → 202 Accepted { order_id, status: "PENDING" }       │
│                                                       │
└───────────────────────────────────────────────────────┘
           │
           │ (Async via Kafka)
           ▼
┌─── [4] Order Service (Kafka Consumer) ───────────────┐
│                                                       │
│  Step 4a: Idempotency Check                           │
│  ┌─────────────────────────────────────────────┐     │
│  │ SELECT * FROM orders                         │     │
│  │ WHERE idempotency_key = ?                    │     │
│  │ if exists → skip (already processed)         │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  Step 4b: Create Order Record                         │
│  ┌─────────────────────────────────────────────┐     │
│  │ INSERT INTO orders (                         │     │
│  │   id, user_id, sale_id, product_id,          │     │
│  │   price, status, payment_deadline,           │     │
│  │   created_at                                 │     │
│  │ ) VALUES (...)                               │     │
│  │                                              │     │
│  │ status = "AWAITING_PAYMENT"                  │     │
│  │ payment_deadline = now() + 15 minutes        │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  Step 4c: Publish Order Created Event                 │
│  ┌─────────────────────────────────────────────┐     │
│  │ Topic: order-events                          │     │
│  │ Event: ORDER_CREATED                         │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
└───────────────────────────────────────────────────────┘
           │
           │ (Kafka Event)
           ▼
┌─── [5] Notification Service ─────────────────────────┐
│                                                       │
│  • WebSocket push → User: "Order berhasil dibuat!"    │
│  • Email: Detail order + link pembayaran              │
│  • Push notification (mobile)                         │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### 6.3 Payment Flow

```
User clicks "Bayar Sekarang"
        │
        ▼
┌─── Payment Service ─────────────────────────────────┐
│                                                      │
│  1. Validasi order status == "AWAITING_PAYMENT"      │
│  2. Validasi payment_deadline belum lewat             │
│  3. Create payment record                            │
│  4. Redirect ke Payment Gateway (Midtrans/Xendit)    │
│                                                      │
│  ← Callback dari Payment Gateway                     │
│                                                      │
│  5. if payment SUCCESS:                              │
│     └→ UPDATE orders SET status = "PAID"             │
│     └→ Publish: PAYMENT_COMPLETED event              │
│     └→ Notify user: "Pembayaran berhasil!"           │
│                                                      │
│  6. if payment FAILED:                               │
│     └→ UPDATE orders SET status = "PAYMENT_FAILED"   │
│     └→ INCR flash_sale:{sale_id}:stock (kembalikan)  │
│     └→ SREM flash_sale:{sale_id}:purchased {user_id} │
│     └→ Notify user: "Pembayaran gagal"               │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 6.4 Payment Timeout Flow

```
┌─── Scheduler (Cron / Delayed Queue) ────────────────┐
│                                                      │
│  Every 1 minute:                                     │
│  SELECT * FROM orders                                │
│  WHERE status = 'AWAITING_PAYMENT'                   │
│  AND payment_deadline < NOW()                        │
│                                                      │
│  For each expired order:                             │
│  1. UPDATE orders SET status = "EXPIRED"             │
│  2. Redis: INCR flash_sale:{sale_id}:stock           │
│  3. Redis: SREM flash_sale:{sale_id}:purchased       │
│            {user_id}                                 │
│  4. Publish: ORDER_EXPIRED event                     │
│  5. Notify user: "Waktu pembayaran habis"            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 7. Database Design

### 7.1 Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    users     │       │   flash_sales    │       │   products   │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)          │       │ id (PK)      │
│ email        │       │ product_id (FK)  │───────│ name         │
│ phone        │       │ sale_price       │       │ original_    │
│ name         │       │ original_stock   │       │   price      │
│ password_    │       │ remaining_stock  │       │ description  │
│   hash       │       │ max_per_user     │       │ category     │
│ created_at   │       │ start_time       │       │ image_url    │
│ updated_at   │       │ end_time         │       │ created_at   │
└──────────────┘       │ status           │       └──────────────┘
       │               │ created_at       │
       │               └──────────────────┘
       │                       │
       │    ┌──────────────────┘
       │    │
       ▼    ▼
┌──────────────────────┐       ┌──────────────────┐
│       orders         │       │    payments       │
├──────────────────────┤       ├──────────────────┤
│ id (PK)              │       │ id (PK)          │
│ user_id (FK)         │       │ order_id (FK)    │
│ flash_sale_id (FK)   │───────│ amount           │
│ product_id (FK)      │       │ payment_method   │
│ price                │       │ gateway_ref_id   │
│ status               │       │ status           │
│ idempotency_key (UQ) │       │ paid_at          │
│ payment_deadline     │       │ created_at       │
│ created_at           │       └──────────────────┘
│ updated_at           │
└──────────────────────┘
```

### 7.2 Table Definitions

```sql
-- Flash Sale Events
CREATE TABLE flash_sales (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id      UUID NOT NULL REFERENCES products(id),
    sale_price      DECIMAL(15,2) NOT NULL,
    original_stock  INTEGER NOT NULL CHECK (original_stock > 0),
    remaining_stock INTEGER NOT NULL CHECK (remaining_stock >= 0),
    max_per_user    INTEGER NOT NULL DEFAULT 1,
    start_time      TIMESTAMPTZ NOT NULL,
    end_time        TIMESTAMPTZ NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'DRAFT'
                    CHECK (status IN ('DRAFT','UPCOMING','ACTIVE',
                                      'SOLD_OUT','ENDED','CANCELLED')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_flash_sales_status ON flash_sales(status);
CREATE INDEX idx_flash_sales_start_time ON flash_sales(start_time);

-- Orders
CREATE TABLE orders (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES users(id),
    flash_sale_id     UUID NOT NULL REFERENCES flash_sales(id),
    product_id        UUID NOT NULL REFERENCES products(id),
    price             DECIMAL(15,2) NOT NULL,
    status            VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                      CHECK (status IN ('PENDING','AWAITING_PAYMENT',
                                        'PAID','EXPIRED','CANCELLED',
                                        'REFUNDED','PAYMENT_FAILED')),
    idempotency_key   VARCHAR(255) NOT NULL UNIQUE,
    payment_deadline  TIMESTAMPTZ,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_user_sale ON orders(user_id, flash_sale_id);
CREATE INDEX idx_orders_status_deadline ON orders(status, payment_deadline);
CREATE INDEX idx_orders_idempotency ON orders(idempotency_key);

-- Payments
CREATE TABLE payments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id        UUID NOT NULL REFERENCES orders(id),
    amount          DECIMAL(15,2) NOT NULL,
    payment_method  VARCHAR(50),
    gateway_ref_id  VARCHAR(255),
    status          VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                    CHECK (status IN ('PENDING','PROCESSING',
                                      'SUCCESS','FAILED','REFUNDED')),
    paid_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_gateway_ref ON payments(gateway_ref_id);
```

### 7.3 Redis Data Structures

```
# ─── Inventory ───────────────────────────────────
flash_sale:{sale_id}:stock          → STRING (integer counter)
flash_sale:{sale_id}:status         → STRING ("UPCOMING"|"ACTIVE"|"ENDED")
flash_sale:{sale_id}:purchased      → SET {user_id_1, user_id_2, ...}

# ─── Rate Limiting ──────────────────────────────
rate_limit:purchase:{user_id}       → STRING (counter, TTL 60s)
rate_limit:global:purchase          → STRING (counter, TTL 1s)

# ─── Idempotency ────────────────────────────────
idempotency:{idempotency_key}       → STRING (order_id, TTL 24h)

# ─── Session / Queue ────────────────────────────
waiting_room:{sale_id}              → SORTED SET {user_id: timestamp}
waiting_room:{sale_id}:admitted     → SET {user_id_1, user_id_2, ...}

# ─── Distributed Lock ───────────────────────────
lock:order:{user_id}:{sale_id}      → STRING (lock_token, TTL 10s)
```

---

## 8. API Design

### 8.1 Flash Sale Endpoints

```
┌────────┬──────────────────────────────────┬───────────────────────────┐
│ Method │ Endpoint                         │ Description               │
├────────┼──────────────────────────────────┼───────────────────────────┤
│ GET    │ /api/v1/flash-sales              │ List upcoming/active sales│
│ GET    │ /api/v1/flash-sales/{id}         │ Detail flash sale + stock │
│ POST   │ /api/v1/flash-sales/{id}/join    │ Join waiting room         │
│ GET    │ /api/v1/flash-sales/{id}/status  │ My queue position/status  │
│ POST   │ /api/v1/flash-sales/{id}/purchase│ Attempt to purchase       │
├────────┼──────────────────────────────────┼───────────────────────────┤
│ GET    │ /api/v1/orders                   │ My orders                 │
│ GET    │ /api/v1/orders/{id}              │ Order detail              │
│ POST   │ /api/v1/orders/{id}/pay          │ Initiate payment          │
│ POST   │ /api/v1/orders/{id}/cancel       │ Cancel order              │
├────────┼──────────────────────────────────┼───────────────────────────┤
│ POST   │ /api/v1/webhooks/payment         │ Payment gateway callback  │
└────────┴──────────────────────────────────┴───────────────────────────┘
```

### 8.2 Purchase Request/Response

```json
// POST /api/v1/flash-sales/{id}/purchase
// Headers:
//   Authorization: Bearer <jwt_token>
//   X-Idempotency-Key: usr_123_sale_456_sku_789
//   X-Captcha-Token: <captcha_response>

// Request Body:
{
    "product_id": "prod_abc123",
    "quantity": 1
}

// ─── Success Response (202 Accepted) ───────────
{
    "status": "success",
    "data": {
        "order_id": "ord_xyz789",
        "status": "PENDING",
        "message": "Pesanan Anda sedang diproses",
        "estimated_confirmation": "5 detik",
        "payment_deadline": "2026-08-07T14:15:00+08:00"
    }
}

// ─── Error: Sold Out (410 Gone) ────────────────
{
    "status": "error",
    "error": {
        "code": "SOLD_OUT",
        "message": "Maaf, stok sudah habis"
    }
}

// ─── Error: Rate Limited (429) ─────────────────
{
    "status": "error",
    "error": {
        "code": "RATE_LIMITED",
        "message": "Terlalu banyak permintaan. Coba lagi dalam 30 detik",
        "retry_after": 30
    }
}

// ─── Error: Already Purchased (409 Conflict) ───
{
    "status": "error",
    "error": {
        "code": "ALREADY_PURCHASED",
        "message": "Anda sudah membeli produk ini"
    }
}
```

---

## 9. Strategi Inventory Management

### 9.1 Redis Lua Script (Atomic Stock Deduction)

Ini adalah **jantung** dari sistem flash sale. Script ini berjalan secara **atomic** di Redis (single-threaded execution), sehingga **tidak mungkin** terjadi race condition.

```lua
-- deduct_stock.lua
-- KEYS[1] = flash_sale:{sale_id}:stock
-- KEYS[2] = flash_sale:{sale_id}:purchased
-- KEYS[3] = flash_sale:{sale_id}:status
-- ARGV[1] = user_id
-- ARGV[2] = max_per_user

-- 1. Cek status sale
local status = redis.call('GET', KEYS[3])
if status ~= 'ACTIVE' then
    return {-2, 'SALE_NOT_ACTIVE'}
end

-- 2. Cek apakah user sudah beli
local already_purchased = redis.call('SISMEMBER', KEYS[2], ARGV[1])
if already_purchased == 1 then
    return {-3, 'ALREADY_PURCHASED'}
end

-- 3. Cek & kurangi stok secara atomic
local current_stock = tonumber(redis.call('GET', KEYS[1]))
if current_stock == nil or current_stock <= 0 then
    -- Auto-update status jika stok habis
    redis.call('SET', KEYS[3], 'SOLD_OUT')
    return {-1, 'SOLD_OUT'}
end

-- 4. Deduct stock
local remaining = redis.call('DECR', KEYS[1])

-- 5. Tandai user sudah beli
redis.call('SADD', KEYS[2], ARGV[1])

-- 6. Jika stok habis setelah deduct, update status
if remaining <= 0 then
    redis.call('SET', KEYS[3], 'SOLD_OUT')
end

return {remaining, 'SUCCESS'}
```

### 9.2 Stock Restoration (Saat Payment Gagal/Expired)

```lua
-- restore_stock.lua
-- KEYS[1] = flash_sale:{sale_id}:stock
-- KEYS[2] = flash_sale:{sale_id}:purchased
-- KEYS[3] = flash_sale:{sale_id}:status
-- ARGV[1] = user_id

-- 1. Kembalikan stok
local new_stock = redis.call('INCR', KEYS[1])

-- 2. Hapus user dari purchased set
redis.call('SREM', KEYS[2], ARGV[1])

-- 3. Jika status SOLD_OUT tapi stok sudah ada, ubah ke ACTIVE
local status = redis.call('GET', KEYS[3])
if status == 'SOLD_OUT' and new_stock > 0 then
    redis.call('SET', KEYS[3], 'ACTIVE')
end

return {new_stock, 'RESTORED'}
```

### 9.3 Reconciliation (Post-Sale)

Setelah flash sale berakhir, **wajib** melakukan reconciliation antara Redis dan Database:

```
┌─────────────────────────────────────────────────────────┐
│             POST-SALE RECONCILIATION                     │
│                                                          │
│  1. Compare Redis stock vs DB order count                │
│     Redis remaining_stock + COUNT(orders) == original    │
│                                                          │
│  2. Jika mismatch:                                       │
│     a. DB order count > (original - Redis stock)         │
│        → ALERT! Possible overselling                     │
│        → Manual review + potential refund                 │
│                                                          │
│     b. DB order count < (original - Redis stock)         │
│        → Ada order yang gagal di Kafka consumer           │
│        → Replay Kafka messages / DLQ processing          │
│                                                          │
│  3. Update DB: remaining_stock = Redis stock              │
│  4. Generate reconciliation report                       │
│  5. Clear Redis keys (TTL 24h sebagai safety net)         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 10. Rate Limiting & Anti-Bot

### 10.1 Multi-Layer Rate Limiting

```
Layer 1: CDN/WAF Level
├── CloudFlare Rate Limiting Rules
├── IP-based: 50 req/sec per IP
├── Known bot ASNs → block
└── Geo-blocking jika diperlukan

Layer 2: API Gateway Level (Kong)
├── Global rate limit: 500K req/sec
├── Per-user rate limit: 10 req/sec
├── Per-IP rate limit: 30 req/sec
└── Sliding window algorithm

Layer 3: Application Level
├── Per-user per-endpoint: 3 purchase attempts/menit
├── Token bucket untuk purchase endpoint
└── Circuit breaker ke downstream services

Layer 4: Redis Level
├── Distributed rate limiter (sliding window log)
├── User purchase deduplication
└── Idempotency key check
```

### 10.2 Anti-Bot Measures

| Strategi | Implementasi |
|----------|-------------|
| **CAPTCHA** | Google reCAPTCHA v3 / hCaptcha sebelum purchase |
| **Browser Fingerprinting** | FingerprintJS untuk deteksi headless browser |
| **Behavioral Analysis** | Track mouse movement, scroll pattern, time-on-page |
| **Device Limit** | Max 1 purchase per device fingerprint |
| **Account Age** | Akun harus dibuat minimal H-7 sebelum flash sale |
| **Phone Verification** | Wajib verifikasi nomor HP untuk ikut flash sale |
| **Proof of Work** | Client harus solve mini computational puzzle |
| **Request Signing** | HMAC signature dengan timestamp (anti-replay) |

### 10.3 Sliding Window Rate Limiter (Redis)

```lua
-- sliding_window_rate_limit.lua
-- KEYS[1] = rate_limit:{type}:{identifier}
-- ARGV[1] = window_size (seconds)
-- ARGV[2] = max_requests
-- ARGV[3] = current_timestamp

local key = KEYS[1]
local window = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Hapus entries di luar window
redis.call('ZREMRANGEBYSCORE', key, 0, now - window * 1000)

-- Count current requests dalam window
local count = redis.call('ZCARD', key)

if count >= limit then
    return {0, count, limit}  -- REJECTED
end

-- Add current request
redis.call('ZADD', key, now, now .. ':' .. math.random(1000000))
redis.call('PEXPIRE', key, window * 1000)

return {1, count + 1, limit}  -- ALLOWED
```

---

## 11. Failure Handling & Consistency

### 11.1 Failure Scenarios & Mitigations

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| **Redis down** | Tidak bisa deduct stock | Circuit breaker → tolak semua purchase (Fail-Closed) |
| **Kafka down** | Order tidak bisa diproses | Fallback: tulis langsung ke DB (degraded mode) |
| **DB down** | Order tidak bisa di-persist | Kafka retains messages, replay setelah DB recovery |
| **Payment Gateway down** | User tidak bisa bayar | Extend payment deadline + notify user |
| **Service crash** mid-deduct | Stock terpotong tapi order belum dibuat | Compensation: cron job reconcile Redis vs DB orders |
| **Network partition** | Split brain antara services | Prefer consistency (CP) → reject uncertain requests |
| **Double submit** | User beli 2x | Idempotency key + Redis SISMEMBER check |

### 11.2 Consistency Model

```
┌────────────────────────────────────────────────────────────┐
│                  CONSISTENCY STRATEGY                       │
│                                                             │
│  Source of Truth (During Sale):  REDIS                      │
│  Source of Truth (After Sale):   PostgreSQL                 │
│  Consistency Model:              Eventual Consistency       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Timeline                                │   │
│  │                                                      │   │
│  │  T=0s     Redis DECR (stock deducted)                │   │
│  │  T=0.1s   Kafka message produced                     │   │
│  │  T=0.5s   Kafka message consumed                     │   │
│  │  T=1s     DB INSERT (order created)                  │   │
│  │  T=1.5s   User notified via WebSocket                │   │
│  │                                                      │   │
│  │  ⚠️  Window of inconsistency: 0s - 1s                │   │
│  │  ✅  Eventually consistent after ~1-2 seconds        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### 11.3 Dead Letter Queue (DLQ) Strategy

```
Kafka Consumer gagal proses message
        │
        ▼
┌─── Retry Policy ────────────────────────────┐
│                                              │
│  Retry 1: setelah 1 detik                    │
│  Retry 2: setelah 5 detik                    │
│  Retry 3: setelah 30 detik                   │
│                                              │
│  if masih gagal setelah 3x retry:            │
│  └→ Pindahkan ke Dead Letter Topic           │
│     (order-requests-dlq)                     │
│                                              │
│  DLQ Consumer:                               │
│  └→ Alert ke on-call engineer                │
│  └→ Log ke incident tracking                 │
│  └→ Manual review & resolution               │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 12. Monitoring & Observability

### 12.1 Key Metrics Dashboard (Grafana)

```
┌─────────────────────────────────────────────────────────────┐
│                    FLASH SALE DASHBOARD                      │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Total RPS   │  │  Error Rate │  │   p99 Lat   │        │
│  │   245,302    │  │    0.03%    │  │    47ms     │        │
│  │  ▲ 12%/sec   │  │  ✅ < 1%    │  │  ✅ < 200ms │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Stock Left   │  │ Orders Made │  │ Payments OK │        │
│  │     127      │  │     373     │  │     298     │        │
│  │  🔴 < 25%    │  │  ▲ 5/sec    │  │  79.8%      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                              │
│  ┌─────────────────────────────────────────────────┐       │
│  │  RPS Over Time                                   │       │
│  │  500K ┤                                          │       │
│  │       │  ╭──╮                                    │       │
│  │  250K ┤  │  ╰───╮                                │       │
│  │       │  │      ╰────────╮                       │       │
│  │    0  ┤──╯               ╰───────────────────    │       │
│  │       └─────────────────────────────────────→    │       │
│  │       T=0   T+30s  T+1m   T+2m    T+5m          │       │
│  └─────────────────────────────────────────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 12.2 Alert Rules

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| High Error Rate | error_rate > 5% for 1 min | 🔴 P1 | Page on-call |
| High Latency | p99 > 500ms for 2 min | 🟡 P2 | Investigate |
| Redis Memory | memory_used > 80% | 🟡 P2 | Scale Redis |
| Kafka Lag | consumer_lag > 10000 | 🟡 P2 | Scale consumers |
| Stock Mismatch | redis_stock != expected | 🔴 P1 | Halt sale + investigate |
| Pod Restarts | restart_count > 3 in 5 min | 🟡 P2 | Check logs |
| DB Connection Pool | usage > 90% | 🔴 P1 | Scale connections |
| DLQ Messages | dlq_count > 0 | 🟡 P2 | Manual review |

### 12.3 Distributed Tracing

```
Trace: purchase_request_abc123
├── [Gateway] JWT Validation ──────────── 2ms
├── [Gateway] Rate Limit Check ────────── 1ms
├── [FlashSale] Status Validation ─────── 0.5ms (Redis GET)
├── [FlashSale] User Eligibility ──────── 0.3ms (Redis SISMEMBER)
├── [FlashSale] Stock Deduction ───────── 0.8ms (Redis Lua Script)
├── [FlashSale] Kafka Produce ─────────── 3ms
│   ├── [OrderSvc] Kafka Consume ──────── 15ms
│   ├── [OrderSvc] Idempotency Check ──── 5ms (DB query)
│   ├── [OrderSvc] Insert Order ───────── 12ms (DB insert)
│   └── [OrderSvc] Publish Event ──────── 2ms (Kafka)
│       └── [NotifSvc] WebSocket Push ─── 5ms
└── Total: ~47ms (sync path: ~7.6ms)
```

---

## 13. Scaling Strategy

### 13.1 Horizontal Pod Autoscaling (HPA)

```yaml
# Kubernetes HPA Configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flash-sale-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flash-sale-service
  minReplicas: 5
  maxReplicas: 100
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "10000"  # 10K RPS per pod
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 15    # Cepat scale up
      policies:
        - type: Pods
          value: 10
          periodSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 300   # Lambat scale down
      policies:
        - type: Pods
          value: 5
          periodSeconds: 60
```

### 13.2 Pre-Scaling Schedule

```
┌──────────────────────────────────────────────────────────┐
│              PRE-SCALING TIMELINE                         │
│                                                           │
│  T-60min  │ Alert: Flash sale in 1 hour                   │
│  T-30min  │ Scale Flash Sale Service: 5 → 50 pods         │
│  T-30min  │ Scale Order Service: 3 → 20 pods              │
│  T-30min  │ Redis: Inventory pre-heating                  │
│  T-15min  │ CDN: Warm cache for product pages             │
│  T-5min   │ Activate Virtual Waiting Room                 │
│  T-0      │ Sale starts! Release users gradually          │
│  T+10min  │ Sale ends / Stock depleted                    │
│  T+30min  │ Begin scale-down (gradual)                    │
│  T+60min  │ Back to normal capacity                       │
│  T+2hr    │ Run reconciliation                            │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 13.3 Database Scaling

```
Write Path (Primary):
  └─→ PostgreSQL Primary
      ├── Connection Pooling: PgBouncer (max 500 connections)
      ├── Sharding: by flash_sale_id (jika multi-event)
      └── Batch inserts dari Kafka consumer

Read Path (Replicas):
  └─→ PostgreSQL Read Replicas (2x)
      ├── Order status queries
      ├── Analytics queries
      └── Admin dashboard queries

Cache Layer:
  └─→ Redis
      ├── Hot data: stok, status, user purchase set
      ├── Session data
      └── Rate limit counters
```

---

## 14. Security Considerations

### 14.1 Security Layers

| Layer | Measure | Detail |
|-------|---------|--------|
| **Network** | VPC + Private Subnets | Services tidak exposed ke internet langsung |
| **Transport** | TLS 1.3 everywhere | End-to-end encryption |
| **Auth** | JWT + Refresh Token | Short-lived access token (15 min) |
| **API** | HMAC Request Signing | Prevent request tampering |
| **Anti-Bot** | CAPTCHA + Fingerprinting | Block automated purchases |
| **Data** | Encryption at rest | AES-256 untuk PII |
| **Secrets** | AWS Secrets Manager / Vault | No hardcoded credentials |
| **Audit** | Immutable audit log | Semua purchase attempts di-log |

### 14.2 Fraud Detection

```
┌─── Fraud Detection Pipeline ─────────────────────────┐
│                                                       │
│  Real-time checks (saat purchase):                    │
│  ├── Same IP, multiple accounts → flag               │
│  ├── Account created < 24h ago → block               │
│  ├── Velocity check: > 3 attempts/min → block        │
│  └── Device fingerprint reuse → flag                 │
│                                                       │
│  Post-sale analysis:                                  │
│  ├── Bulk purchase patterns → review                 │
│  ├── Payment from stolen cards → refund + ban        │
│  └── Reseller detection → future ban                 │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

## 15. Catatan & Trade-offs

### 15.1 Key Design Decisions

| Decision | Chosen | Alternative | Reasoning |
|----------|--------|-------------|-----------|
| Inventory di Redis vs DB | **Redis** | Database with SELECT FOR UPDATE | DB lock contention akan crash system di 500K RPS |
| Async order via Kafka | **Kafka** | Synchronous DB write | Decouple purchase dari order creation, handle backpressure |
| Eventual vs Strong Consistency | **Eventual** | 2PC / SAGA | Performa > strong consistency untuk kasus ini. Window ~1-2 detik acceptable |
| Go/Rust vs Java/Node | **Go** | Java, Node.js | Lower memory, higher concurrency per pod, faster cold start |
| Virtual Waiting Room | **Yes** | First-come-first-serve free-for-all | Fairness + controlled traffic = predictable system behavior |
| Payment deadline 15 min | **15 min** | 5 min, 30 min, 1 hour | Balance antara UX (user butuh waktu) dan stock holding cost |

### 15.2 Trade-offs to Be Aware Of

```
⚠️ TRADE-OFF #1: Consistency vs Performance
   Redis atomic ops = blazing fast, tapi jika Redis crash,
   ada window dimana stok sudah terpotong tapi order belum ada di DB.
   Mitigation: Reconciliation job + Redis persistence (RDB + AOF)

⚠️ TRADE-OFF #2: Fairness vs Throughput
   Virtual Waiting Room membatasi throughput (controlled release),
   tapi memberikan pengalaman lebih fair untuk user.
   Tanpa waiting room, bot dengan koneksi cepat selalu menang.

⚠️ TRADE-OFF #3: Over-rejection vs Overselling
   System lebih memilih over-reject (menolak user yang seharusnya bisa beli)
   daripada oversell (menjual lebih dari stok).
   Ini design choice yang DISENGAJA — overselling jauh lebih mahal.

⚠️ TRADE-OFF #4: Cost vs Performance
   50 pods × 24/7 = mahal. Tapi flash sale hanya 10 menit.
   Solusi: Pre-scale hanya saat event, scale down setelahnya.
   Serverless alternative (Lambda) punya cold start problem.

⚠️ TRADE-OFF #5: UX vs Security
   Terlalu banyak security check (CAPTCHA, OTP, puzzle) = UX buruk.
   Terlalu sedikit = bot menguasai.
   Balance: reCAPTCHA v3 (invisible) + account age requirement.
```

### 15.3 What Could Go Wrong (Known Risks)

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Redis cluster failure | Low | 🔴 Critical | Multi-AZ deployment, automatic failover, Fail-Closed |
| Kafka consumer lag | Medium | 🟡 High | Auto-scale consumers, monitor lag, DLQ |
| DDoS attack during sale | Medium | 🔴 Critical | CloudFlare DDoS protection, WAF rules, geo-blocking |
| Payment gateway overload | Medium | 🟡 High | Multiple gateway fallback, extend deadline |
| Stock reconciliation mismatch | Low | 🟡 High | Automated alerts, manual review process |
| Thundering herd on sale start | High | 🟡 High | Virtual waiting room + gradual release |

### 15.4 Future Improvements

- [ ] **Machine Learning Fraud Detection** — Real-time ML model untuk deteksi bot/fraud
- [ ] **Geo-distributed Flash Sale** — Multi-region deployment untuk latency rendah
- [ ] **Dynamic Pricing** — Adjust harga berdasarkan demand real-time
- [ ] **Reservation System** — Allow VIP users to pre-reserve
- [ ] **A/B Testing Framework** — Test different UX flows untuk conversion optimization
- [ ] **Chaos Engineering** — Regular failure injection untuk test resilience
- [ ] **GraphQL Gateway** — Reduce over-fetching untuk mobile clients

---

## Ringkasan Arsitektur (TL;DR)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  USER  ──→  CDN ──→  WAF ──→  Waiting Room ──→  API Gateway     │
│                                                    │             │
│                                                    ▼             │
│                                            Flash Sale Service    │
│                                            (Redis Lua: DECR)     │
│                                                    │             │
│                                                    ▼             │
│                                               Kafka Queue        │
│                                                    │             │
│                                                    ▼             │
│                                             Order Service        │
│                                            (PostgreSQL INSERT)   │
│                                                    │             │
│                                              ┌─────┴─────┐      │
│                                              ▼           ▼      │
│                                         Notification  Payment   │
│                                          Service      Service   │
│                                                                  │
│  Prinsip: TOLAK secepat mungkin, PROSES sesedikit mungkin,       │
│           SIMPAN seaman mungkin                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> **Filosofi utama:** Dari 5 juta request, hanya 500 yang berhasil beli.
> Jadi tugas utama sistem adalah **menolak 4.999.500 request secepat dan seefisien mungkin**, bukan memproses semuanya.
