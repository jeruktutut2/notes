# Panduan High Availability: Streaming Replication, Failover, dan Failback

Panduan ini adalah kelanjutan dari skenario PITR. Di sini kita akan menambahkan node **Replica** dan mempraktikkan proses kegagalan (Failover) dan pemulihan node (Failback) menggunakan `pg_rewind`.

## Langkah-langkah Skenario

### Langkah 1: Persiapan Awal
Pastikan Anda sudah menjalankan script `1_init_and_backup.sh` sebelumnya dan memiliki beberapa data. Jika belum, jalankan:
```bash
./scripts/1_init_and_backup.sh
```

### Langkah 2: Setup Streaming Replication
Kita akan menggunakan `pg_basebackup` untuk menduplikasi Primary saat ini ke node Replica, lalu menyalakannya.
Jalankan:
```bash
./scripts/4_setup_replication.sh
```
**Validasi:** Anda akan melihat `sync_state` = `async` (atau `sync`) dan output JSON dari API Golang yang menampilkan data awal Anda.

### Langkah 3: Simulasi Bencana (Primary Mati) & Failover
Tiba-tiba server Primary Anda (`pitr_postgres`) mengalami kerusakan hardware dan mati (disimulasikan dengan `docker compose stop db`).

Kita harus mengarahkan trafik aplikasi ke Replica secepat mungkin.
Jalankan:
```bash
./scripts/5_failover.sh
```
**Apa yang terjadi?**
1. Replica (`pitr_replica`) dipromosikan menjadi Primary baru menggunakan `pg_ctl promote`.
2. PgBouncer dikonfigurasi ulang untuk menunjuk ke IP/Hostname Primary yang baru.
3. Script akan otomatis memasukkan data baru (Transaksi Pasca Failover) melalui API dan menampilkannya, membuktikan aplikasi kembali normal dan menunjuk ke database yang benar.

### Langkah 4: Failback (Resync Primary Lama)
Server lama Anda sudah diperbaiki. Namun datanya sekarang sudah tertinggal (dan posisinya sebelumnya adalah Primary). Anda tidak bisa langsung menyalakannya, karena akan terjadi *Split-Brain*.

Kita akan menggunakan `pg_rewind` untuk menarik log/data yang berubah dari Primary Baru (`pitr_replica`) ke server lama (`pitr_postgres`), lalu menyalakannya sebagai Standby (Replica).

Jalankan:
```bash
./scripts/6_failback.sh
```
**Apa yang terjadi?**
1. `pg_rewind` dijalankan untuk mensinkronisasi data.
2. File `standby.signal` dibuat di folder server lama.
3. Node lama dinyalakan.
4. Script akan mencoba *SELECT* dari Standby untuk membuktikan data baru sudah ada.
5. Script akan melakukan *INSERT* data baru di Primary, dan membuktikan data tersebut otomatis muncul di Standby!

> [!TIP]
> Dengan menggunakan `pg_rewind`, Anda menghemat sangat banyak waktu karena tidak perlu melakukan `pg_basebackup` dari awal (yang bisa berukuran ratusan GB atau TB di dunia nyata).
