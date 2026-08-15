# Skenario Progresif PostgreSQL: Master-Replica + Horizontal Sharding (Citus) + Automated Backup & Recovery

Repositori ini berisi implementasi komprehensif skala industri yang menggabungkan 3 komponen penting arsitektur basis data modern PostgreSQL dalam **1 skenario progresif**:
1. **Master-Replica Streaming Replication** (Ketersediaan Tinggi & Read Scalability)
2. **Horizontal Sharding via Citus Cluster** (Skalabilitas Write & Distribusi Penyimpanan)
3. **Automated Physical/Logical Backup & Restore** (Durabilitas Data, RPO/RTO & Disaster Recovery)

---

## 📐 Arsitektur & Topologi Sistem

```
                         +-----------------------------------+
                         |    KLIEN / APLIKASI UTAMA         |
                         +-----------------------------------+
                                           |
                                  (Write & Read Queries)
                                           v
+------------------------+       +-----------------------------------+
|  Coordinator Replica   | <==== |         citus-coordinator         | (Master Node)
| (Standby Streaming Rep)|       |      (Primary - Port: 5432)       |
|      (Port: 5433)      |       +-----------------------------------+
+------------------------+             /                       \
   (Read-Only Replica)                / (Shard Metadata         \ (Shard Metadata
                                     /   & Routing)              \   & Routing)
                                    v                             v
                         +--------------------+         +--------------------+
                         |   citus-worker-1   |         |   citus-worker-2   |
                         |   (Port: 5434)     |         |   (Port: 5435)     |
                         +--------------------+         +--------------------+
                           (Shard Partition 1)            (Shard Partition 2)

                                           |
                                   (Scheduled Backup)
                                           v
                         +-----------------------------------+
                         |           backup-agent            |
                         |  (Dumps & Restore Verification)   |
                         +-----------------------------------+
```

---

## 📌 Rincian Layanan & Port Mapping

| Service Name | Peran Utama | Host Port | Internal Port | Penjelasan Deskriptif |
| :--- | :--- | :--- | :--- | :--- |
| `citus-coordinator` | Primary Master | `5432` | `5432` | Menerima query aplikasi, mengelola metadata shard, & mengoordinasikan eksekusi query paralel. |
| `citus-coordinator-replica` | Read Standby Replica | `5433` | `5432` | Synchronous/Asynchronous Streaming Replica dari Master. Khusus menangani query `SELECT` (Read-Only). |
| `citus-worker-1` | Worker Node 1 | `5434` | `5432` | Menyimpan pecahan (shard) data fisik terdistribusi untuk `users` & `orders`. |
| `citus-worker-2` | Worker Node 2 | `5435` | `5432` | Menyimpan pecahan (shard) data fisik terdistribusi untuk `users` & `orders`. |
| `backup-agent` | Disaster Recovery Agent | - | - | Container terisolasi pengelola backup terjadwal (`pg_dump` / `pg_basebackup`) & pengujian restore. |

---

## 🚀 Panduan Memulai Cepat (Quick Start)

### Prasyarat
- Docker & Docker Compose (`docker compose` v2.x+)
- RAM bebas minimal 2-4 GB

### Eksekusi Otomatis 1-Command
Cukup jalankan satu script orkestrasi di bawah ini untuk memulai seluruh klaster dan mengeksekusi Tahap 1, 2, dan 3 secara otomatis:

```bash
./scripts/run_all_progressive.sh
```

---

## 🧪 Penjelasan Detail Skenario Progresif

Skenario ini disusun secara bertahap agar Anda dapat mengamati evolusi arsitektur secara terstruktur.

---

### Tahap 1: Master-Replica Streaming Replication

Pada tahap ini, kita memverifikasi bahwa seluruh data yang ditulis pada Primary Master (`citus-coordinator`) langsung direplikasikan secara real-time ke Standby Replica (`citus-coordinator-replica`).

- **Script Pengujian**: `./scripts/step1_master_replica.sh`
- **Poin Verifikasi**:
  1. Status koneksi `pg_stat_replication` di Master.
  2. Penulisan record baru di Master (`port 5432`) dapat langsung dibaca dari Replica (`port 5433`).
  3. Percobaan penulisan (Write/`INSERT`) ke Replica secara otomatis ditolak (`read-only transaction`).

---

### Tahap 2: Horizontal Sharding (Citus Cluster)

Pada tahap ini, kita mengonversi tabel relasional standar menjadi **Distributed Tables** dan **Reference Tables** menggunakan ekstensi Citus.

- **Script Pengujian**: `./scripts/step2_sharding.sh`
- **Poin Verifikasi**:
  1. Pendaftaran node `citus-worker-1` dan `citus-worker-2` ke Master Coordinator via `citus_add_node()`.
  2. Pembagian data `users` (10.000 rows) dan `orders` (20.000 rows) secara merata ke dalam pecahan shard pada `worker-1` dan `worker-2`.
  3. Penggunaan **Reference Table** (`categories`) yang direplikasikan utuh ke semua worker node untuk optimasi join lokal.
  4. Eksekusi **Distributed Execution Plan** (`EXPLAIN ANALYZE`) di mana Coordinator mendistribusikan query ke worker nodes secara paralel.

---

### Tahap 3: Automated Backup & Disaster Recovery Restore

Pada tahap ini, kita mensimulasikan prosedur pemeliharaan durabilitas data dan pemulihan bencana (*Disaster Recovery*).

- **Script Pengujian**: `./scripts/step3_backup_restore.sh`
- **Poin Verifikasi**:
  1. Pembuatan file backup terkompresi otomatis oleh container `backup-agent`.
  2. Simulasi pembuatan database kosong baru `restore_db`.
  3. Pemulihan (*restore*) seluruh schema, data shard, dan tabel referensi dari file backup.
  4. Verifikasi bahwa jumlah data sebelum dan sesudah restore cocok 100%.

---

## 🛠️ Perintah Pengujian Manual

Anda juga dapat masuk ke container dan menjalankan query SQL secara interaktif:

```bash
# Connect ke Primary Master Coordinator (Port 5432)
docker exec -it citus-coordinator psql -U postgres -d app_db

# Connect ke Read Replica (Port 5433)
docker exec -it citus-coordinator-replica psql -U postgres -d app_db

# Connect ke Worker Node 1 (Port 5434)
docker exec -it citus-worker-1 psql -U postgres -d app_db
```

Query untuk mengecek distribusi shard pada Coordinator:
```sql
SELECT nodename, count(*) AS shard_count 
FROM citus_shards 
GROUP BY nodename;
```

---

## 💡 Best Practices Lingkungan Produksi

1. **Connection Pooling**: Gunakan **PgBouncer** di depan `citus-coordinator` untuk mengelola koneksi aplikasi berkepadatan tinggi.
2. **High Availability untuk Coordinator**: Gabungkan Citus Coordinator dengan **Patroni** + **pg_auto_failover** atau **Keepalived** untuk otomatisasi Failover Master -> Replica.
3. **Backup Strategy 3-2-1**:
   - **WAL Archiving**: Aktifkan `archive_mode = on` untuk Point-In-Time Recovery (PITR) detik-demi-detik menggunakan **pgBackRest** atau **WAL-G**.
   - Simpan minimal 1 salinan backup di media penyimpanan terpisah (Cloud Object Storage seperti AWS S3 / Google Cloud Storage).
