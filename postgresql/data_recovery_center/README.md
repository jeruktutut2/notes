# Data Recovery Center (DRC) - Panduan Pembelajaran & Implementasi Lengkap

Proyek edukasi komprehensif untuk mempelajari konsep **Data Recovery Center (DRC)**, hubungannya dengan **Data Center (DC)**, mekanisme **Streaming Replication**, pengambilalihan peran (**Failover**), serta pengembalian peran (**Failback**).

---

## 📚 Pembahasan Konseptual DRC

### 1. Apa itu Data Recovery Center (DRC)?
**Data Recovery Center (DRC)** — sering juga disebut *Disaster Recovery Center* — adalah fasilitas infrastruktur teknologi informasi cadangan yang dirancang khusus untuk merecovery (memulihkan) data dan mengambil alih operasi sistem ketika terjadi bencana alam, kegagalan infrastruktur total, atau gangguan serius pada **Data Center (DC) utama**.

DRC berfungsi sebagai **"asuransi kelangsungan bisnis"** (*Business Continuity Plan*) untuk memastikan bahwa layanan aplikasi dan data perusahaan tidak mati permanen saat terjadi musibah pada lokasi fisik utama.

---

### 2. Hubungan DC dengan DRC

| Parameter | Data Center (DC) Utama | Data Recovery Center (DRC) |
| :--- | :--- | :--- |
| **Fungsi Utama** | Pusat pemrosesan harian (Production) | Tempat cadangan & pemulihan bencana |
| **Status Operasional** | **Active** (Selalu memproses Read & Write) | **Standby** (Pasif, hanya menerima sinkronisasi data) |
| **Tujuan Utama** | Performa & efisiensi bisnis harian | Kelangsungan bisnis & pencegahan kehilangan data |
| **Karakteristik Database** | **Primary / Master** (Read-Write) | **Standby / Replica** (Read-Only dalam kondisi normal) |
| **Lokasi Geografis** | Lokasi operasional utama | Lokasi terpisah secara geografis (>100 km) |

---

### 3. Bagaimana DC Mengirim Data ke DRC?

DC mengirimkan data ke DRC menggunakan **PostgreSQL Streaming Replication** berbasis **WAL (Write-Ahead Logging)**:

1. **Aplikasi Menulis Data**: Ketika aplikasi menyimpan data baru, PostgreSQL DC pertama kali menulis perubahan tersebut ke dalam berkas **WAL (Write-Ahead Log)** di server DC.
2. **Streaming WAL Receiver**: Proses `walreceiver` di DRC terhubung secara terus-menerus (*persistent TCP connection*) ke proses `walsender` di DC via port database (5432).
3. **Replikasi Real-Time**: Setiap kali ada transaksi baru commit di DC, catatan WAL langsung disalurkan (*streamed*) melalui jaringan ke DRC.
4. **Replay di DRC**: PostgreSQL DRC mengaplikasikan (*replay*) catatan WAL tersebut ke dalam struktur penyimpanan DRC secara instan.

> **RPO (Recovery Point Objective)**: Dengan streaming replication, perbedaan data (lag) antara DC dan DRC hanya berkisar hitungan milidetik (*near-zero data loss*).

---

### 4. Pada Saat Kapan DRC Digunakan?

DRC diaktifkan untuk mengambil alih operasi hanya pada kondisi darurat:
1. **Bencana Alam**: Gempa bumi, banjir bandang, kebakaran, atau badai di lokasi Data Center fisik.
2. **Kegagalan Infrastruktur Utama**: Listrik mati total (blackout panjang), kegagalan sistem pendingin (HVAC failure), atau perusakan fisik hardware.
3. **Serangan Siber Tingkat Tinggi**: Serangan ransomware massal atau sabotase fisik pada DC.
4. **Pengujian Disaster Recovery (DR Drill)**: Simulasi rutin tahunan/semesteran untuk menguji kesiapan tim dan infrastruktur DR.

---

### 5. Jika DC Down, Apakah DRC Menggantikan Peran DC? Dan Bagaimana Cara Mengambil Alih?

