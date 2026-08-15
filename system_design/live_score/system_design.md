# ⚽ System Design: Live Score Platform

## Daftar Isi

1. [Gambaran Umum](#1-gambaran-umum)
2. [Functional & Non-Functional Requirements](#2-functional--non-functional-requirements)
3. [Estimasi Kapasitas (Capacity Estimation)](#3-estimasi-kapasitas)
4. [High-Level Architecture](#4-high-level-architecture)
5. [Komponen & Tools yang Digunakan](#5-komponen--tools-yang-digunakan)
6. [Alur Kerja (Detailed Flow)](#6-alur-kerja-detailed-flow)
7. [Real-Time Delivery Deep Dive](#7-real-time-delivery-deep-dive)
8. [Database Design](#8-database-design)
9. [API Design](#9-api-design)
10. [Caching Strategy](#10-caching-strategy)
11. [Data Ingestion & Provider Management](#11-data-ingestion--provider-management)
12. [Failure Handling & Consistency](#12-failure-handling--consistency)
13. [Monitoring & Observability](#13-monitoring--observability)
14. [Scaling Strategy](#14-scaling-strategy)
15. [Security Considerations](#15-security-considerations)
16. [Catatan & Trade-offs](#16-catatan--trade-offs)

---

## 1. Gambaran Umum

Live Score adalah platform yang menyediakan update skor pertandingan olahraga secara **real-time** kepada jutaan pengguna secara bersamaan. Tantangan utamanya:

| Tantangan | Penjelasan |
|-----------|------------|
| **Extreme Read-Heavy** | Rasio baca:tulis bisa mencapai 100.000:1 — jutaan user membaca, hanya beberapa data source yang menulis |
| **Ultra-Low Latency** | Update skor harus sampai ke user dalam < 1-2 detik dari kejadian nyata di lapangan |
| **Massive Concurrency** | Pertandingan besar (Final Piala Dunia, El Clasico) bisa menghasilkan 50+ juta concurrent viewers |
| **Data Accuracy** | Skor yang ditampilkan HARUS akurat — error skor bisa berdampak serius (gambling, media) |
| **High Availability** | Platform harus tetap hidup 24/7, karena pertandingan olahraga terjadi di seluruh zona waktu |
| **Multi-Sport Support** | Harus mendukung berbagai olahraga: sepakbola, basket, tenis, cricket, dll. |

### Contoh Skenario
- **Event:** Final Piala Dunia 2026
- **Concurrent Users:** 50.000.000+
- **Update Frequency:** Setiap 1-5 detik per pertandingan aktif
- **Total Live Matches:** 500+ pertandingan di berbagai liga secara bersamaan
- **Jenis Update:** Goal, kartu, substitusi, half-time, penalti, statistik real-time

---

## 2. Functional & Non-Functional Requirements

### Functional Requirements

| # | Requirement | Detail |
|---|-------------|--------|
| F1 | Live Score Updates | User menerima update skor secara real-time tanpa perlu refresh halaman |
| F2 | Match Listing | Daftar pertandingan yang sedang berlangsung, akan datang, dan sudah selesai |
| F3 | Match Detail | Detail pertandingan lengkap: lineup, timeline events, statistik |
| F4 | Match Events Timeline | Kronologi event: gol, kartu kuning/merah, substitusi, penalti, VAR decision |
| F5 | Live Commentary | Komentar pertandingan teks secara real-time |
| F6 | League Standings | Klasemen liga yang ter-update otomatis setelah pertandingan selesai |
| F7 | Push Notifications | Notifikasi untuk gol, mulai/selesai pertandingan, dan event penting lainnya |
| F8 | Favorite Teams | User bisa follow tim favorit dan mendapat notifikasi khusus |
| F9 | Multi-Sport | Support berbagai cabang olahraga (sepakbola, basket, tenis, dll.) |
| F10 | Historical Data | Akses data pertandingan yang sudah berlalu (arsip) |
| F11 | Search | Cari tim, pemain, liga, atau pertandingan |
| F12 | Live Match Statistics | Statistik real-time: possession, shots, corners, passes, dll. |

### Non-Functional Requirements

| # | Requirement | Target |
|---|-------------|--------|
| NF1 | **Latency (Delivery)** | Update skor sampai ke user dalam < 2 detik dari data source |
| NF2 | **Throughput** | Handle 10.000.000+ WebSocket connections secara bersamaan |
| NF3 | **Availability** | 99.99% uptime (< 52 menit downtime/tahun) |
| NF4 | **Read Throughput** | 1.000.000+ read requests/detik untuk API polling |
| NF5 | **Scalability** | Horizontal scaling untuk handle event besar (Piala Dunia, Olimpiade) |
| NF6 | **Data Freshness** | Data pertandingan aktif tidak boleh stale > 5 detik |
| NF7 | **Data Accuracy** | 100% akurasi skor — zero tolerance untuk skor salah |
| NF8 | **Global Reach** | Low latency access dari seluruh dunia (< 100ms API response) |

---

## 3. Estimasi Kapasitas

### Traffic Estimation

```
Peak Concurrent Users    : 50.000.000 (saat event besar seperti Final Piala Dunia)
Daily Active Users       : 10.000.000 (hari biasa dengan liga-liga top Eropa)
WebSocket Connections    : 10.000.000 (peak, ~20% dari concurrent viewers)
API Polling Requests     : 5.000.000 req/min (user yang tidak pakai WebSocket)
Peak Read RPS            : ~1.000.000 req/sec
Peak Write RPS           : ~5.000 req/sec (dari data providers)
Matches per Day          : ~2.000 pertandingan di seluruh dunia
Live Matches at Peak     : ~500 pertandingan simultan
Events per Match         : ~200-500 events (gol, kartu, statistik update, commentary)
```

### Storage Estimation

```
Per Match Data           : ~50 KB (skor, events, stats, lineup)
Per Commentary Entry     : ~500 bytes
Commentaries per Match   : ~300 entries = ~150 KB
Per Match Total          : ~200 KB
Daily Storage (all)      : 2.000 × 200 KB = ~400 MB/hari
Monthly Storage          : ~12 GB
Yearly Storage           : ~150 GB
Historical Data (10yr)   : ~1.5 TB

Redis Cache (hot data)   : ~5 GB (semua live matches + recent data)
```

### Bandwidth Estimation

```
WebSocket Update Size    : ~500 bytes per event
Updates per Second       : ~1.000 events/sec (semua pertandingan)
Fan-out Factor           : 10.000.000 subscribers (peak)

Peak Outbound WS         : 1.000 × 500 bytes × fan-out factor
                         : ~5 TB/sec (total, sebelum optimasi)
                         : dengan topic-based pub/sub → ~50 GB/sec (actual)

API Response Size        : ~5 KB (match detail)
API Bandwidth (peak)     : 1.000.000 × 5 KB = ~5 GB/sec
CDN Offload              : ~85% → origin hanya ~750 MB/sec
```

### Kenapa Fan-out Perlu Dioptimasi?

```
Naif: 1 update × 10M user = 10M individual messages = IMPOSSIBLE
Optimasi:
  └─→ Topic-based pub/sub (per match)
  └─→ Match populer: 5M user, match biasa: 1K user
  └─→ Edge servers fan-out di layer terakhir
  └─→ Batching: kirim batch update setiap 1-2 detik
  └─→ Actual per-server fan-out: ~50K connections per server
```

---

## 4. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                       DATA SOURCE LAYER                              │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Opta / Stats│  │  SportRadar  │  │   Manual     │              │
│  │  Perform     │  │              │  │   Input      │              │
│  │  (Primary)   │  │  (Secondary) │  │  (Fallback)  │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                       │
└─────────┼─────────────────┼──────────────────┼───────────────────────┘
          │                 │                  │
          ▼                 ▼                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                                    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │              Data Ingestion Service (Go)                    │     │
│  │  • Normalize data dari berbagai provider                   │     │
│  │  • Validasi & deduplication                                │     │
│  │  • Provider failover (primary → secondary → manual)        │     │
│  │  • Conflict resolution (jika 2 source beda skor)           │     │
│  └──────────────────────────┬─────────────────────────────────┘     │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                 PROCESSING & MESSAGING LAYER                         │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Apache Kafka Cluster                       │   │
│  │                                                              │   │
│  │  Topics:                                                     │   │
│  │  ├── raw-match-events     (dari ingestion, belum diproses)  │   │
│  │  ├── processed-events     (sudah divalidasi & enriched)     │   │
│  │  ├── score-updates        (khusus perubahan skor)           │   │
│  │  ├── notification-events  (trigger push notification)       │   │
│  │  └── analytics-events     (untuk analytics pipeline)        │   │
│  │                                                              │   │
│  └────────────────────────────┬─────────────────────────────────┘   │
│                               │                                      │
│  ┌────────────────────────────┴─────────────────────────────────┐   │
│  │            Event Processing Service (Go/Rust)                │   │
│  │  • Event enrichment (tambah nama pemain, info tim, dll.)     │   │
│  │  • Business logic (update standings, stats aggregation)      │   │
│  │  • Fan-out routing decisions                                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
                    ▼          ▼          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                        │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │    Redis     │  │  PostgreSQL  │  │ Elasticsearch│              │
│  │   Cluster    │  │              │  │              │              │
│  │              │  │              │  │              │              │
│  │ • Live match │  │ • Historical │  │ • Full-text  │              │
│  │   data (hot) │  │   match data │  │   search     │              │
│  │ • Real-time  │  │ • Standings  │  │ • Analytics  │              │
│  │   stats      │  │ • User prefs │  │ • Log search │              │
│  │ • Pub/Sub    │  │ • Teams/     │  │              │              │
│  │   channels   │  │   Players    │  │              │              │
│  └──────┬───────┘  └──────────────┘  └──────────────┘              │
│         │                                                            │
└─────────┼────────────────────────────────────────────────────────────┘
          │ (Pub/Sub)
          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                 REAL-TIME DELIVERY LAYER                              │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │          WebSocket Gateway Cluster (Go / Rust)               │   │
│  │                                                              │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐      ┌────────┐       │   │
│  │  │ WS     │  │ WS     │  │ WS     │ ...  │ WS     │       │   │
│  │  │Server 1│  │Server 2│  │Server 3│      │Server N│       │   │
│  │  │ 50K    │  │ 50K    │  │ 50K    │      │ 50K    │       │   │
│  │  │ conns  │  │ conns  │  │ conns  │      │ conns  │       │   │
│  │  └────────┘  └────────┘  └────────┘      └────────┘       │   │
│  │                                                              │   │
│  │  Total: 200 servers × 50K = 10M concurrent connections      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
          ▲
          │ (WebSocket / SSE / Long Polling)
          │
┌──────────────────────────────────────────────────────────────────────┐
│                       EDGE & CLIENT LAYER                            │
│                                                                      │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐                     │
│  │   CDN    │  │   API        │  │   WAF    │                     │
│  │(CloudFl.)│  │  Gateway     │  │  + DDoS  │                     │
│  └──────────┘  └──────────────┘  └──────────┘                     │
│       ▲               ▲                ▲                            │
│       │               │                │                            │
│  ┌────┴────┐   ┌──────┴─────┐   ┌─────┴──────┐                   │
│  │ Web App │   │ Mobile App │   │  3rd Party  │                   │
│  │ (React) │   │ (Flutter)  │   │  (API/      │                   │
│  │         │   │            │   │   Widget)   │                   │
│  └─────────┘   └────────────┘   └────────────┘                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Komponen & Tools yang Digunakan

### 5.1 Data Providers (Sumber Data)

| Provider | Tipe | Coverage | Latency | Harga |
|----------|------|----------|---------|-------|
| **Opta (Stats Perform)** | Primary | 1.000+ liga, 30+ olahraga | ~1-3 detik | $$$$$ (Enterprise) |
| **SportRadar** | Secondary/Backup | 900+ liga, 25+ olahraga | ~2-5 detik | $$$$ |
| **API-Football** | Budget Alternative | 800+ liga, sepakbola | ~5-15 detik | $$ |
| **Manual Input** | Fallback | Custom coverage | Real-time (operator) | $ (staff cost) |

> **Kenapa Multiple Providers?**
> - **Redundancy:** Jika Opta down, SportRadar jadi fallback otomatis
> - **Cross-validation:** Bandingkan data dari 2 source untuk deteksi anomali
> - **Coverage Gap:** Liga kecil mungkin hanya di-cover oleh 1 provider

### 5.2 Infrastructure & Cloud

| Komponen | Tool | Alasan Pemilihan |
|----------|------|------------------|
| **Cloud Provider** | AWS / GCP | Global presence, managed services, auto-scaling |
| **Container Orchestration** | Kubernetes (EKS/GKE) | Auto-scaling pods per service |
| **Container Runtime** | Docker | Konsistensi environment |
| **IaC** | Terraform | Infrastructure as code, reproducible |
| **CI/CD** | GitHub Actions + ArgoCD | GitOps deployment workflow |
| **Multi-Region** | AWS Global Accelerator / GCP Anycast | Low latency worldwide |

### 5.3 Edge & Networking

| Komponen | Tool | Alasan Pemilihan |
|----------|------|------------------|
| **CDN** | CloudFlare / CloudFront | Cache API responses di edge, global PoP |
| **WAF** | CloudFlare WAF | Bot protection, rate limiting |
| **Load Balancer** | AWS NLB (L4) + ALB (L7) | NLB untuk WebSocket (persistent conn), ALB untuk HTTP API |
| **DNS** | Route 53 / CloudFlare DNS | Latency-based routing, health checks |
| **WebSocket LB** | Sticky sessions via NLB | Maintain persistent connection ke server yang sama |

### 5.4 API Gateway

| Komponen | Tool | Alasan Pemilihan |
|----------|------|------------------|
| **Gateway** | Kong / AWS API Gateway | Rate limiting, auth, caching, throttling |
| **Service Mesh** | Istio / Linkerd | mTLS antar service, traffic management |

### 5.5 Application Services

| Service | Bahasa | Framework | Tanggung Jawab |
|---------|--------|-----------|----------------|
| **Data Ingestion Service** | Go | Custom + gRPC | Consume data dari providers, normalize, validate, dedup |
| **Event Processing Service** | Go / Rust | Custom | Enrich events, business logic, route ke subscribers |
| **Match Service** | Go | Gin / Fiber | CRUD match data, match lifecycle management |
| **WebSocket Gateway** | Go / Rust | Custom (epoll-based) | Manage 50K+ WebSocket connections per instance |
| **Notification Service** | Go / Node.js | Gin / Express | Push notification (FCM/APNs), email digest |
| **User Service** | Go | Gin | Auth, user preferences, favorite teams |
| **Search Service** | Go / Python | Gin / FastAPI | Search tim, pemain, liga (backed by Elasticsearch) |
| **Standing Service** | Go | Gin | Hitung dan serve klasemen liga |
| **Admin Service** | Node.js / Go | Express / Gin | CMS untuk operator manual input, monitoring dashboard |

> **Kenapa Go/Rust untuk WebSocket Gateway?**
> Go dan Rust bisa handle puluhan ribu concurrent connections per process dengan memory footprint sangat rendah. Node.js akan struggle di 50K+ concurrent WebSocket connections karena single-threaded event loop overhead.

> **Kenapa Custom WebSocket Server (bukan Socket.io)?**
> Socket.io menambahkan overhead protokol yang tidak diperlukan. Untuk skala 10M+ koneksi, custom WebSocket server berbasis `epoll` (Linux) atau `kqueue` (macOS) memberikan kontrol penuh atas memory, buffering, dan connection lifecycle.

### 5.6 Data Layer

| Komponen | Tool | Konfigurasi | Alasan |
|----------|------|-------------|--------|
| **In-Memory Store** | Redis Cluster (7.x) | 6 nodes (3 master + 3 replica) + Redis Pub/Sub | Hot data, real-time pub/sub, sub-millisecond read |
| **Message Broker** | Apache Kafka | 5+ brokers, replication factor 3 | High throughput event streaming, durable log |
| **Primary Database** | PostgreSQL 16 | Primary + 3 Read Replicas, multi-AZ | Historical data, standings, user data |
| **Time-Series DB** | TimescaleDB (ext PostgreSQL) | Hypertable partitioned by time | Match statistics over time, analytics |
| **Search Engine** | Elasticsearch | 3-node cluster | Full-text search untuk teams, players, matches |
| **Object Storage** | S3 / GCS | Multi-region replication | Team logos, player photos, static assets |

### 5.7 Real-Time Delivery

| Komponen | Tool | Alasan |
|----------|------|--------|
| **Primary Channel** | WebSocket (RFC 6455) | Full-duplex, lowest latency, native browser support |
| **Fallback Channel** | Server-Sent Events (SSE) | Simpler, works behind proxy, one-way sufficient for scores |
| **Last Resort** | HTTP Long Polling | Firewall-friendly, works everywhere |
| **Internal Pub/Sub** | Redis Pub/Sub + Kafka | Redis untuk real-time fan-out, Kafka untuk durability |
| **Mobile Push** | FCM (Android) + APNs (iOS) | Native OS-level push untuk user yang tidak buka app |

### 5.8 Monitoring & Observability

| Komponen | Tool | Fungsi |
|----------|------|--------|
| **Metrics** | Prometheus + Grafana | Dashboard real-time, alerting, custom metrics |
| **Logging** | ELK Stack / Loki | Centralized logging, query logs |
| **Tracing** | Jaeger / OpenTelemetry | Distributed tracing dari ingestion sampai delivery |
| **Alerting** | PagerDuty / OpsGenie | On-call rotation, incident management |
| **Uptime** | Pingdom / Checkly | External availability & latency monitoring |
| **Custom** | Score Accuracy Monitor | Bandingkan skor kita vs multiple sources |

### 5.9 Frontend

| Komponen | Tool | Alasan |
|----------|------|--------|
| **Web Framework** | React / Next.js | SSR, fast hydration, SEO-friendly |
| **State Management** | Zustand / TanStack Query | Lightweight, optimistic updates |
| **Real-time** | Native WebSocket API | No library overhead, custom reconnection logic |
| **Styling** | Tailwind CSS | Rapid UI development |
| **Mobile** | Flutter / React Native | Cross-platform, single codebase |
| **Desktop Widget** | Electron / PWA | Desktop score ticker widget |

---

## 6. Alur Kerja (Detailed Flow)

### 6.1 Data Ingestion Flow (Dari Provider ke Sistem)

```
Pertandingan dimulai di lapangan
          │
          ▼
┌─── [1] Sports Data Provider ────────────────────────┐
│                                                      │
│  Opta / SportRadar operator di stadion               │
│  └→ Observasi event langsung                         │
│  └→ Input ke sistem provider                         │
│  └→ Dikirim via:                                     │
│     • Push API (Webhook / gRPC stream)               │
│     • atau Polling API (REST, setiap 5-10 detik)     │
│                                                      │
│  Data format (contoh Opta):                          │
│  {                                                   │
│    "match_id": "m_2026_wc_final",                    │
│    "event_type": "GOAL",                             │
│    "minute": 73,                                     │
│    "player_id": "p_12345",                           │
│    "team": "home",                                   │
│    "score": {"home": 2, "away": 1},                  │
│    "timestamp": "2026-08-07T20:15:03Z"               │
│  }                                                   │
│                                                      │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌─── [2] Data Ingestion Service ──────────────────────┐
│                                                      │
│  Step 2a: Receive & Parse                            │
│  ┌──────────────────────────────────────────────┐   │
│  │ Terima data via webhook / gRPC stream         │   │
│  │ Parse ke internal format (normalized)         │   │
│  │ Setiap provider punya adapter sendiri         │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 2b: Validation & Deduplication                 │
│  ┌──────────────────────────────────────────────┐   │
│  │ • Cek apakah event ini duplikat               │   │
│  │   (hash: match_id + event_type + minute +     │   │
│  │    player_id)                                 │   │
│  │ • Validasi: skor tidak mundur, menit masuk    │   │
│  │   akal, player_id valid                       │   │
│  │ • Jika ada 2 provider, cross-check skor       │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 2c: Normalize ke Internal Format               │
│  ┌──────────────────────────────────────────────┐   │
│  │ Opta format → Internal MatchEvent schema      │   │
│  │ SportRadar format → Internal MatchEvent schema│   │
│  │                                               │   │
│  │ Internal Schema:                              │   │
│  │ {                                             │   │
│  │   "event_id": "evt_uuid",                    │   │
│  │   "match_id": "m_2026_wc_final",             │   │
│  │   "type": "GOAL",                            │   │
│  │   "minute": 73,                              │   │
│  │   "extra_time_minute": null,                  │   │
│  │   "player": {                                 │   │
│  │     "id": "p_12345",                          │   │
│  │     "name": "Player Name"                     │   │
│  │   },                                          │   │
│  │   "team_side": "HOME",                        │   │
│  │   "score": {"home": 2, "away": 1},            │   │
│  │   "source": "OPTA",                           │   │
│  │   "received_at": "2026-08-07T20:15:03.142Z"   │   │
│  │ }                                             │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 2d: Publish ke Kafka                           │
│  ┌──────────────────────────────────────────────┐   │
│  │ Topic: raw-match-events                       │   │
│  │ Key: match_id (partitioning by match)         │   │
│  │ Guarantees: at-least-once delivery            │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 6.2 Event Processing Flow

```
Kafka: raw-match-events
           │
           ▼
┌─── [3] Event Processing Service ────────────────────┐
│                                                      │
│  Step 3a: Consume & Deduplicate (lagi)               │
│  ┌──────────────────────────────────────────────┐   │
│  │ Idempotency check via event_id di Redis       │   │
│  │ SETNX processed_events:{event_id} 1 EX 3600  │   │
│  │ if already exists → skip                      │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 3b: Enrich Event Data                          │
│  ┌──────────────────────────────────────────────┐   │
│  │ • Tambahkan nama pemain lengkap, foto         │   │
│  │ • Tambahkan nama tim, logo URL                │   │
│  │ • Tambahkan info liga, round, matchday        │   │
│  │ • Hitung derived stats (xG, possession %, dll)│   │
│  │ • Data dari Redis cache (pre-loaded)          │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 3c: Update State di Redis                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Update live match data:                       │   │
│  │ HSET match:{match_id} score_home 2            │   │
│  │ HSET match:{match_id} score_away 1            │   │
│  │ HSET match:{match_id} minute 73               │   │
│  │ HSET match:{match_id} status "LIVE"           │   │
│  │                                               │   │
│  │ Append event ke timeline:                     │   │
│  │ RPUSH match:{match_id}:events {event_json}    │   │
│  │                                               │   │
│  │ Update stats:                                 │   │
│  │ HSET match:{match_id}:stats possession_home 58│   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 3d: Persist ke PostgreSQL (async)              │
│  ┌──────────────────────────────────────────────┐   │
│  │ INSERT INTO match_events (...)               │   │
│  │ UPDATE matches SET score_home=2, score_away=1│   │
│  │ (batched writes via Kafka consumer)           │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 3e: Fan-out ke Real-Time Channels              │
│  ┌──────────────────────────────────────────────┐   │
│  │ 1. Redis PUBLISH match:{match_id} {event}    │   │
│  │    → WebSocket Gateway servers subscribe      │   │
│  │                                               │   │
│  │ 2. Kafka topic: score-updates                 │   │
│  │    → Notification service consume             │   │
│  │                                               │   │
│  │ 3. Kafka topic: notification-events           │   │
│  │    → Push notification untuk GOAL events      │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 6.3 Real-Time Delivery Flow (Dari Sistem ke User)

```
Redis PUBLISH match:{match_id}
           │
           ▼
┌─── [4] WebSocket Gateway ───────────────────────────┐
│                                                      │
│  Step 4a: Receive Pub/Sub Message                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ Setiap WS Gateway server subscribe ke         │   │
│  │ channel match:{match_id} untuk semua match    │   │
│  │ yang user-nya sedang connected                │   │
│  │                                               │   │
│  │ "Smart Subscribe": hanya subscribe match      │   │
│  │ yang ada user interested di server ini         │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 4b: Fan-out ke Connected Users                 │
│  ┌──────────────────────────────────────────────┐   │
│  │ Untuk setiap user yang subscribe match ini:   │   │
│  │                                               │   │
│  │ 1. Serialize event ke compact format          │   │
│  │    (MessagePack / Protobuf, bukan JSON)       │   │
│  │                                               │   │
│  │ 2. Write ke user's WebSocket connection       │   │
│  │    ws.WriteMessage(event_bytes)               │   │
│  │                                               │   │
│  │ 3. Jika write gagal (connection broken):      │   │
│  │    └→ Mark connection as dead                 │   │
│  │    └→ Clean up resources                      │   │
│  │    └→ Remove from subscription                │   │
│  │                                               │   │
│  │ Batching Optimization:                        │   │
│  │ • Buffer events selama 100ms                  │   │
│  │ • Kirim sebagai batch (1 write per user)      │   │
│  │ • Reduce syscall overhead drastis             │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Step 4c: Connection Lifecycle                       │
│  ┌──────────────────────────────────────────────┐   │
│  │ • Heartbeat setiap 30 detik (ping/pong)       │   │
│  │ • Idle timeout: 5 menit tanpa subscribe       │   │
│  │ • Graceful reconnection support               │   │
│  │ • Client-side: auto-reconnect + eksponensial  │   │
│  │   backoff (1s → 2s → 4s → 8s → max 30s)      │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
           │
           ▼
┌─── [5] Client (Browser / Mobile App) ───────────────┐
│                                                      │
│  Receive WebSocket message                           │
│  ┌──────────────────────────────────────────────┐   │
│  │ 1. Deserialize event                          │   │
│  │ 2. Update local state (Redux/Zustand)         │   │
│  │ 3. Re-render UI:                              │   │
│  │    • Score update → animate score change      │   │
│  │    • Goal → show goal celebration animation   │   │
│  │    • Card → show card icon in timeline        │   │
│  │ 4. Play sound effect (jika goal)              │   │
│  │ 5. Update tab title: "⚽ Team A 2-1 Team B"  │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 6.4 Push Notification Flow

```
Kafka: notification-events
           │
           ▼
┌─── [6] Notification Service ───────────────────────┐
│                                                     │
│  Step 6a: Filter & Routing                          │
│  ┌─────────────────────────────────────────────┐   │
│  │ Hanya event PENTING yang trigger push:       │   │
│  │ • GOAL                                       │   │
│  │ • MATCH_START                                │   │
│  │ • MATCH_END (final score)                    │   │
│  │ • RED_CARD                                   │   │
│  │ • PENALTY_AWARDED                            │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Step 6b: Resolve Subscribers                       │
│  ┌─────────────────────────────────────────────┐   │
│  │ Query: SELECT user_id, fcm_token, apns_token│   │
│  │ FROM user_subscriptions                      │   │
│  │ WHERE team_id IN (home_team, away_team)      │   │
│  │ AND notification_enabled = true              │   │
│  │                                              │   │
│  │ → Bisa ratusan ribu sampai jutaan user       │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Step 6c: Send Push Notifications (Batched)         │
│  ┌─────────────────────────────────────────────┐   │
│  │ FCM: Batch 500 tokens per request            │   │
│  │ APNs: HTTP/2 multiplexed connections         │   │
│  │                                              │   │
│  │ Notification content:                        │   │
│  │ "⚽ GOAL! Argentina 2-1 France               │   │
│  │  73' — Lionel Messi                          │   │
│  │  Tap to see live match"                      │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 6.5 Match Lifecycle (State Machine)

```
┌──────────────────────────────────────────────────────────┐
│                   MATCH STATE MACHINE                     │
│                                                           │
│   ┌───────────┐                                          │
│   │ SCHEDULED │  (pertandingan terjadwal)                │
│   └─────┬─────┘                                          │
│         │ T = kickoff_time                               │
│         ▼                                                │
│   ┌───────────┐                                          │
│   │   LIVE    │  (pertandingan berlangsung)              │
│   │  1st Half │                                          │
│   └─────┬─────┘                                          │
│         │ minute = 45 + stoppage                         │
│         ▼                                                │
│   ┌───────────┐                                          │
│   │ HALF_TIME │  (istirahat)                             │
│   └─────┬─────┘                                          │
│         │ 2nd half start                                 │
│         ▼                                                │
│   ┌───────────┐                                          │
│   │   LIVE    │  (babak kedua)                           │
│   │  2nd Half │                                          │
│   └─────┬─────┘                                          │
│         │ minute = 90 + stoppage                         │
│         ▼                                                │
│   ┌───────────┐    ┌────────────┐    ┌──────────┐       │
│   │ FULL_TIME ├───→│EXTRA_TIME  ├───→│ PENALTIES │       │
│   └─────┬─────┘    │(jika seri  │    │(jika seri│       │
│         │          │ di knockout)│    │ di ET)   │       │
│         │          └────────────┘    └─────┬────┘       │
│         │                                  │             │
│         ▼                                  ▼             │
│   ┌───────────┐                                          │
│   │ FINISHED  │  (pertandingan selesai)                  │
│   └─────┬─────┘                                          │
│         │ T + 2 jam (data finalized)                     │
│         ▼                                                │
│   ┌───────────┐                                          │
│   │ ARCHIVED  │  (pindah ke cold storage)                │
│   └───────────┘                                          │
│                                                           │
│   Alternate States:                                       │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐           │
│   │ POSTPONED │  │ CANCELLED │  │ SUSPENDED │           │
│   └───────────┘  └───────────┘  └───────────┘           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 7. Real-Time Delivery Deep Dive

### 7.1 WebSocket vs SSE vs Long Polling

| Feature | WebSocket | SSE | Long Polling |
|---------|-----------|-----|-------------|
| **Direction** | Full-duplex | Server → Client only | Client → Server (repeated) |
| **Latency** | Ultra-low (~50ms) | Low (~100ms) | Medium (~1-5s) |
| **Browser Support** | 97%+ | 95%+ (no IE) | 100% |
| **Firewall Friendly** | ❌ Some block | ✅ Uses HTTP | ✅ Standard HTTP |
| **Connection Overhead** | Low (persistent) | Low (persistent) | High (reconnect each time) |
| **Scalability** | Moderate (stateful) | Good (lighter) | Best (stateless) |
| **Best For** | Live scores (primary) | Fallback | Last resort |

### 7.2 WebSocket Connection Management

```
┌──────────────────────────────────────────────────────────┐
│            WEBSOCKET CONNECTION LIFECYCLE                  │
│                                                           │
│  Client                              WS Gateway           │
│    │                                      │               │
│    │──── WS Handshake (Upgrade) ────────→│               │
│    │     GET /ws?token=jwt_xxx            │               │
│    │                                      │               │
│    │←─── 101 Switching Protocols ────────│               │
│    │                                      │               │
│    │──── Subscribe: {"matches":  ────────→│               │
│    │      ["m_123","m_456"]}              │               │
│    │                                      │               │
│    │     [Server subscribes to            │               │
│    │      Redis channels for              │               │
│    │      these matches]                  │               │
│    │                                      │               │
│    │←─── Score Update ───────────────────│               │
│    │     {"match":"m_123",                │               │
│    │      "score":{"h":2,"a":1},          │               │
│    │      "event":"GOAL","min":73}        │               │
│    │                                      │               │
│    │←─── Ping (every 30s) ──────────────│               │
│    │──── Pong ──────────────────────────→│               │
│    │                                      │               │
│    │──── Unsubscribe: {"matches": ──────→│               │
│    │      ["m_123"]}                      │               │
│    │                                      │               │
│    │     [If no user subscribes to        │               │
│    │      m_123 on this server,           │               │
│    │      unsubscribe from Redis]         │               │
│    │                                      │               │
│    │──── Close (or timeout) ────────────→│               │
│    │                                      │               │
└──────────────────────────────────────────────────────────┘
```

### 7.3 Fan-out Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FAN-OUT STRATEGY                            │
│                                                               │
│  ❌ NAIF APPROACH (tidak scalable):                           │
│  Event Processing → langsung kirim ke 10M users              │
│  Problem: bottleneck di satu titik                            │
│                                                               │
│  ✅ TIERED FAN-OUT (yang digunakan):                          │
│                                                               │
│  Level 1: Event Processing Service                            │
│  └→ PUBLISH ke 1 Redis channel per match                     │
│     (1 message)                                               │
│                                                               │
│  Level 2: Redis Pub/Sub                                       │
│  └→ Fan-out ke N WebSocket Gateway servers                   │
│     yang subscribe channel ini                                │
│     (N = ~50-200 servers, depends on popularity)              │
│                                                               │
│  Level 3: Each WebSocket Gateway                              │
│  └→ Fan-out ke ~50K connected users per server               │
│     yang subscribe match ini                                  │
│     (50K × N = total fan-out)                                 │
│                                                               │
│  Contoh Final Piala Dunia:                                    │
│  1 event → Redis → 200 WS servers → 50K users/server         │
│  = 10M users receive update                                  │
│  Total messages: 1 + 200 + 10M = ~10M                        │
│  Tapi setiap layer handle bagiannya sendiri!                  │
│                                                               │
│  ┌─────────────┐                                             │
│  │  Event      │ ─── 1 msg ───→  Redis Pub/Sub              │
│  │  Processing │                    │                         │
│  └─────────────┘                    │                         │
│                        ┌────────────┼────────────┐           │
│                        ▼            ▼            ▼           │
│                    ┌──────┐    ┌──────┐    ┌──────┐          │
│                    │WS GW │    │WS GW │    │WS GW │ ...     │
│                    │  #1  │    │  #2  │    │  #3  │          │
│                    │ 50K  │    │ 50K  │    │ 50K  │          │
│                    │users │    │users │    │users │          │
│                    └──────┘    └──────┘    └──────┘          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 7.4 Message Compression & Optimization

```
┌──────────────────────────────────────────────────────────┐
│             MESSAGE OPTIMIZATION STRATEGIES                │
│                                                           │
│  1. COMPACT PAYLOAD FORMAT                                │
│     Full JSON:  ~500 bytes                                │
│     MessagePack: ~200 bytes (60% reduction)               │
│     Custom binary: ~100 bytes (80% reduction)             │
│                                                           │
│  2. DELTA UPDATES (hanya kirim yang berubah)              │
│     Full state:  {"home":2,"away":1,"min":73,...}         │
│     Delta:       {"s":[2,1],"m":73,"e":"G"}              │
│                                                           │
│  3. BATCHING                                              │
│     Tanpa batching: 10 events → 10 WS writes             │
│     Dengan batching (100ms window):                       │
│     10 events → 1 WS write (array of events)             │
│     Reduce syscall 10× per connection                     │
│                                                           │
│  4. PER-WEBSOCKET COMPRESSION                             │
│     WebSocket permessage-deflate extension                │
│     Typical compression ratio: 60-80%                     │
│     Trade-off: CPU cost vs bandwidth saving               │
│     → Enable hanya untuk koneksi lambat                   │
│                                                           │
│  5. CLIENT-SIDE THROTTLING                                │
│     UI update max 1×/detik (requestAnimationFrame)        │
│     Buffer incoming events, batch render                  │
│     Prevent DOM thrashing                                 │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 8. Database Design

### 8.1 Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    sports    │       │     leagues       │       │   seasons    │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)          │       │ id (PK)      │
│ name         │───┐   │ sport_id (FK)    │───┐   │ league_id(FK)│
│ slug         │   │   │ name             │   │   │ name         │
│ icon_url     │   │   │ country          │   │   │ start_date   │
│ config_json  │   └──→│ logo_url         │   └──→│ end_date     │
└──────────────┘       │ tier             │       │ is_current   │
                       └──────────────────┘       └──────┬───────┘
                                                         │
                              ┌───────────────────────────┘
                              │
                              ▼
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    teams     │       │     matches      │       │   players    │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)          │       │ id (PK)      │
│ name         │◄──┐   │ season_id (FK)   │       │ name         │
│ short_name   │   │   │ home_team_id(FK) │──┐    │ team_id (FK) │
│ country      │   ├───│ away_team_id(FK) │──┘    │ position     │
│ logo_url     │   │   │ matchday         │       │ jersey_number│
│ venue        │   │   │ venue            │       │ nationality  │
│ founded_year │   │   │ kickoff_time     │       │ photo_url    │
└──────────────┘   │   │ status           │       └──────────────┘
                   │   │ minute           │               │
                   │   │ score_home       │               │
                   │   │ score_away       │               │
                   │   │ score_ht_home    │               │
                   │   │ score_ht_away    │               │
                   │   │ referee          │               │
                   │   │ attendance       │               │
                   │   │ updated_at       │               │
                   │   └──────────────────┘               │
                   │           │                          │
                   │    ┌──────┘                          │
                   │    │                                 │
                   │    ▼                                 │
                   │  ┌──────────────────┐               │
                   │  │  match_events    │               │
                   │  ├──────────────────┤               │
                   │  │ id (PK)          │               │
                   │  │ match_id (FK)    │               │
                   │  │ event_type       │  ◄────────────┘
                   │  │ minute           │
                   │  │ extra_time_min   │
                   │  │ player_id (FK)   │
                   │  │ secondary_player │
                   │  │   _id (FK)       │
                   │  │ team_id (FK)     │───┘
                   │  │ detail_json      │
                   │  │ created_at       │
                   │  └──────────────────┘
                   │
                   │  ┌──────────────────┐       ┌──────────────────┐
                   │  │  match_stats     │       │  standings       │
                   │  ├──────────────────┤       ├──────────────────┤
                   │  │ id (PK)          │       │ id (PK)          │
                   │  │ match_id (FK)    │       │ season_id (FK)   │
                   │  │ team_id (FK)  ───┘       │ team_id (FK)     │
                   │  │ possession       │       │ position         │
                   │  │ shots_total      │       │ played           │
                   │  │ shots_on_target  │       │ won              │
                   │  │ corners          │       │ drawn            │
                   │  │ fouls            │       │ lost             │
                   │  │ offsides         │       │ goals_for        │
                   │  │ passes_total     │       │ goals_against    │
                   │  │ passes_accurate  │       │ goal_difference  │
                   │  │ yellow_cards     │       │ points           │
                   │  │ red_cards        │       │ form (last 5)    │
                   │  │ updated_at       │       │ updated_at       │
                   │  └──────────────────┘       └──────────────────┘

┌──────────────────┐       ┌──────────────────┐
│    users         │       │ user_subscriptions│
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ email            │       │ user_id (FK)     │
│ username         │       │ team_id (FK)     │
│ password_hash    │       │ league_id (FK)   │
│ fcm_token        │       │ notify_goals     │
│ apns_token       │       │ notify_start     │
│ timezone         │       │ notify_end       │
│ language         │       │ notify_cards     │
│ created_at       │       │ created_at       │
└──────────────────┘       └──────────────────┘

┌──────────────────┐
│  commentaries    │
├──────────────────┤
│ id (PK)          │
│ match_id (FK)    │
│ minute           │
│ text             │
│ is_important     │
│ created_at       │
└──────────────────┘
```

### 8.2 Table Definitions

```sql
-- Sports
CREATE TABLE sports (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(100) NOT NULL UNIQUE,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    icon_url    TEXT,
    config_json JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Leagues
CREATE TABLE leagues (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sport_id    UUID NOT NULL REFERENCES sports(id),
    name        VARCHAR(255) NOT NULL,
    country     VARCHAR(100),
    logo_url    TEXT,
    tier        INTEGER DEFAULT 1,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_leagues_sport ON leagues(sport_id);
CREATE INDEX idx_leagues_country ON leagues(country);

-- Seasons
CREATE TABLE seasons (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    league_id   UUID NOT NULL REFERENCES leagues(id),
    name        VARCHAR(50) NOT NULL,   -- "2025/2026"
    start_date  DATE NOT NULL,
    end_date    DATE NOT NULL,
    is_current  BOOLEAN NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_seasons_league ON seasons(league_id);
CREATE UNIQUE INDEX idx_seasons_league_current ON seasons(league_id)
    WHERE is_current = true;

-- Teams
CREATE TABLE teams (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name         VARCHAR(255) NOT NULL,
    short_name   VARCHAR(10),
    country      VARCHAR(100),
    logo_url     TEXT,
    venue        VARCHAR(255),
    founded_year INTEGER,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_teams_name ON teams USING gin(name gin_trgm_ops);

-- Players
CREATE TABLE players (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name           VARCHAR(255) NOT NULL,
    team_id        UUID REFERENCES teams(id),
    position       VARCHAR(50),
    jersey_number  INTEGER,
    nationality    VARCHAR(100),
    date_of_birth  DATE,
    photo_url      TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_players_team ON players(team_id);
CREATE INDEX idx_players_name ON players USING gin(name gin_trgm_ops);

-- Matches (Tabel utama — paling sering diquery)
CREATE TABLE matches (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    season_id      UUID NOT NULL REFERENCES seasons(id),
    home_team_id   UUID NOT NULL REFERENCES teams(id),
    away_team_id   UUID NOT NULL REFERENCES teams(id),
    matchday       INTEGER,
    venue          VARCHAR(255),
    kickoff_time   TIMESTAMPTZ NOT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED'
                   CHECK (status IN ('SCHEDULED','LIVE','HALF_TIME',
                                     'LIVE_2H','EXTRA_TIME','PENALTIES',
                                     'FINISHED','POSTPONED',
                                     'CANCELLED','SUSPENDED')),
    minute         INTEGER DEFAULT 0,
    added_time     INTEGER DEFAULT 0,
    score_home     INTEGER DEFAULT 0,
    score_away     INTEGER DEFAULT 0,
    score_ht_home  INTEGER,
    score_ht_away  INTEGER,
    score_et_home  INTEGER,
    score_et_away  INTEGER,
    score_pen_home INTEGER,
    score_pen_away INTEGER,
    referee        VARCHAR(255),
    attendance     INTEGER,
    provider_id    VARCHAR(255),      -- ID di data provider
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_matches_kickoff ON matches(kickoff_time);
CREATE INDEX idx_matches_status ON matches(status);
CREATE INDEX idx_matches_season ON matches(season_id);
CREATE INDEX idx_matches_home_team ON matches(home_team_id);
CREATE INDEX idx_matches_away_team ON matches(away_team_id);
CREATE INDEX idx_matches_live ON matches(status) WHERE status IN ('LIVE','HALF_TIME','LIVE_2H','EXTRA_TIME','PENALTIES');
CREATE INDEX idx_matches_date ON matches(DATE(kickoff_time AT TIME ZONE 'UTC'));

-- Match Events (gol, kartu, substitusi, dll.)
CREATE TABLE match_events (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id            UUID NOT NULL REFERENCES matches(id),
    event_type          VARCHAR(30) NOT NULL
                        CHECK (event_type IN ('GOAL','OWN_GOAL','PENALTY_GOAL',
                                             'PENALTY_MISS','YELLOW_CARD',
                                             'RED_CARD','SECOND_YELLOW',
                                             'SUBSTITUTION','VAR_DECISION',
                                             'ASSIST','MATCH_START','HALF_TIME',
                                             'SECOND_HALF','EXTRA_TIME_START',
                                             'PENALTIES_START','MATCH_END')),
    minute              INTEGER NOT NULL,
    extra_time_minute   INTEGER,
    player_id           UUID REFERENCES players(id),
    secondary_player_id UUID REFERENCES players(id),   -- assist / player keluar
    team_id             UUID REFERENCES teams(id),
    detail_json         JSONB DEFAULT '{}',
    provider_event_id   VARCHAR(255),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_match_events_match ON match_events(match_id);
CREATE INDEX idx_match_events_type ON match_events(match_id, event_type);
CREATE INDEX idx_match_events_player ON match_events(player_id);

-- Match Statistics
CREATE TABLE match_stats (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id         UUID NOT NULL REFERENCES matches(id),
    team_id          UUID NOT NULL REFERENCES teams(id),
    possession       DECIMAL(5,2),
    shots_total      INTEGER DEFAULT 0,
    shots_on_target  INTEGER DEFAULT 0,
    corners          INTEGER DEFAULT 0,
    fouls            INTEGER DEFAULT 0,
    offsides         INTEGER DEFAULT 0,
    passes_total     INTEGER DEFAULT 0,
    passes_accurate  INTEGER DEFAULT 0,
    yellow_cards     INTEGER DEFAULT 0,
    red_cards        INTEGER DEFAULT 0,
    saves            INTEGER DEFAULT 0,
    tackles          INTEGER DEFAULT 0,
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_match_stats_match_team ON match_stats(match_id, team_id);

-- Standings
CREATE TABLE standings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    season_id       UUID NOT NULL REFERENCES seasons(id),
    team_id         UUID NOT NULL REFERENCES teams(id),
    position        INTEGER NOT NULL,
    played          INTEGER DEFAULT 0,
    won             INTEGER DEFAULT 0,
    drawn           INTEGER DEFAULT 0,
    lost            INTEGER DEFAULT 0,
    goals_for       INTEGER DEFAULT 0,
    goals_against   INTEGER DEFAULT 0,
    goal_difference INTEGER GENERATED ALWAYS AS (goals_for - goals_against) STORED,
    points          INTEGER DEFAULT 0,
    form            VARCHAR(10),    -- "WWDLW"
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_standings_season_team ON standings(season_id, team_id);
CREATE INDEX idx_standings_season_pos ON standings(season_id, position);

-- Commentaries
CREATE TABLE commentaries (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id     UUID NOT NULL REFERENCES matches(id),
    minute       INTEGER NOT NULL,
    text         TEXT NOT NULL,
    is_important BOOLEAN DEFAULT false,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_commentaries_match ON commentaries(match_id);

-- User Subscriptions (tim favorit & notifikasi)
CREATE TABLE user_subscriptions (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id        UUID NOT NULL REFERENCES users(id),
    team_id        UUID REFERENCES teams(id),
    league_id      UUID REFERENCES leagues(id),
    notify_goals   BOOLEAN DEFAULT true,
    notify_start   BOOLEAN DEFAULT true,
    notify_end     BOOLEAN DEFAULT true,
    notify_cards   BOOLEAN DEFAULT false,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_user_sub_user_team ON user_subscriptions(user_id, team_id)
    WHERE team_id IS NOT NULL;
CREATE UNIQUE INDEX idx_user_sub_user_league ON user_subscriptions(user_id, league_id)
    WHERE league_id IS NOT NULL;
CREATE INDEX idx_user_sub_team ON user_subscriptions(team_id);
```

### 8.3 Redis Data Structures

```
# ─── Live Match Data (Hot) ─────────────────────────
match:{match_id}                   → HASH {
                                       status: "LIVE",
                                       minute: 73,
                                       added_time: 2,
                                       score_home: 2,
                                       score_away: 1,
                                       home_team_id: "t_123",
                                       home_team_name: "Argentina",
                                       away_team_id: "t_456",
                                       away_team_name: "France",
                                       league_id: "l_789",
                                       updated_at: "2026-08-07T20:15:03Z"
                                     }

# ─── Match Events Timeline ────────────────────────
match:{match_id}:events            → LIST [event_json_1, event_json_2, ...]

# ─── Match Statistics ─────────────────────────────
match:{match_id}:stats:{team_id}   → HASH {
                                       possession: 58.3,
                                       shots_total: 12,
                                       shots_on_target: 5,
                                       corners: 6,
                                       fouls: 8,
                                       ...
                                     }

# ─── Live Commentary ──────────────────────────────
match:{match_id}:commentary        → LIST [commentary_json_1, ...]

# ─── Match Lineup ─────────────────────────────────
match:{match_id}:lineup:{team_id}  → LIST [player_json_1, ...]

# ─── Live Matches Index ──────────────────────────
live_matches                       → SET {match_id_1, match_id_2, ...}
live_matches:by_league:{league_id} → SET {match_id_1, match_id_2, ...}

# ─── Today's Matches ─────────────────────────────
matches:date:{YYYY-MM-DD}         → SORTED SET {match_id: kickoff_timestamp}

# ─── Standings Cache ─────────────────────────────
standings:{season_id}              → STRING (JSON, TTL 60s)

# ─── Deduplication ───────────────────────────────
processed_events:{event_hash}      → STRING ("1", TTL 3600)

# ─── Connection Tracking ─────────────────────────
ws:server:{server_id}:connections  → INTEGER (gauge)
ws:match:{match_id}:subscribers    → INTEGER (gauge, approximate)

# ─── API Response Cache ──────────────────────────
cache:api:matches:today            → STRING (JSON, TTL 10s)
cache:api:match:{match_id}         → STRING (JSON, TTL 5s for live, 300s for finished)
cache:api:standings:{season_id}    → STRING (JSON, TTL 60s)
```

---

## 9. API Design

### 9.1 REST API Endpoints

```
┌────────┬─────────────────────────────────────────┬────────────────────────────────┐
│ Method │ Endpoint                                │ Description                    │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│        │ MATCH ENDPOINTS                         │                                │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│ GET    │ /api/v1/matches/live                    │ Semua pertandingan live         │
│ GET    │ /api/v1/matches?date=2026-08-07         │ Pertandingan per tanggal       │
│ GET    │ /api/v1/matches/{id}                    │ Detail pertandingan            │
│ GET    │ /api/v1/matches/{id}/events             │ Timeline events (gol, kartu)   │
│ GET    │ /api/v1/matches/{id}/stats              │ Statistik pertandingan         │
│ GET    │ /api/v1/matches/{id}/lineup             │ Lineup kedua tim              │
│ GET    │ /api/v1/matches/{id}/commentary         │ Live commentary teks           │
│ GET    │ /api/v1/matches/{id}/head-to-head       │ H2H kedua tim                 │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│        │ LEAGUE & STANDING ENDPOINTS             │                                │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│ GET    │ /api/v1/leagues                         │ Daftar liga                    │
│ GET    │ /api/v1/leagues/{id}/matches            │ Pertandingan per liga          │
│ GET    │ /api/v1/leagues/{id}/standings           │ Klasemen liga                  │
│ GET    │ /api/v1/leagues/{id}/top-scorers        │ Daftar top skor               │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│        │ TEAM & PLAYER ENDPOINTS                 │                                │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│ GET    │ /api/v1/teams/{id}                      │ Detail tim                     │
│ GET    │ /api/v1/teams/{id}/matches              │ Pertandingan tim (past+future) │
│ GET    │ /api/v1/teams/{id}/squad                │ Daftar pemain                  │
│ GET    │ /api/v1/players/{id}                    │ Detail pemain                  │
│ GET    │ /api/v1/players/{id}/stats              │ Statistik pemain musim ini     │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│        │ USER ENDPOINTS                          │                                │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│ POST   │ /api/v1/auth/register                   │ Registrasi user               │
│ POST   │ /api/v1/auth/login                      │ Login user                     │
│ GET    │ /api/v1/users/me/subscriptions          │ Tim favorit saya              │
│ POST   │ /api/v1/users/me/subscriptions          │ Follow tim/liga               │
│ DELETE │ /api/v1/users/me/subscriptions/{id}     │ Unfollow tim/liga             │
│ PUT    │ /api/v1/users/me/notifications/settings │ Atur preferensi notifikasi    │
│ POST   │ /api/v1/users/me/devices                │ Register device token (FCM)   │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│        │ SEARCH ENDPOINT                         │                                │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│ GET    │ /api/v1/search?q=barcelona&type=team    │ Search tim, pemain, liga       │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│        │ WEBSOCKET ENDPOINT                      │                                │
├────────┼─────────────────────────────────────────┼────────────────────────────────┤
│ GET    │ /ws                                     │ WebSocket connection endpoint  │
└────────┴─────────────────────────────────────────┴────────────────────────────────┘
```

### 9.2 Key API Request/Response Examples

```json
// ─── GET /api/v1/matches/live ─────────────────────
// Semua pertandingan yang sedang berlangsung

{
  "status": "success",
  "data": {
    "count": 47,
    "matches": [
      {
        "id": "m_2026_wc_final",
        "league": {
          "id": "l_wc",
          "name": "FIFA World Cup 2026",
          "logo_url": "https://cdn.livescore.com/leagues/wc.svg"
        },
        "home_team": {
          "id": "t_arg",
          "name": "Argentina",
          "short_name": "ARG",
          "logo_url": "https://cdn.livescore.com/teams/arg.svg"
        },
        "away_team": {
          "id": "t_fra",
          "name": "France",
          "short_name": "FRA",
          "logo_url": "https://cdn.livescore.com/teams/fra.svg"
        },
        "status": "LIVE",
        "minute": 73,
        "added_time": 0,
        "score": {
          "home": 2,
          "away": 1,
          "half_time": {"home": 1, "away": 0}
        },
        "kickoff_time": "2026-08-07T19:00:00Z",
        "venue": "MetLife Stadium",
        "last_event": {
          "type": "GOAL",
          "minute": 73,
          "player": "Lionel Messi",
          "team_side": "HOME"
        }
      }
      // ... more matches
    ]
  },
  "meta": {
    "cached_at": "2026-08-07T20:15:03Z",
    "next_update": "2026-08-07T20:15:08Z"
  }
}
```

```json
// ─── GET /api/v1/matches/{id}/events ─────────────
// Timeline event pertandingan

{
  "status": "success",
  "data": {
    "match_id": "m_2026_wc_final",
    "events": [
      {
        "id": "evt_001",
        "type": "MATCH_START",
        "minute": 0,
        "detail": "Kick-off!"
      },
      {
        "id": "evt_002",
        "type": "GOAL",
        "minute": 23,
        "player": {
          "id": "p_12345",
          "name": "Lionel Messi",
          "photo_url": "https://cdn.livescore.com/players/messi.jpg"
        },
        "assist": {
          "id": "p_67890",
          "name": "Ángel Di María"
        },
        "team": {
          "id": "t_arg",
          "name": "Argentina",
          "side": "HOME"
        },
        "score_after": {"home": 1, "away": 0},
        "detail": "Left foot shot from the center of the box"
      },
      {
        "id": "evt_003",
        "type": "YELLOW_CARD",
        "minute": 34,
        "player": {
          "id": "p_22222",
          "name": "Aurélien Tchouaméni"
        },
        "team": {
          "id": "t_fra",
          "name": "France",
          "side": "AWAY"
        },
        "detail": "Foul on De Paul"
      },
      {
        "id": "evt_004",
        "type": "HALF_TIME",
        "minute": 45,
        "detail": "Half Time: Argentina 1-0 France"
      },
      {
        "id": "evt_005",
        "type": "SUBSTITUTION",
        "minute": 62,
        "player": {
          "id": "p_33333",
          "name": "Ousmane Dembélé"
        },
        "secondary_player": {
          "id": "p_44444",
          "name": "Marcus Thuram"
        },
        "team": {
          "id": "t_fra",
          "name": "France",
          "side": "AWAY"
        },
        "detail": "Dembélé replaces Thuram"
      },
      {
        "id": "evt_006",
        "type": "GOAL",
        "minute": 73,
        "player": {
          "id": "p_12345",
          "name": "Lionel Messi"
        },
        "team": {
          "id": "t_arg",
          "name": "Argentina",
          "side": "HOME"
        },
        "score_after": {"home": 2, "away": 1},
        "detail": "Brilliant solo run, right foot shot to the bottom corner"
      }
    ]
  }
}
```

### 9.3 WebSocket Protocol

```json
// ─── Client → Server Messages ─────────────────────

// Subscribe ke pertandingan tertentu
{
  "action": "subscribe",
  "matches": ["m_2026_wc_final", "m_epl_123"]
}

// Unsubscribe
{
  "action": "unsubscribe",
  "matches": ["m_epl_123"]
}

// Subscribe ke semua pertandingan liga tertentu
{
  "action": "subscribe_league",
  "league_id": "l_epl"
}

// Pong response (heartbeat)
{
  "action": "pong"
}


// ─── Server → Client Messages ─────────────────────

// Score update
{
  "type": "SCORE_UPDATE",
  "match_id": "m_2026_wc_final",
  "data": {
    "score": {"home": 2, "away": 1},
    "minute": 73,
    "event": {
      "type": "GOAL",
      "player": "Lionel Messi",
      "team_side": "HOME"
    }
  },
  "timestamp": "2026-08-07T20:15:03Z"
}

// Status change (half time, full time, dll.)
{
  "type": "STATUS_CHANGE",
  "match_id": "m_2026_wc_final",
  "data": {
    "old_status": "LIVE",
    "new_status": "HALF_TIME",
    "minute": 45,
    "score": {"home": 1, "away": 0}
  },
  "timestamp": "2026-08-07T19:47:00Z"
}

// Statistics update (setiap 30 detik)
{
  "type": "STATS_UPDATE",
  "match_id": "m_2026_wc_final",
  "data": {
    "home": {
      "possession": 58.3,
      "shots": 12,
      "shots_on_target": 5,
      "corners": 6
    },
    "away": {
      "possession": 41.7,
      "shots": 8,
      "shots_on_target": 3,
      "corners": 3
    }
  },
  "timestamp": "2026-08-07T20:15:30Z"
}

// Match event (kartu, substitusi, dll.)
{
  "type": "MATCH_EVENT",
  "match_id": "m_2026_wc_final",
  "data": {
    "event_type": "YELLOW_CARD",
    "minute": 34,
    "player": "Aurélien Tchouaméni",
    "team_side": "AWAY"
  },
  "timestamp": "2026-08-07T19:34:15Z"
}

// Commentary
{
  "type": "COMMENTARY",
  "match_id": "m_2026_wc_final",
  "data": {
    "minute": 73,
    "text": "GOOOAL! Messi with a magnificent solo run...",
    "is_important": true
  },
  "timestamp": "2026-08-07T20:15:05Z"
}

// Ping (heartbeat from server)
{
  "type": "PING",
  "timestamp": "2026-08-07T20:15:30Z"
}

// Error
{
  "type": "ERROR",
  "data": {
    "code": "INVALID_MATCH",
    "message": "Match m_invalid not found"
  }
}
```

---

## 10. Caching Strategy

### 10.1 Multi-Layer Cache Architecture

```
┌──────────────────────────────────────────────────────────┐
│                CACHING LAYERS                             │
│                                                           │
│  Layer 1: CDN Edge Cache (CloudFlare)                     │
│  ├── Static assets: 24 jam                                │
│  ├── API: /matches/live → Cache-Control: max-age=5        │
│  ├── API: /matches/{id} (live) → max-age=3, stale-while- │
│  │   revalidate=2                                         │
│  ├── API: /matches/{id} (finished) → max-age=300          │
│  ├── API: /standings → max-age=60                         │
│  └── Purge API: purge cache saat ada update penting       │
│                                                           │
│  Layer 2: API Gateway Cache (Kong)                        │
│  ├── Response caching per endpoint                        │
│  ├── TTL varies by data freshness needs                   │
│  └── Cache key: endpoint + query params + ETag            │
│                                                           │
│  Layer 3: Application Cache (Redis)                       │
│  ├── Live match data → no TTL (diupdate real-time)        │
│  ├── Match detail → TTL 5s (live), 300s (finished)        │
│  ├── Standings → TTL 60s                                  │
│  ├── Team/Player data → TTL 3600s (1 jam)                 │
│  └── Search results → TTL 300s                            │
│                                                           │
│  Layer 4: Database Query Cache (PostgreSQL)               │
│  ├── Prepared statements                                  │
│  ├── Connection pooling (PgBouncer)                       │
│  └── Materialized views for standings                     │
│                                                           │
│  Layer 5: Client-Side Cache (Browser/App)                 │
│  ├── HTTP cache headers (ETag, Last-Modified)             │
│  ├── Service Worker cache for offline support             │
│  └── In-memory state (WebSocket updates override cache)   │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 10.2 Cache Invalidation Strategy

```
┌──────────────────────────────────────────────────────────┐
│            CACHE INVALIDATION FLOWS                       │
│                                                           │
│  Skenario 1: Score Update (GOAL)                          │
│  ┌────────────────────────────────────────────────┐      │
│  │ 1. Event Processing updates Redis (instant)    │      │
│  │ 2. Invalidate CDN cache:                       │      │
│  │    • /api/v1/matches/live                      │      │
│  │    • /api/v1/matches/{match_id}                │      │
│  │    • /api/v1/matches/{match_id}/events         │      │
│  │ 3. WebSocket broadcast (real-time, bypass CDN) │      │
│  │ 4. API requests setelah CDN purge → fresh data │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
│  Skenario 2: Match Selesai (FINISHED)                     │
│  ┌────────────────────────────────────────────────┐      │
│  │ 1. Update Redis: status=FINISHED               │      │
│  │ 2. Remove dari live_matches set                 │      │
│  │ 3. Invalidate standings cache                   │      │
│  │ 4. Set longer TTL for match cache (300s)        │      │
│  │ 5. Trigger standings recalculation              │      │
│  │ 6. 2 jam kemudian: archive match data,          │      │
│  │    clear Redis hot data                         │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
│  Skenario 3: Static Data Update (Tim pindah pemain, dll.)│
│  ┌────────────────────────────────────────────────┐      │
│  │ 1. Admin update via CMS                        │      │
│  │ 2. Update DB                                   │      │
│  │ 3. Invalidate Redis cache for affected entity   │      │
│  │ 4. CDN purge for affected endpoints             │      │
│  │ 5. TTL-based expiry for any stragglers          │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 10.3 Cache TTL by Data Type

| Data Type | Redis TTL | CDN TTL | Rationale |
|-----------|-----------|---------|-----------|
| **Live Match Score** | No TTL (real-time update) | 3-5s | Harus fresh, tapi CDN melindungi origin |
| **Live Match Stats** | No TTL (real-time update) | 10s | Stats update tiap 30 detik |
| **Live Match Events** | No TTL | 5s | Event timeline harus up-to-date |
| **Finished Match** | 300s | 300s | Data tidak berubah, cache lebih lama |
| **Standings** | 60s | 60s | Update hanya saat match selesai |
| **Team Data** | 3600s | 3600s | Jarang berubah |
| **Player Data** | 3600s | 3600s | Jarang berubah |
| **Search Results** | 300s | 60s | Moderate freshness |
| **Historical Data** | 86400s (24h) | 86400s | Tidak pernah berubah |

---

## 11. Data Ingestion & Provider Management

### 11.1 Provider Adapter Pattern

```
┌──────────────────────────────────────────────────────────┐
│             ADAPTER PATTERN FOR DATA PROVIDERS            │
│                                                           │
│  interface DataProviderAdapter {                          │
│    Name() string                                          │
│    Connect() error                                        │
│    Subscribe(matchIDs []string) error                     │
│    OnEvent(callback func(NormalizedEvent))                │
│    HealthCheck() bool                                     │
│  }                                                        │
│                                                           │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │  OptaAdapter    │  │ SportRadarAdpt  │               │
│  │                 │  │                 │               │
│  │ • gRPC stream   │  │ • REST polling  │               │
│  │ • Push-based    │  │ • 5s interval   │               │
│  │ • Opta format   │  │ • SR format     │               │
│  │   → normalize   │  │   → normalize   │               │
│  └────────┬────────┘  └────────┬────────┘               │
│           │                    │                          │
│           ▼                    ▼                          │
│  ┌─────────────────────────────────────────┐             │
│  │        Unified Ingestion Pipeline       │             │
│  │                                         │             │
│  │  1. Receive normalized event            │             │
│  │  2. Deduplicate (hash-based)            │             │
│  │  3. Validate (skor masuk akal?)         │             │
│  │  4. Cross-reference (jika 2 source)     │             │
│  │  5. Publish ke Kafka                    │             │
│  └─────────────────────────────────────────┘             │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 11.2 Provider Failover Strategy

```
┌──────────────────────────────────────────────────────────┐
│              PROVIDER FAILOVER LOGIC                      │
│                                                           │
│  Priority:                                                │
│  1. Opta (Primary) — push-based, lowest latency           │
│  2. SportRadar (Secondary) — polling, slightly delayed    │
│  3. Manual Input (Fallback) — operator di CMS             │
│                                                           │
│  Failover triggers:                                       │
│  ┌────────────────────────────────────────────────┐      │
│  │ • No data received for 30 detik (live match)   │      │
│  │   → Switch ke secondary provider               │      │
│  │                                                │      │
│  │ • Health check failed 3× berturut-turut        │      │
│  │   → Mark provider as DOWN                      │      │
│  │   → Alert ops team                             │      │
│  │                                                │      │
│  │ • Data inconsistency detected                  │      │
│  │   (provider A: 2-1, provider B: 1-1)           │      │
│  │   → Flag for manual review                     │      │
│  │   → Use provider with lower latency as truth   │      │
│  │   → Alert on-call + show warning in admin      │      │
│  │                                                │      │
│  │ • All automated providers down                 │      │
│  │   → Enable manual input mode                   │      │
│  │   → Alert: "CRITICAL: Manual mode active"      │      │
│  │   → Operator input via admin dashboard         │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
│  Recovery:                                                │
│  ┌────────────────────────────────────────────────┐      │
│  │ • When primary recovers:                       │      │
│  │   → Don't switch immediately                   │      │
│  │   → Verify data consistency for 60 detik       │      │
│  │   → Then gradually switch back                 │      │
│  │   → Keep secondary as hot standby              │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 11.3 Data Validation Rules

```
┌──────────────────────────────────────────────────────────┐
│              DATA VALIDATION RULES                        │
│                                                           │
│  Rule 1: Score Monotonicity                               │
│  └→ Skor tidak boleh turun (kecuali event VAR cancel)     │
│  └→ home_score + away_score >= previous total             │
│                                                           │
│  Rule 2: Minute Progression                               │
│  └→ Minute harus naik (allow same minute, different event)│
│  └→ Half 1: 0-45+, Half 2: 45-90+, ET: 90-120+          │
│                                                           │
│  Rule 3: Player Validation                                │
│  └→ Player harus exist di squad database                  │
│  └→ Player harus dari tim yang benar                      │
│                                                           │
│  Rule 4: Event Type Constraints                           │
│  └→ GOAL harus memiliki player_id                         │
│  └→ SUBSTITUTION harus memiliki 2 player IDs              │
│  └→ Tidak boleh 2× kickoff event per match                │
│                                                           │
│  Rule 5: Rate Limiting per Match                          │
│  └→ Max 5 events per menit per match (sanity check)       │
│  └→ Jika lebih → flag as suspicious, alert ops            │
│                                                           │
│  Rule 6: Score vs Event Consistency                       │
│  └→ Jumlah GOAL events harus == total skor                │
│  └→ Jika mismatch → alert + manual reconciliation         │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 12. Failure Handling & Consistency

### 12.1 Failure Scenarios & Mitigations

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| **Data Provider down** | Tidak ada update skor | Auto-failover ke secondary provider, lalu manual input |
| **Kafka down** | Events tidak bisa diproses | Write-Ahead Log (WAL) di ingestion service, replay setelah recovery |
| **Redis down** | Live data tidak tersedia, WebSocket buta | Circuit breaker, serve dari DB (degraded mode, higher latency) |
| **PostgreSQL down** | Historical data tidak tersedia | Redis masih serve live data, DB writes queued di Kafka |
| **WebSocket Gateway crash** | Users kehilangan connection | Client auto-reconnect, LB route ke server lain |
| **Network partition** | Split brain antar services | Prefer AP (availability), serve potentially stale data + flag |
| **CDN outage** | High load ke origin | Multi-CDN strategy (CloudFlare + CloudFront), DNS failover |
| **Duplicate events** | Data duplikat ke user | Idempotency via event hash, client-side dedup |
| **Skor salah dari provider** | User lihat skor salah | Cross-validate multiple sources, admin override capability |

### 12.2 Consistency Model

```
┌──────────────────────────────────────────────────────────┐
│                CONSISTENCY STRATEGY                       │
│                                                           │
│  Model: EVENTUAL CONSISTENCY dengan prioritas FRESHNESS   │
│                                                           │
│  Source of Truth:                                          │
│  • Selama pertandingan live → REDIS (hot data)            │
│  • Setelah pertandingan selesai → POSTGRESQL (cold data)  │
│                                                           │
│  ┌─────────────────────────────────────────────────┐     │
│  │              Data Flow Timeline                  │     │
│  │                                                  │     │
│  │  T=0.0s    Event terjadi di lapangan             │     │
│  │  T=1.0s    Data provider kirim ke sistem         │     │
│  │  T=1.1s    Ingestion service normalize + validate│     │
│  │  T=1.2s    Kafka produce (raw-match-events)      │     │
│  │  T=1.4s    Event Processing consume + enrich     │     │
│  │  T=1.5s    Redis HSET (state updated)            │     │
│  │  T=1.5s    Redis PUBLISH (broadcast)             │     │
│  │  T=1.6s    WebSocket Gateway receive pub/sub     │     │
│  │  T=1.7s    Fan-out ke connected users            │     │
│  │  T=1.8s    User melihat update di layar ✅       │     │
│  │                                                  │     │
│  │  T=2.0s    Kafka consumer persist ke PostgreSQL   │     │
│  │            (async, eventual consistency)          │     │
│  │                                                  │     │
│  │  ⏱️  End-to-end latency: ~1.5 - 2 detik         │     │
│  │  ⚠️  Redis ↔ PostgreSQL gap: ~0.5 - 1 detik     │     │
│  └─────────────────────────────────────────────────┘     │
│                                                           │
│  Kenapa ini acceptable?                                   │
│  • User tidak pernah langsung query DB untuk live data     │
│  • Redis selalu serve the freshest data                   │
│  • DB hanya untuk historical, analytics, dan recovery     │
│  • Jika Redis crash, DB data max ~1 detik stale           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 12.3 WebSocket Reconnection & State Sync

```
┌──────────────────────────────────────────────────────────┐
│          RECONNECTION & STATE SYNC STRATEGY               │
│                                                           │
│  Problem: User disconnects, reconnects 30 detik kemudian  │
│  → Missed 3 events (gol + kartu + substitusi)             │
│                                                           │
│  Solution: "Catch-up" Protocol                             │
│  ┌────────────────────────────────────────────────┐      │
│  │                                                │      │
│  │  1. Client menyimpan last_event_id locally     │      │
│  │                                                │      │
│  │  2. Saat reconnect, kirim:                     │      │
│  │     { "action": "subscribe",                   │      │
│  │       "matches": ["m_123"],                    │      │
│  │       "since_event_id": "evt_005" }            │      │
│  │                                                │      │
│  │  3. Server mengirim missed events:             │      │
│  │     { "type": "CATCH_UP",                      │      │
│  │       "events": [evt_006, evt_007, evt_008] }  │      │
│  │                                                │      │
│  │  4. Lalu lanjut streaming real-time             │      │
│  │                                                │      │
│  │  Alternative (simpler): client fetch full match │      │
│  │  state via REST API, lalu subscribe WS         │      │
│  │                                                │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
│  Client-Side Reconnection Logic:                          │
│  ┌────────────────────────────────────────────────┐      │
│  │                                                │      │
│  │  attempt = 0                                   │      │
│  │  while (not connected):                        │      │
│  │    delay = min(2^attempt × 1000, 30000) // ms  │      │
│  │    delay += random(0, 1000) // jitter          │      │
│  │    wait(delay)                                 │      │
│  │    try connect()                               │      │
│  │    attempt++                                   │      │
│  │                                                │      │
│  │  Backoff: 1s → 2s → 4s → 8s → 16s → 30s (max)│      │
│  │  Jitter: prevent thundering herd reconnection  │      │
│  │                                                │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 13. Monitoring & Observability

### 13.1 Key Metrics Dashboard (Grafana)

```
┌──────────────────────────────────────────────────────────┐
│                  LIVE SCORE DASHBOARD                      │
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Live Matches │  │ WS Conns    │  │ Event Lag   │     │
│  │     47       │  │  8.2M       │  │   1.3s      │     │
│  │  ✅ Normal   │  │  ▲ 5%/min   │  │  ✅ < 2s    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ API RPS     │  │ Error Rate  │  │ p99 Latency │     │
│  │   342,501   │  │   0.02%     │  │    23ms     │     │
│  │  ▲ 8%/sec   │  │  ✅ < 1%    │  │  ✅ < 100ms │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  WebSocket Connections Over Time                  │   │
│  │  10M ┤                          ╭──────           │   │
│  │      │                    ╭────╯                   │   │
│  │   5M ┤              ╭───╯                         │   │
│  │      │         ╭───╯                              │   │
│  │   0  ┤─────────╯                                  │   │
│  │      └───────────────────────────────────────→    │   │
│  │      18:00  18:30  19:00  19:30  20:00  20:30    │   │
│  │      (matches kick off gradually)                 │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Event Processing Latency (end-to-end)            │   │
│  │                                                   │   │
│  │  Provider → Ingestion     : avg 200ms             │   │
│  │  Ingestion → Kafka        : avg 50ms              │   │
│  │  Kafka → Event Processing : avg 100ms             │   │
│  │  Processing → Redis       : avg 5ms               │   │
│  │  Redis → WS Gateway       : avg 10ms              │   │
│  │  WS Gateway → User        : avg 50ms              │   │
│  │  ─────────────────────────────────                │   │
│  │  TOTAL                    : avg 415ms (~0.4s)     │   │
│  │  TOTAL (with provider)    : avg 1.4s              │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 13.2 Alert Rules

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Provider Data Gap | No events for live match > 30s | 🔴 P1 | Auto-failover + page on-call |
| High Event Latency | end-to-end > 5s for 1 min | 🔴 P1 | Investigate pipeline bottleneck |
| WS Connection Drop | connections drop > 10% in 1 min | 🔴 P1 | Check WS servers, LB, network |
| High Error Rate | API error_rate > 2% for 2 min | 🟡 P2 | Investigate, check dependencies |
| Redis Memory | memory_used > 80% | 🟡 P2 | Scale Redis, check for leaks |
| Kafka Consumer Lag | consumer_lag > 5000 | 🟡 P2 | Scale consumers |
| Score Mismatch | 2 providers disagree on score | 🔴 P1 | Alert ops, manual review |
| DB Replication Lag | replica_lag > 10s | 🟡 P2 | Investigate DB health |
| CDN Hit Ratio | cache_hit_ratio < 80% | 🟡 P3 | Review cache headers |
| WS Server CPU | cpu > 80% for 5 min | 🟡 P2 | Scale up WS servers |

### 13.3 Score Accuracy Monitoring (Khusus Live Score)

```
┌──────────────────────────────────────────────────────────┐
│           SCORE ACCURACY MONITOR                          │
│                                                           │
│  Unique challenge untuk live score: SKOR HARUS BENAR.     │
│  Menampilkan skor salah = bencana (terutama untuk         │
│  gambling platforms yang consume API kita).                │
│                                                           │
│  ┌────────────────────────────────────────────────┐      │
│  │  Automated Cross-Validation Pipeline:          │      │
│  │                                                │      │
│  │  1. Setiap 60 detik, untuk semua live matches: │      │
│  │     a. Ambil skor dari Redis (our data)        │      │
│  │     b. Ambil skor dari Provider A (Opta)       │      │
│  │     c. Ambil skor dari Provider B (SportRadar) │      │
│  │                                                │      │
│  │  2. Compare semua tiga:                        │      │
│  │     if (redis == provA == provB):              │      │
│  │       ✅ All good                              │      │
│  │     elif (redis == provA != provB):            │      │
│  │       ⚠️ Log discrepancy, likely provB delay   │      │
│  │     elif (redis != provA && redis != provB):   │      │
│  │       🔴 CRITICAL: Our data might be wrong!    │      │
│  │       → Alert on-call                          │      │
│  │       → Auto-correct to provider consensus     │      │
│  │                                                │      │
│  │  3. Metrics:                                   │      │
│  │     • score_accuracy_percentage (target: 100%) │      │
│  │     • score_discrepancy_count                  │      │
│  │     • time_to_detect_discrepancy               │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 13.4 Distributed Tracing

```
Trace: goal_event_processing_abc123
├── [Ingestion] Receive webhook from Opta ────────── 5ms
├── [Ingestion] Parse + Normalize ────────────────── 2ms
├── [Ingestion] Validate + Dedup ─────────────────── 3ms
├── [Ingestion] Kafka Produce (raw-match-events) ─── 8ms
│   ├── [EventProc] Kafka Consume ────────────────── 12ms
│   ├── [EventProc] Dedup Check (Redis) ──────────── 0.5ms
│   ├── [EventProc] Enrich Event ─────────────────── 2ms
│   ├── [EventProc] Update Redis State ───────────── 1ms
│   ├── [EventProc] Redis PUBLISH ────────────────── 0.5ms
│   │   └── [WS Gateway] Receive Pub/Sub ─────────── 3ms
│   │       └── [WS Gateway] Fan-out to 125K users ─ 45ms
│   ├── [EventProc] Kafka Produce (score-updates) ── 5ms
│   │   └── [NotifSvc] Send Push (FCM batch) ─────── 200ms
│   └── [EventProc] Kafka Produce (processed) ────── 5ms
│       └── [DBWriter] INSERT match_events ────────── 8ms
│       └── [DBWriter] UPDATE matches ─────────────── 5ms
└── Total: User receives update in ~95ms after Kafka consume
    End-to-end from event to user screen: ~1.4s
```

---

## 14. Scaling Strategy

### 14.1 Component Scaling Profiles

```
┌──────────────────────────────────────────────────────────┐
│              SCALING STRATEGY PER COMPONENT               │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Data Ingestion Service                           │   │
│  │  Scale Factor: RENDAH (hanya beberapa instance)   │   │
│  │  Reason: Terbatas oleh jumlah data providers      │   │
│  │  Config: 3-5 pods (one per provider + redundancy) │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Event Processing Service                         │   │
│  │  Scale Factor: SEDANG                              │   │
│  │  Reason: Kafka consumer, scale by partition count  │   │
│  │  Config: 10-50 pods (1 pod per Kafka partition)   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  WebSocket Gateway ⭐ (BOTTLENECK UTAMA)         │   │
│  │  Scale Factor: TINGGI                              │   │
│  │  Reason: 1 server = ~50K connections              │   │
│  │  Config: 50-200 pods (untuk 2.5M-10M connections) │   │
│  │  Memory: ~1-2 GB per 50K connections              │   │
│  │  CPU: Mostly I/O bound, moderate CPU              │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  REST API Service (Match Service)                 │   │
│  │  Scale Factor: TINGGI                              │   │
│  │  Reason: High read RPS dari polling clients        │   │
│  │  Config: 20-100 pods, scale by RPS metric         │   │
│  │  CDN offloads 85% → effective origin load rendah   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Notification Service                             │   │
│  │  Scale Factor: SEDANG-TINGGI                       │   │
│  │  Reason: Burst saat GOAL event (batch push notif)  │   │
│  │  Config: 5-30 pods, scale by notification queue    │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 14.2 Kubernetes HPA Configuration

```yaml
# WebSocket Gateway HPA (komponen paling kritis)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ws-gateway-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ws-gateway
  minReplicas: 20
  maxReplicas: 300
  metrics:
    - type: Pods
      pods:
        metric:
          name: ws_active_connections
        target:
          type: AverageValue
          averageValue: "40000"   # Scale up sebelum 50K limit
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
        - type: Pods
          value: 20              # Agresif scale up
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 600   # Lambat scale down (10 min)
      policies:
        - type: Pods
          value: 5
          periodSeconds: 120
```

### 14.3 Event-Based Pre-Scaling

```
┌──────────────────────────────────────────────────────────┐
│           PRE-SCALING FOR BIG EVENTS                      │
│                                                           │
│  Contoh: Final Piala Dunia (expected 50M viewers)         │
│                                                           │
│  T-24h   │ Manual pre-scale:                              │
│          │ • WS Gateway: 20 → 200 pods                    │
│          │ • Match API: 20 → 100 pods                     │
│          │ • Redis: scale up memory tier                   │
│          │ • Multi-CDN activation                          │
│          │                                                 │
│  T-6h    │ Load testing against production replica         │
│          │ • Simulate 10M WebSocket connections            │
│          │ • Verify all services healthy                   │
│          │                                                 │
│  T-2h    │ Warm up:                                        │
│          │ • Pre-load match data ke Redis                  │
│          │ • CDN cache warming (match page)                │
│          │ • DB connection pool pre-warming                │
│          │                                                 │
│  T-30min │ Monitor ramp-up:                                │
│          │ • Users mulai connect WebSocket                 │
│          │ • Watch connection count, CPU, memory           │
│          │ • HPA fine-tuning jika perlu                    │
│          │                                                 │
│  T-0     │ Match starts                                    │
│          │ • Full monitoring mode                          │
│          │ • War room active (on-call engineers standby)   │
│          │                                                 │
│  T+3h    │ Match ends + buffer                             │
│          │ • Begin gradual scale-down                      │
│          │ • WS Gateway: 200 → 50 → 20 pods (over 2 hrs) │
│          │                                                 │
└──────────────────────────────────────────────────────────┘
```

### 14.4 Multi-Region Deployment

```
┌──────────────────────────────────────────────────────────┐
│            MULTI-REGION ARCHITECTURE                      │
│                                                           │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐     │
│  │  Region:   │    │  Region:   │    │  Region:   │     │
│  │  us-east-1 │    │  eu-west-1 │    │  ap-south-1│     │
│  │  (Americas)│    │  (Europe)  │    │  (Asia)    │     │
│  ├────────────┤    ├────────────┤    ├────────────┤     │
│  │ WS Gateway │    │ WS Gateway │    │ WS Gateway │     │
│  │ Match API  │    │ Match API  │    │ Match API  │     │
│  │ Redis ★    │    │ Redis ★    │    │ Redis ★    │     │
│  │ (replica)  │    │ (replica)  │    │ (replica)  │     │
│  └──────┬─────┘    └──────┬─────┘    └──────┬─────┘     │
│         │                 │                  │            │
│         └────────────┬────┘──────────────────┘            │
│                      │                                    │
│                      ▼                                    │
│              ┌──────────────┐                             │
│              │ Central      │                             │
│              │ Kafka +      │                             │
│              │ PostgreSQL   │                             │
│              │ (us-east-1)  │                             │
│              └──────────────┘                             │
│                                                           │
│  ★ Redis di setiap region = replica dari central,          │
│    atau menggunakan Redis Global Datastore (AWS)          │
│                                                           │
│  Data flow:                                               │
│  • Write: Ingestion → Central Kafka → Central DB          │
│  • Read:  User → Nearest Region → Local Redis →           │
│           Local WS Gateway                                │
│  • Replication: Central Redis → Regional Redis (async)    │
│  • Latency benefit: 200ms → 30ms (user di Asia)           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 15. Security Considerations

### 15.1 Security Layers

| Layer | Measure | Detail |
|-------|---------|--------|
| **Network** | VPC + Private Subnets | Internal services tidak exposed ke internet |
| **Transport** | TLS 1.3 everywhere | Termasuk WebSocket (WSS), API, dan inter-service |
| **CDN/WAF** | CloudFlare WAF | DDoS protection, bot mitigation, IP rate limiting |
| **Auth (Users)** | JWT + Refresh Token | Short-lived access token (30 min), refresh token (7 days) |
| **Auth (API Partners)** | API Key + HMAC | API key untuk identifikasi, HMAC untuk request signing |
| **Data** | Encryption at rest | AES-256 untuk user data (PII) |
| **Provider Auth** | mTLS / API Key | Secure connection ke data providers |
| **Rate Limiting** | Multi-layer | CDN → API Gateway → Application level |
| **Audit** | Immutable audit log | Semua admin actions dan data corrections di-log |

### 15.2 API Rate Limiting

```
┌──────────────────────────────────────────────────────────┐
│              API RATE LIMITING TIERS                       │
│                                                           │
│  Free Users (Anonymous):                                  │
│  ├── 60 requests/minute per IP                            │
│  ├── WebSocket: 5 match subscriptions max                 │
│  └── No push notifications                                │
│                                                           │
│  Registered Users:                                        │
│  ├── 300 requests/minute per user                         │
│  ├── WebSocket: 20 match subscriptions max                │
│  └── Push notifications enabled                            │
│                                                           │
│  API Partners (B2B):                                      │
│  ├── 1000 requests/minute per API key                     │
│  ├── WebSocket: unlimited subscriptions                    │
│  ├── Dedicated rate limit                                  │
│  └── SLA agreement                                        │
│                                                           │
│  Internal Services:                                       │
│  ├── No rate limiting (trusted network)                    │
│  └── mTLS authentication                                  │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 15.3 WebSocket Security

```
┌──────────────────────────────────────────────────────────┐
│              WEBSOCKET SECURITY MEASURES                   │
│                                                           │
│  1. Authentication:                                       │
│     • JWT token required in WS handshake                  │
│     • Token passed via query param: /ws?token=xxx         │
│     • Token validated on upgrade (before connection)      │
│     • Expired token → connection closed + 4401            │
│                                                           │
│  2. Authorization:                                        │
│     • Subscription limits per user tier                   │
│     • Can't subscribe to admin-only channels              │
│                                                           │
│  3. Connection Limits:                                    │
│     • Max 3 connections per user                          │
│     • Max 50K connections per server                      │
│     • Connection throttling: 100 new conns/sec per server │
│                                                           │
│  4. Message Validation:                                   │
│     • Max message size: 4 KB (client → server)            │
│     • Only allow defined actions (subscribe, unsub, pong) │
│     • Invalid messages → warning, 3 strikes → disconnect  │
│                                                           │
│  5. DDoS Protection:                                      │
│     • Slow loris protection (connection timeout)          │
│     • Invalid frame detection → disconnect                │
│     • IP-based connection limiting at LB level            │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 16. Catatan & Trade-offs

### 16.1 Key Design Decisions

| Decision | Chosen | Alternative | Reasoning |
|----------|--------|-------------|-----------|
| Redis Pub/Sub vs Kafka untuk real-time delivery | **Redis Pub/Sub** | Kafka consumer per WS server | Redis Pub/Sub = fire-and-forget, ultra-low latency. Kafka terlalu berat untuk real-time fan-out ke WS servers |
| WebSocket vs SSE sebagai primary channel | **WebSocket** | SSE | WebSocket full-duplex, bisa kirim subscribe/unsubscribe dari client. SSE one-way saja |
| Custom WS server vs Socket.io | **Custom** | Socket.io, Pusher | Kontrol penuh atas memory, connection lifecycle, batching. Socket.io terlalu abstrak untuk 50K+ conns/server |
| Go vs Node.js untuk WS Gateway | **Go** | Node.js, Java, Rust | Goroutines = ringan per koneksi. Node.js event loop struggle di 50K conns. Rust terlalu complex untuk use case ini |
| Redis vs Memcached untuk hot data | **Redis** | Memcached | Redis punya Pub/Sub + rich data structures (Hash, List, Set). Memcached hanya key-value |
| PostgreSQL vs MongoDB | **PostgreSQL** | MongoDB | Relational data (teams, players, standings punya relasi kuat). ACID compliance untuk data integrity |
| Multi-provider vs Single provider | **Multi** | Single | Redundancy + cross-validation. Single point of failure tidak acceptable untuk live score |
| CDN caching for API vs No CDN | **CDN** | Origin only | 85% traffic offloaded. Tanpa CDN, origin harus handle 1M+ RPS — sangat mahal |

### 16.2 Trade-offs to Be Aware Of

```
⚠️ TRADE-OFF #1: Latency vs Accuracy
   Mengirim update secepat mungkin berisiko kirim data yang
   belum divalidasi. Terlalu banyak validasi = tambah latency.
   Balance: validate di ingestion layer (~100ms), tapi tetap
   kirim. Cross-validate async di background.

⚠️ TRADE-OFF #2: WebSocket Statefulness vs Scalability
   WebSocket connections are stateful (tied to specific server).
   Ini menyulitkan scaling dan rolling updates.
   Mitigation: Graceful drain saat deploy, client auto-reconnect,
   sticky sessions di LB.

⚠️ TRADE-OFF #3: Fan-out Latency vs Infrastructure Cost
   Lebih banyak WS Gateway servers = lebih cepat fan-out,
   tapi lebih mahal. 200 servers × 24/7 = significant cost.
   Balance: Scale berdasarkan peak, aggressive scale-down off-peak.

⚠️ TRADE-OFF #4: Cache Freshness vs Origin Load
   CDN cache yang lebih pendek = data lebih fresh, tapi lebih
   banyak request ke origin. CDN cache 3-5s untuk live matches
   = acceptable staleness untuk polling users. WebSocket users
   mendapat data real-time (bypass CDN).

⚠️ TRADE-OFF #5: Multiple Data Providers vs Cost
   Setiap provider = biaya langganan besar ($$$$$/tahun).
   Tapi single provider = single point of failure + no
   cross-validation. Minimal 2 providers untuk pertandingan
   penting.

⚠️ TRADE-OFF #6: Redis as Source of Truth vs Durability
   Redis di-memory, risiko data loss jika crash.
   Mitigation: Redis RDB + AOF persistence, replicas, dan
   Kafka sebagai durable log untuk recovery.

⚠️ TRADE-OFF #7: Global Deployment vs Complexity
   Multi-region = low latency worldwide, tapi menambah
   complexity (data replication, consistency, cost).
   Start dengan 1 region + CDN, expand saat user base global.
```

### 16.3 What Could Go Wrong (Known Risks)

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data provider outage during major event | Medium | 🔴 Critical | Multi-provider failover + manual input fallback |
| WebSocket thundering herd (mass reconnect) | Medium | 🔴 Critical | Jittered reconnection, connection throttling |
| Score discrepancy between providers | Medium | 🟡 High | Cross-validation monitor, admin override |
| Redis memory exhaustion (too many live matches) | Low | 🔴 Critical | Memory alerts, TTL for expired data, vertical scaling |
| Kafka partition imbalance | Low | 🟡 Medium | Partition rebalancing, monitoring consumer lag |
| CDN cache serving stale data after goal | High | 🟡 Medium | Short TTL + cache purge on score change |
| DDoS during popular match | Medium | 🔴 Critical | CloudFlare DDoS protection, rate limiting |
| Rolling deployment drops WebSocket connections | High | 🟡 Medium | Graceful drain, PodDisruptionBudget |

### 16.4 Future Improvements

- [ ] **AI-Powered Commentary** — Generate automated commentary menggunakan LLM
- [ ] **Predictive Analytics** — xG, win probability, next goal prediction
- [ ] **Video Highlights Integration** — Link ke video highlight saat gol (via partner API)
- [ ] **AR/VR Match Experience** — Immersive match viewing
- [ ] **Social Features** — Chat room per match, reactions, predictions
- [ ] **Personalized Feed** — ML-driven recommendation berdasarkan viewing history
- [ ] **Offline Mode** — Cached data + background sync saat reconnect
- [ ] **GraphQL API** — Reduce over-fetching untuk mobile clients
- [ ] **Edge Computing** — Process events di edge server untuk sub-100ms delivery
- [ ] **Blockchain Verified Scores** — Immutable score record untuk gambling compliance

---

## Ringkasan Arsitektur (TL;DR)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  DATA PROVIDER ──→ Ingestion Service ──→ Kafka ──→ Event         │
│  (Opta/SportRadar)  (normalize+validate)         Processing     │
│                                                    │             │
│                                          ┌─────────┼──────┐     │
│                                          ▼         ▼      ▼     │
│                                        Redis    PostgreSQL Push  │
│                                       (live)   (historical) Notif│
│                                          │                       │
│                                          ▼                       │
│                                    Redis Pub/Sub                 │
│                                          │                       │
│                                          ▼                       │
│                                   WebSocket Gateway              │
│                                   (200 servers × 50K)            │
│                                          │                       │
│                                    ┌─────┼─────┐                │
│                                    ▼     ▼     ▼                │
│                                  Web   Mobile  3rd Party         │
│                                  App    App    (API)             │
│                                                                  │
│  Prinsip Utama:                                                  │
│  1. DATA MASUK secepat mungkin (< 2 detik end-to-end)            │
│  2. CACHE EVERYTHING (Redis + CDN = minimal DB hits)             │
│  3. FAN-OUT BERTINGKAT (1 event → Redis → 200 WS → 10M users)   │
│  4. NEVER WRONG (cross-validate skor, fallback providers)        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> **Filosofi utama:** Live Score adalah sistem yang **write-light, read-heavy** dengan kebutuhan
> **ultra-low latency delivery**. Dari ~5.000 write/detik, kita harus deliver update ke
> **jutaan reader dalam < 2 detik**. Kuncinya adalah: caching agresif, fan-out bertingkat,
> dan multiple data source untuk akurasi.
