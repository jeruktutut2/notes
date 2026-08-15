# Skenario Pengujian Data Recovery Center (DRC)

Dokumen ini berisi panduan skenario pengujian lengkap untuk proyek edukasi Data Recovery Center.

---

## Skenario 1: Normal Operation & Replikasi Real-Time (DC -> DRC)

### Konsep
Dalam kondisi normal, Data Center (DC) memproses semua operasi penulisan (Write) dan pembacaan (Read). PostgreSQL DC bertindak sebagai **Primary**, sedangkan PostgreSQL DRC bertindak sebagai **Standby** yang menerima aliran Write-Ahead Log (WAL) secara real-time.

### Langkah Pengujian
1. Jalankan lingkungan:
   ```bash
   ./scripts/setup.sh
   ```
2. Jalankan skenario pengiriman data dari DC ke DRC:
   ```bash
   ./scripts/simulate-dc-to-drc.sh
   ```
3. Periksa replikasi secara rinci:
   ```bash
   ./scripts/check-replication.sh
   ```

### Hasil yang Diharapkan
- Data yang di-insert via API (`POST /api/data`) langsung masuk ke `pg-dc`.
- Dalam waktu hitungan milidetik (< 1 detik), data tersebut dapat di-select langsung dari `pg-drc` (Port 5433).
- Lag byte replikasi berada di angka 0 atau mendekati 0.

---

## Skenario 2: Data Center Down & Proses Failover (Pengambilalihan Peran)

### Konsep
Ketika Data Center mengalami bencana / outage total (hardware failure, power outage, bencana alam, dll.):
1. Server DC mati total.
2. DRC (Standby) dipromosikan menjadi **Primary (Read-Write)** baru menggunakan `pg_promote()`.
3. Aplikasi mengalihkan koneksi ke DRC (PgBouncer DRC).
4. Aplikasi kembali dapat menerima penulisan data baru walaupun DC mati total.

### Langkah Pengujian
1. Simulasi DC mati total:
   ```bash
   ./scripts/simulate-dc-down.sh
   ```
2. Eksekusi Failover:
   ```bash
   ./scripts/failover.sh
   ```
3. Cek status via REST API:
   ```bash
   curl http://localhost:8080/health
   curl http://localhost:8080/api/status
   ```
4. Tambahkan data baru saat DC mati:
   ```bash
   curl -X POST http://localhost:8080/api/data \
     -H "Content-Type: application/json" \
     -d '{"title":"Data Baru di DRC","content":"Ditulis saat DC Down"}'
   ```

### Hasil yang Diharapkan
- `pg-dc` berstatus STOPPED / DOWN.
- `pg-drc` berubah status dari `pg_is_in_recovery() = true` menjadi `false` (Primary baru).
- API Aplikasi mengembalikan `"active_target": "drc"`.
- Data baru berhasil ditulis ke `pg-drc`.

---

## Skenario 3: Pemulihan DC & Proses Failback (Mengembalikan Peran ke DC)

### Konsep
Setelah Data Center fisik selesai diperbaiki:
1. Server DC di-restore/dinyalakan kembali.
2. Data baru yang dibuat di DRC selama periode failover di-sinkronkan kembali ke DC (resync via `pg_basebackup`).
3. DC dipromosikan kembali menjadi **Primary Utama**.
4. DRC dikembalikan fungsinya menjadi **Standby Replica** (Streaming WAL dari DC ke DRC diaktifkan lagi).
5. Koneksi aplikasi dikembalikan ke DC (PgBouncer DC).

### Langkah Pengujian
1. Eksekusi Failback:
   ```bash
   ./scripts/failback.sh
   ```
2. Verifikasi status replikasi kembali normal:
   ```bash
   ./scripts/check-replication.sh
   ```
3. Uji penulisan data di DC kembali:
   ```bash
   ./scripts/simulate-dc-to-drc.sh
   ```

### Hasil yang Diharapkan
- `pg-dc` kembali menjadi **Primary** (`pg_is_in_recovery() = false`).
- `pg-drc` kembali menjadi **Standby** (`pg_is_in_recovery() = true`).
- API Aplikasi mengembalikan `"active_target": "dc"`.
- Streaming replication dari DC ke DRC aktif kembali (terlihat di `pg_stat_replication`).
- Data yang dibuat selama failover tetap utuh dan tidak hilang.

---

## Ringkasan Perintah

| Tujuan | Perintah |
| :--- | :--- |
| Inisialisasi awal | `./scripts/setup.sh` |
| Cek status replikasi | `./scripts/check-replication.sh` |
| Uji kirim data DC -> DRC | `./scripts/simulate-dc-to-drc.sh` |
| Simulasi DC mati | `./scripts/simulate-dc-down.sh` |
| Jalankan Failover | `./scripts/failover.sh` |
| Jalankan Failback | `./scripts/failback.sh` |
| Health check sistem | `./scripts/health-check.sh` |
| Monitoring real-time | `./monitoring/monitor.sh` |
| Cleanup lingkungan | `./scripts/cleanup.sh` |