**Ya, sementara.** Ketika DC mengalami outage, DRC mengambil alih seluruh fungsi database dan aplikasi melalui proses yang disebut **FAILOVER**.

#### 🛠️ CARA DRC MENGAMBIL ALIH (PROSES FAILOVER):

```
       KONDISI DC DOWN:
       ┌──────────────────────┐        ┌──────────────────────┐
       │     PostgreSQL DC    │        │    PostgreSQL DRC    │
       │     ❌ MATI / OFF    │        │  (Dipromosikan ke)   │
       └──────────────────────┘        │   PRIMARY READ-WRITE │
                                       └──────────▲───────────┘
                                                  │
       ┌──────────────────────┐        ┌──────────┴───────────┐
       │   Golang Echo App    │───────►│    PgBouncer DRC     │
       └──────────────────────┘        └──────────────────────┘
```

Proses pengambilalihan terdiri dari **3 Langkah Utama**:

1. **Deteksi Kegagalan (Failure Detection)**:
   Sistem monitoring atau health-check mendeteksi bahwa DC utama mati total (tidak merespons ping/connection query).

2. **Promosi Database Standby (Promote Standby to Primary)**:
   Database DRC yang tadinya berstatus Read-Only dipromosikan menjadi **Primary (Read-Write)** baru.
   - Pada PostgreSQL, ini dilakukan dengan memanggil fungsi:
     ```sql
     SELECT pg_promote();
     ```
     Atau mengeksekusi command line: `pg_ctl promote`.
   - File `standby.signal` pada data directory DRC akan dihapus secara otomatis, menandakan bahwa DRC kini adalah Master/Primary.

3. **Pengalihan Trafik Aplikasi (Traffic Redirection)**:
   Koneksi aplikasi yang tadinya mengarah ke PgBouncer DC dialihkan ke **PgBouncer DRC**.
   - Aplikasi kini melakukan operasi Read & Write langsung ke PostgreSQL DRC.

---

### 6. Apakah Aplikasi Menggunakan DRC Sebagai Database Utama?

**Tidak dalam kondisi normal.**
- **Saat Normal**: Aplikasi hanya terhubung ke **DC** untuk operasi Read & Write. DRC murni berada dalam status standby pasif.
- **Saat Emergency/Disaster**: Aplikasi dialihkan sementara ke **DRC** sampai DC utama berhasil dipulihkan.

---

### 7. Bagaimana Cara Melakukan FAILBACK Setelah DC Pulih?

**Failback** adalah proses mengembalikan peran operasional utama kembali dari DRC ke Data Center (DC) setelah DC berhasil diperbaiki.

#### 🛠️ CARA MELAKUKAN FAILBACK (SKENARIO FAILBACK):

```
       KONDISI FAILBACK:
       ┌──────────────────────┐        ┌──────────────────────┐
       │    PostgreSQL DC     │◄───────│    PostgreSQL DRC    │
       │ (Resync & Dipromosikan│ (Base  │ (Mengirim data baru  │
       │  Kembali ke PRIMARY) │ Backup)│  yang tercipta)      │
       └──────────┬───────────┘        └──────────────────────┘
                  │ Streaming Replication
                  ▼ (Normal Kembali)
       ┌──────────────────────┐
       │    PostgreSQL DRC    │
       │  (Kembali Standby)   │
       └──────────────────────┘
```

Proses Failback dilakukan melalui **4 Langkah Utama**:

1. **Menyalakan & Menyinkronkan Kembali DC (Re-synchronization)**:
   - Server DC dinyalakan kembali.
   - Karena ada data baru yang ditulis ke DRC selama masa failover, DC harus mengambil (*catch up*) data terbaru dari DRC menggunakan `pg_basebackup`.

2. **Mempromosikan Kembali DC Menjadi Primary Utama**:
   - DC dinyatakan sebagai **Primary Utama** kembali.
   - File `standby.signal` di DC dibuang dan PostgreSQL DC di-restart.

3. **Mengembalikan DRC Menjadi Standby Replica**:
   - DRC di-rekonfigurasi kembali menjadi **Standby Replica** yang mendengarkan streaming WAL dari DC.
   - Streaming replication DC → DRC aktif kembali.

