# 🚀 Panduan Running Demo DC & DRC (Docker Compose + Golang Echo v5)

Folder ini berisi implementasi runnable menggunakan **Docker Compose**, **PostgreSQL Physical Streaming Replication**, **Golang Echo v5 API Service**, dan **HAProxy Router** untuk mensimulasikan sistem *Active-Standby Data Center & Disaster Recovery Center*.

---

## 🏗️ Komponen Container

| Nama Service | Peran / Deskripsi | IP/Port Internal | Port Published |
| :--- | :--- | :--- | :--- |
| `postgres-dc` | PostgreSQL Primary (Read-Write - Jakarta) | 5432 | `5432` |
| `postgres-drc` | PostgreSQL Standby (Read-Only Replica - Surabaya) | 5432 | `5433` |
| `app-dc` | Golang Echo Web Service (DC Node) | 1323 | `1323` |
| `app-drc` | Golang Echo Web Service (DRC Node) | 1323 | `1324` |
| `haproxy` | Traffic Router / GSLB Simulator | 8080 / 8404 | `8080` (API) & `8404` (Stats) |

---

## ⚡ Cara Menjalankan (Step-by-Step)

### 1. Jalankan Seluruh Cluster dengan Docker Compose
```bash
cd demo
docker-compose up --build -d
```

### 2. Cek Logs Inisialisasi Replikasi Database
```bash
docker-compose logs -f postgres-drc
```
*Pastikan muncul pesan `pg_basebackup: base backup completed` dan PostgreSQL DRC berjalan dalam mode standby (`database system is ready to accept read only connections`).*

---

## 🧪 Pengujian Skenario Ops & Disaster

### Skenario A: Operasional Normal (Active DC)
1. **Buka Web Interface Router**: Akses `http://localhost:8080` di browser.
   - Halaman akan menunjukkan status `MAIN_DATA_CENTER_JAKARTA` dan badge hijau `Primary (Read-Write)`.

2. **Buat Catatan Baru (Write Operation di DC)**:
   ```bash
   curl -X POST http://localhost:8080/api/notes \
        -H "Content-Type: application/json" \
        -d '{"title":"Catatan Pertama", "content":"Transaksi berhasil di DC Utama"}'
   ```
   *Respon*: HTTP 201 Created.

3. **Verifikasi Streaming Replication di Standby DRC**:
   Akses data langsung melalui port aplikasi DRC (`http://localhost:1324/api/notes`) atau via PostgreSQL DRC langsung:
   ```bash
   docker exec -it postgres-drc psql -U postgres -d dcdrc_db -c "SELECT * FROM notes;"
   ```
   *Data yang dibuat di DC Utama otomatis muncul secara real-time di DRC!*

---

### Skenario B: Bencana Terjadi di DC Utama (Simulasi Failover)
1. **Simulasikan Matinya DC Utama (Jakarta Down)**:
   ```bash
   docker stop app-dc postgres-dc
   ```

2. **Pengujian Failover Router**:
   Akses kembali `http://localhost:8080/` atau jalankan Healthcheck:
   ```bash
   curl http://localhost:8080/health
   ```
   *HAProxy secara otomatis mengalihkan 100% traffic ke `DISASTER_RECOVERY_CENTER_SURABAYA` tanpa downtime pada layar pengguna!*

3. **Cek Dashboard Stats HAProxy**:
   Buka `http://localhost:8404` (User: `admin`, Password: `admin`).
   - Server `app_dc` akan berwarna **MERAH (DOWN)**.
   - Traffic otomatis mengalir ke `app_drc` yang berwarna **HIJAU (BACKUP ACTIVE)**.

4. **Percobaan Write pada DRC (Read-Only Safety Protection)**:
   ```bash
   curl -X POST http://localhost:8080/api/notes \
        -H "Content-Type: application/json" \
        -d '{"title":"Tes Write", "content":"Mencoba menulis ke DRC"}'
   ```
   *Respon*: `HTTP 423 Read-Only Replica (DRC Standby)` — Melindungi database DRC dari *unauthorized split-brain writes* sampai dipromosikan secara sah.

---

### Skenario C: Pemulihan (Failback & Reverse Synchronization)
1. **Perintah Otomatis (All-in-One Script)**:
   Kami menyediakan script otomatis `run-failover-demo.sh` untuk mensimulasikan seluruh skenario ini (Normal -> Failover + Write di DRC -> Reverse Sync Data ke DC).
   ```bash
   cd demo
   ./run-failover-demo.sh all
   ```

2. **Perintah Tahapan Manual via Script**:
   - ` ./run-failover-demo.sh normal`   : Memulai cluster & menulis data awal di DC.
   - ` ./run-failover-demo.sh failover` : Mematikan DC, promote DRC ke Read-Write, dan menulis data baru di DRC.
   - ` ./run-failover-demo.sh failback` : Melakukan reverse sync snapshot dari DRC ke DC Utama dan mengembalikan status ke semula.

