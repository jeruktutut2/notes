# Panduan Simulasi Point-In-Time Recovery (PITR) PostgreSQL

Panduan ini akan membawa Anda melalui skenario lengkap dari awal sampai akhir mengenai cara melakukan PITR pada PostgreSQL. Skenario ini menggunakan **PgBouncer** sebagai connection pooler dan aplikasi **Golang (Echo V4/V5)** untuk mensimulasikan trafik. 

## Arsitektur

- **PostgreSQL 16**: Berjalan di Docker dengan volume ter-mount (`./data` dan `./archive`). Konfigurasi WAL Archiving sudah diaktifkan di `postgres/postgresql.conf`.
- **PgBouncer**: Berjalan di depan PostgreSQL (port 6432) untuk me-manage koneksi.
- **Golang API**: Aplikasi sederhana (port 8080) yang melakukan insert dan query ke PgBouncer.

---

## Langkah-langkah Skenario

### Langkah 1: Inisialisasi dan Base Backup

Pertama, kita harus menjalankan semua service dan mengambil *Base Backup*. Base backup adalah fondasi dari PITR. Anda tidak bisa melakukan PITR hanya dengan file WAL; Anda butuh backup utuh pada titik tertentu.

Jalankan script pembantu:
```bash
./scripts/1_init_and_backup.sh
```

**Apa yang terjadi?**
1. `docker-compose up -d` akan menjalankan PostgreSQL, PgBouncer, dan API Golang.
2. Script akan menunggu sebentar hingga DB siap, lalu menjalankan `pg_basebackup`.
3. Backup utuh akan disimpan di `./backup/base_backup`.

### Langkah 2: Simulasi Trafik (Memasukkan Data)

Sekarang, mari kita tambahkan beberapa data melalui API Golang.

Buka terminal dan jalankan beberapa kali perintah `curl` ini:
```bash
curl -X POST http://localhost:8080/transactions \
     -H "Content-Type: application/json" \
     -d '{"amount": 100.50, "notes": "Transaksi Pertama"}'

curl -X POST http://localhost:8080/transactions \
     -H "Content-Type: application/json" \
     -d '{"amount": 250.00, "notes": "Transaksi Kedua"}'
```

Pastikan data masuk dengan melakukan GET:
```bash
curl http://localhost:8080/transactions
```

> [!IMPORTANT]
> **CATAT WAKTU SAAT INI!** 
> Waktu ini adalah **Target Recovery Time** Anda. Anda ingin data kembali persis seperti pada detik ini (misalnya `2026-08-11 16:15:00`).

### Langkah 3: Simulasi Bencana (Data Hilang)

Mari kita asumsikan beberapa menit kemudian, ada developer yang tidak sengaja menghapus tabel!

Jalankan script bencana:
```bash
./scripts/2_simulate_disaster.sh
```

Jika Anda mengecek API lagi:
```bash
curl http://localhost:8080/transactions
# Akan menghasilkan error: "relation \"transactions\" does not exist"
```
Data Anda telah hilang!

### Langkah 4: Melakukan Point-In-Time Recovery (PITR)

Sekarang kita akan melakukan proses *restore*.

Kita akan menggunakan script ke-3 dengan argumen waktu yang Anda catat pada Langkah 2 (Target Recovery Time). Format waktunya adalah `YYYY-MM-DD HH:MM:SS`. Sesuaikan dengan timezone PostgreSQL (default UTC jika di dalam kontainer). Anda dapat menyesuaikan jamnya agar mendekati titik di mana data masih ada.

```bash
# GANTI WAKTU INI DENGAN WAKTU YANG ANDA CATAT SEBELUM BENCANA!
./scripts/3_perform_pitr.sh '2026-08-11 08:15:00'
```

**Apa yang dilakukan script ini?**
1. Menghentikan kontainer database dan pgbouncer.
2. Menghapus folder `data` saat ini yang telah rusak/kehilangan tabel.
3. Menyalin isi `./backup/base_backup` kembali ke `./data`.
4. Membuat file `recovery.signal` di `./data`.
5. Menambahkan `recovery_target_time` ke `postgresql.conf`.
6. Menjalankan ulang PostgreSQL.

PostgreSQL akan membaca `recovery.signal`, lalu mulai me-*replay* file-file WAL (Write-Ahead Logs) yang ada di folder `./archive` satu per satu **HANYA SAMPAI** titik waktu yang Anda tentukan (`recovery_target_time`).

### Langkah 5: Verifikasi Hasil

Tunggu beberapa detik hingga PostgreSQL selesai melakukan recovery. Anda bisa melihat log-nya:
```bash
docker compose logs -f db
```
*(Anda akan melihat pesan "database system is ready to accept read only connections" dan kemudian "recovery ended").*

Setelah selesai, nyalakan kembali PgBouncer (jika belum berjalan):
```bash
docker compose start pgbouncer
```

Cek lagi API Golang:
```bash
curl http://localhost:8080/transactions
```

**Selamat!** Data transaksi pertama dan kedua Anda seharusnya sudah kembali, dan perintah `DROP TABLE` (bencana) tidak pernah tereksekusi pada database yang baru ini karena kita berhenti (*stop recovery*) tepat sebelum bencana itu terjadi.

---

## Pembersihan

Jika Anda sudah selesai mencoba dan ingin menghapus semuanya:
```bash
docker compose down -v
rm -rf ./data/* ./archive/* ./backup/*
```