4. **Pengalihan Kembali Trafik Aplikasi (Switch Back Connection)**:
   - Aplikasi mengalihkan target database dari PgBouncer DRC kembali ke **PgBouncer DC**.

---

## 🏗️ Arsitektur Teknologi Proyek

| Komponen | Teknologi | Keterangan |
| :--- | :--- | :--- |
| **Data Center (DC)** | PostgreSQL 16 Alpine | Primary Database (Port 5432) |
| **Recovery Center (DRC)** | PostgreSQL 16 Alpine | Standby Replica (Port 5433) |
| **DC Connection Pooler** | PgBouncer | Managed connection pool DC (Port 6432) |
| **DRC Connection Pooler**| PgBouncer | Managed connection pool DRC (Port 6433) |
| **Backend REST API** | Golang 1.25 + Echo v5 | High-performance Go web API (Port 8080) |
| **Orchestration** | Docker Compose | Kontainerisasi seluruh komponen |

---

## 🚀 Cara Menjalankan Proyek

### 1. Inisialisasi & Setup Lingkungan
Jalankan script `setup.sh` untuk membangun dan memicu 5 service Docker:
```bash
./scripts/setup.sh
```

### 2. Memeriksa Status Replikasi Real-Time
Untuk melihat status LSN, bytes lag, dan konsistensi row data antara DC dan DRC:
```bash
./scripts/check-replication.sh
```

### 3. Simulasi Pengiriman Data DC -> DRC
Jalankan skenario penulisan data di DC dan lihat replikasinya langsung di DRC:
```bash
./scripts/simulate-dc-to-drc.sh
```

### 4. Simulasi Bencana (DC Down)
Matikan server DC secara paksa untuk menguji deteksi kesehatan aplikasi:
```bash
./scripts/simulate-dc-down.sh
```

### 5. Eksekusi Failover (DRC Takeover)
Promosikan DRC menjadi Primary dan alihkan aplikasi ke DRC:
```bash
./scripts/failover.sh
```

### 6. Eksekusi Failback (Kembali ke DC)
Setelah DC dipulihkan, lakukan sinkronisasi balik dan kembalikan peran ke DC:
```bash
./scripts/failback.sh
```

### 7. Monitoring Real-Time Terminal
Jalankan dashboard monitoring live:
```bash
./monitoring/monitor.sh
```

### 8. Cleanup Environment
Untuk menghentikan dan menghapus semua container serta data volume:
```bash
./scripts/cleanup.sh
```

---

## 📐 Diagram Arsitektur & Alur Trafik

### 1. Kondisi Normal (Normal Operation)
Aplikasi menulis dan membaca data dari **PostgreSQL DC (Primary)** melalui **PgBouncer DC**. Perubahan data secara real-time dialirkan ke **PostgreSQL DRC (Standby)** via WAL Streaming.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         NORMAL OPERATION                              │
│                                                                       │
│  ┌─────────┐     ┌───────────────┐     ┌─────────────────────────┐   │
│  │  Golang  │────▶│   PgBouncer   │────▶│  PostgreSQL Primary     │   │
│  │  Echo v5 │     │  (DC Pool)    │     │  (Data Center)          │   │
│  │   App    │     └───────────────┘     └──────────┬──────────────┘   │
│  └─────────┘                              WAL Streaming │             │
│                                                         ▼             │
│                                            ┌─────────────────────┐   │
│                                            │ PostgreSQL Standby   │   │
│                                            │ (Recovery Center)    │   │
│                                            └─────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### 2. Kondisi DC Down (Failover Active)
Saat Data Center mati, DRC dipromosikan menjadi **Primary**. Aplikasi dialihkan untuk terhubung ke **PgBouncer DRC**.

