# 02. Mekanisme Jaringan, Replikasi Data & High Availability

## 1. Mekanisme Routing Traffic & Failover Jaringan

Untuk memastikan pengguna dialihkan secara mulus dari DC ke DRC tanpa perlu mengubah konfigurasi di sisi aplikasi/client, digunakan kombinasi 3 layer routing:

```
[User Request]
       │
       ▼
 [Layer 1: GSLB / DNS Failover] ──(Health Check Fail)──► [Switch IP Address to DRC Endpoint]
       │
       ▼
 [Layer 2: BGP Anycast Routing]  ──(Route Withdrawal)─► [Advertise DRC Subnet IP to Internet]
       │
       ▼
 [Layer 3: Local Virtual IP (VIP)] ──(Keepalived/Patroni)─► [Reassign VIP to Local Active Node]
```

### A. Global Server Load Balancing (GSLB) / DNS Failover
- GSLB terus-menerus memantau HTTPS Health Check Endpoint di DC Utama (`https://dc.domain.com/health`).
- Jika DC Utama gagal merespon selama 3x berturut-turut (15 detik), GSLB secara otomatis mengubah catatan DNS `A Record` domain `api.domain.com` dari IP Public DC (`203.0.113.10`) menjadi IP Public DRC (`198.51.100.10`).
- TTL DNS disetel sangat rendah (**TTL = 10 - 60 detik**) untuk mempercepat propagasi DNS di sisi client.

### B. BGP Anycast / Route Announcement
- Pada infrastruktur Enterprise tingkat lanjut, subnet IP Public milik organisasi di-announce menggunakan protokol **BGP** ke ISP.
- Saat DC down, router DC menarik rute BGP (*Route Withdrawal*), dan router DRC langsung meng-announce rute prefix IP yang sama ke ISP Surabaya. Dengan cara ini, IP Public tidak perlu berganti sama sekali.

---

## 2. Mekanisme Replikasi Data (Database Streaming & Storage)

### A. PostgreSQL Physical Streaming Replication
Replikasi berbasis **WAL (Write-Ahead Logging)** digunakan untuk mengirimkan perubahan data mentah pada tingkat block binary dari Primary (DC) ke Standby (DRC).

```
   ┌────────────────────────────────┐                 ┌────────────────────────────────┐
   │    Main DC: PostgreSQL Leader  │                 │   DRC Site: PostgreSQL Standby │
   │                                │                 │                                │
   │  [ Transaction Execution ]     │                 │                                │
   │              │                 │                 │                                │
   │              ▼                 │                 │                                │
   │     [ Write to WAL Buffer ]    │                 │                                │
   │              │                 │                 │                                │
   │              ├─────────────────┼── Physical ────►│  [ WAL Receiver Process ]      │
   │              │ (Async Stream)  │   Streaming     │              │                 │
   │              ▼                 │   TCP 5432      │              ▼                 │
   │     [ Local WAL Disk ]         │                 │     [ Write to Relay WAL ]     │
   │              │                 │                 │              │                 │
   │              ▼                 │                 │              ▼                 │
   │  [ WAL Archiver (pgBackRest) ] │                 │  [ Startup/Startup Process ]   │
   │              │                 │                 │     (Apply WAL to DB Block)    │
   └──────────────┼─────────────────┘                 └────────────────────────────────┘
                  │
                  ▼
   ┌────────────────────────────────┐
   │ Offsite S3 / MinIO Storage     │
   │ (Central Point of WAL Backup)  │
   └────────────────────────────────┘
```

#### Synchronous vs Asynchronous Trade-off:
1. **Intra-DC (Primary ke Replica lokal di DC)**:
   - Menggunakan **Synchronous Replication** (`synchronous_commit = on`).
   - *Keuntungan*: Zero Data Loss di dalam DC utama jika 1 server database mati.
   - *Latensi*: Sangat rendah (< 1ms via LAN 10Gbps).

2. **Inter-DC (Primary DC ke Standby DRC)**:
   - Menggunakan **Asynchronous Streaming Replication** (`synchronous_commit = local`).
   - *Alasan*: Latensi jaringan antar-kota (~12-15ms) akan memperlambat setiap transaksi `COMMIT` jika menggunakan synchronous replication.
   - *Dampak*: RPO di DRC adalah **< 1 detik** (bergantung pada lag jaringan).

### B. WAL Archiving (Fallback & Point-in-Time Recovery)
Selain streaming real-time, WAL segment disalin ke S3/MinIO Object Storage menggunakan **pgBackRest** setiap kali 1 file WAL (16MB) penuh.
- Jika koneksi streaming antar DC terputus sementara (misal: kabel FO putus selama 2 jam), node DRC tidak perlu membuat ulang database dari awal (*re-base*).
- Node DRC akan secara otomatis mengunduh file WAL yang tertinggal langsung dari Object Storage S3 (*WAL Restore Command*) begitu koneksi pulih.

---

## 3. Consensus Cluster & Pencegahan Split-Brain

Salah satu bahaya terbesar dalam sistem DRC adalah **Split-Brain Syndrome**: kondisi di mana jaringan antar DC terputus, dan node DRC secara salah menduga bahwa DC mati, lalu mengangkat dirinya sendiri menjadi Leader (Primary baru). Akibatnya, kedua lokasi menerima transaksi *Read-Write* secara paralel yang menyebabkan kerusakkan data permanen.

### A. Solusi: Distributed Configuration Store (Patroni + etcd Quorum)
Untuk mencegah *Split-Brain*, digunakan mekanisme **Quorum (Jumlah Ganjil Minimal)** menggunakan **etcd** 3-Node:

```
                  ┌──────────────────────┐
                  │ Node 1: etcd (DC)    │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
┌──────────────────────┐           ┌──────────────────────┐
│ Node 2: etcd (DC)    │           │ Node 3: etcd (DRC)   │
└──────────────────────┘           └──────────────────────┘
```

- Total Node etcd = **3 Node** (Quorum minimal = $(3/2) + 1 = \mathbf{2\text{ Node}}$).
- **Aturan Quorum**: Node database HANYA boleh memegang status *LEADER* jika ia berhasil memperoleh kunci kepemimpinan (*leader lock*) dari mayoritas etcd cluster (minimal 2 dari 3 node etcd menyetujui).

### B. Skenario Putus Jaringan Inter-DC:
1. Kabel jaringan Jakarta - Surabaya terputus.
2. Node DRC (Surabaya) hanya dapat mengontak 1 node etcd lokalnya sendiri (Node 3).
3. Karena 1 node < Quorum (2 node), **Node DRC MENOLAK meng-promote dirinya menjadi Leader**. Node DRC tetap berada dalam mode Safe Read-Only Standby.
4. DC Utama (Jakarta) masih memiliki 2 node etcd (Node 1 & Node 2 = 2/3 Quorum). DC Utama tetap berjalan normal sebagai Leader tanpa gangguan.
5. **Kesimpulan**: Split-brain berhasil dicegah 100%.