```
┌──────────────────────────────────────────────────────────────────────┐
│                       FAILOVER (DC DOWN)                              │
│                                                                       │
│  ┌─────────┐     ┌───────────────┐     ┌─────────────────────────┐   │
│  │  Golang  │────▶│   PgBouncer   │────▶│  PostgreSQL (Promoted)  │   │
│  │  Echo v5 │     │ (DRC Pool)    │     │  (Recovery Center)      │   │
│  │   App    │     └───────────────┘     └─────────────────────────┘   │
│  └─────────┘                                                          │
│                    ┌─────────────────────────────────────┐            │
│                    │  DC PostgreSQL: ❌ DOWN / OFFLINE    │            │
│                    └─────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 Endpoints REST API (Golang Echo v5)

Aplikasi menyediakan endpoint REST API untuk pengujian dan otomasi failover:

| Method | Endpoint | Fungsi / Deskripsi |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check aplikasi dan konektivitas database aktif |
| `GET` | `/api/status` | Informasi status sistem, database target, total baris & record terakhir |
| `GET` | `/api/replication` | Cek status replikasi, LSN, mode recovery, dan jumlah replica aktif |
| `GET` | `/api/data` | Mengambil seluruh daftar data transaksi |
| `POST` | `/api/data` | Menambah data transaksi baru (Demonstrasi Write) |
| `GET` | `/api/data/:id` | Mengambil data transaksi berdasarkan ID |
| `GET` | `/api/logs` | Mengambil riwayat log event Disaster Recovery |
| `POST` | `/api/failover` | Pemicu manual switch target database aplikasi ke **DRC** |
| `POST` | `/api/failback` | Pemicu manual switch target database aplikasi kembali ke **DC** |

---

## 📝 Catatan Teknis Replikasi & RPO/RTO

> [!NOTE]
> **Asynchronous vs Synchronous Replication**:
> - Proyek ini secara default menggunakan **Asynchronous Streaming Replication**.
> - **Kelebihan**: Latensi penulisan data di DC sangat cepat (tidak terhambat kecepatan jaringan inter-DC).
> - **Toleransi Loss**: RPO mendekati nol (beberapa milidetik transaksi terakhir yang mungkin belum terkirim jika DC mendadak hancur).
> - **Zero Data Loss (Synchronous)**: Jika sistem membutuhkan RPO = 0 mutlak, PostgreSQL dapat dikonfigurasi dengan `synchronous_commit = remote_apply` / `on` di `postgresql.conf`. Namun hal ini akan menambah latency pada setiap proses INSERT/UPDATE.

---

## 📌 Struktur Berkas Proyek

```
data_recovery_center/
├── README.md                      # Dokumentasi pembelajaran DRC lengkap
├── docker-compose.yml             # Orchestrasi 5 services Docker
├── Dockerfile.app                 # Build Golang Echo v5 app (Multi-stage)
├── app/                           # Aplikasi Golang Echo v5
│   ├── go.mod
│   ├── main.go                    # Server HTTP & routing
│   ├── config/config.go           # Konfigurasi koneksi DC & DRC
│   ├── model/model.go             # Data structs & API schemas
│   ├── repository/repository.go   # Operasi database & pool management
│   ├── handler/handler.go         # REST API handlers
│   └── middleware/middleware.go   # HTTP logger
├── db/                            # Scripts database
│   ├── init-primary.sh            # Setup replication user & slot di DC
│   ├── init-primary.sql           # Schema SQL & seed data awal
│   └── setup-standby.sh           # Setup standby via pg_basebackup di DRC
├── pgbouncer/                     # Konfigurasi PgBouncer
│   ├── Dockerfile
│   ├── pgbouncer-dc.ini           # Config PgBouncer DC
│   ├── pgbouncer-drc.ini          # Config PgBouncer DRC
│   └── userlist.txt
├── scripts/                       # Skenario eksekusi shell scripts
│   ├── setup.sh                   # Build & start all containers
│   ├── check-replication.sh      # Cek LSN lag & data consistency
│   ├── simulate-dc-to-drc.sh     # Demo write DC -> streaming -> DRC
│   ├── simulate-dc-down.sh       # Demo DC outage
│   ├── failover.sh                # Demo promotion & takeover ke DRC
│   ├── failback.sh                # Demo resync & switch back ke DC
│   ├── health-check.sh           # Health check all components
│   └── cleanup.sh                 # Tear down containers & volumes
├── monitoring/
│   └── monitor.sh                 # Terminal real-time dashboard
└── docs/
    └── SCENARIOS.md               # Skenario pengujian terperinci
```

