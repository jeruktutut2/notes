# 🐬 Panduan Lengkap MySQL Master-Replica (GTID Based)

Dokumentasi ini berisi catatan lengkap, arsitektur, panduan konfigurasi, dan skenario pengujian untuk mekanisme **MySQL Primary-Replica (Master-Replica) Replication** menggunakan **GTID (Global Transaction Identifier)** dan **Docker Compose**.

---

## 🚀 Mengapa Menggunakan Tools Ini?

1. **Docker & Docker Compose**:
   - Memungkinkan simulasi klaster multi-node (1 Master + N Replicas) di lingkungan lokal tanpa perlu instalasi MySQL berulang pada host machine.
   - Menyediakan isolasi jaringan (*bridge network*) dan penanganan container yang konsisten.

2. **MySQL 8.0+ dengan GTID (Global Transaction Identifier)**:
   - **Modern Best Practice**: Menggantikan metode legacy berbasis `master_log_file` & `master_log_pos` yang rentan kesalahan.
   - **Auto-Positioning (`SOURCE_AUTO_POSITION = 1`)**: Replica secara otomatis mendeteksi transaksi mana yang belum diterima dari Master.
   - **Failover & Scale-out Cepat**: Mempromosikan replica menjadi master atau menambah replica baru dapat dilakukan hanya dengan 1 perintah tanpa perlu mencari koordinat binlog secara manual.

---

## 📂 Struktur Project

```
master_replica/
├── config/
│   ├── master.cnf          # Konfigurasi MySQL Master (server-id=1, log-bin, GTID)
│   ├── replica1.cnf        # Konfigurasi MySQL Replica 1 (server-id=2, read_only=ON)
│   ├── replica2.cnf        # Konfigurasi MySQL Replica 2 (server-id=3, read_only=ON)
│   ├── replica3.cnf        # Konfigurasi MySQL Replica 3 (server-id=4, read_only=ON)
│   └── proxysql.cnf        # Konfigurasi ProxySQL Layer 7 Smart Query Router (Port 6033/6032)
├── app/                    # Aplikasi REST API Golang Echo v5 (Raw SQL / No ORM)
│   ├── main.go             # Entrypoint & Router Echo v5 (Port 8080)
│   ├── db/client.go        # Koneksi database/sql ke ProxySQL
│   ├── models/employee.go  # Struct & DTOs
│   └── handlers/           # REST Handlers (Insert, Select, Explicit Transaction)
├── init/
│   └── 01-master-init.sql  # Database, tabel, user replikasi (repl_user), dan seed data
├── scripts/
│   ├── 01-setup-replica1.sh # Menghubungkan Replica 1 ke Master
│   ├── 02-setup-replica2.sh # Menghubungkan Replica 2 ke Master
│   ├── 03-setup-replica3.sh # Menghubungkan Replica 3 ke Master
│   ├── test-scenario-1.sh  # Pengujian Skenario 1 (1 Master 1 Replica)
│   ├── test-scenario-2.sh  # Pengujian Skenario 2 (Failover / Master Down)
│   ├── test-scenario-3.sh  # Pengujian Skenario 3 (Scale-Out / Tambah Replica 2)
│   ├── test-scenario-4.sh  # Pengujian Skenario 4 (Progresif 1 DB Standalone -> Master -> Replica 1 -> Replica 2)
│   ├── test-scenario-5.sh  # Pengujian Skenario 5 (Progresif Complete + Failover Master & Promosi Replica)
│   ├── test-scenario-6.sh  # Pengujian Skenario 6 (Kompleks: Tahap 1-5 + DB4 Join + Failback ke DB1)
│   └── test-scenario-7.sh  # Pengujian Skenario 7 (Enterprise: ProxySQL + Golang Echo v5 REST API)
├── docker-compose.yml      # Service mysql-master, replica1..3, proxysql, golang-app
└── README.md              # Dokumentasi lengkap
```

---

## 🛠️ Detail Konfigurasi Utama

### 1. Master Configuration (`config/master.cnf`)
```ini
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog_format = ROW
gtid_mode = ON
enforce_gtid_consistency = ON
default_authentication_plugin = mysql_native_password
```

### 2. Replica Configuration (`config/replica1.cnf` & `config/replica2.cnf`)
```ini
[mysqld]
server-id = 2 # Server-id harus unik untuk tiap node (Replica 2 = 3)
log-bin = mysql-bin
binlog_format = ROW
gtid_mode = ON
enforce_gtid_consistency = ON
read_only = ON
super_read_only = ON
default_authentication_plugin = mysql_native_password
```

---

## 🧪 Skenario Pengujian

### 🟢 Skenario 1: 1 Master + 1 Replica (Select & Insert)

**Tujuan**: Membuktikan bahwa data yang di-`INSERT` pada Master tereplikasi secara real-time ke Replica 1, dan Replica 1 berada dalam mode *Read-Only*.

#### Langkah Manual / Eksekusi Script:
```bash
# 1. Start Service Master dan Replica 1
docker-compose up -d mysql-master mysql-replica1

# 2. Hubungkan Replica 1 ke Master
./scripts/01-setup-replica1.sh

# 3. Jalankan pengujian Skenario 1
./scripts/test-scenario-1.sh
```

#### Penjelasan Query Skenario 1:
- **Insert di Master**:
  ```sql
  INSERT INTO company_db.employees (name, position) VALUES ('Charlie Developer', 'Fullstack Engineer');
  ```
- **Select di Replica 1**:
  ```sql
  SELECT * FROM company_db.employees;
  ```
- **Uji Proteksi Read-Only di Replica 1**:
  ```sql
  INSERT INTO company_db.employees (name, position) VALUES ('Illegal Insert', 'Hacker');
  -- Output Error: ERROR 1290 (HY000): The MySQL server is running with the --read-only option
  ```

---

### 🔴 Skenario 2: Master OFF -> Promote Replica 1 jadi Master (Failover)

**Tujuan**: Simulasi bencana saat Master mati (*crash/down*). Replica 1 dipromosikan menjadi Master Baru (*Primary*) dan disiapkan untuk menerima lalu lintas WRITE (`INSERT`) dan READ (`SELECT`).

#### Langkah Manual / Eksekusi Script:
```bash
./scripts/test-scenario-2.sh
```

#### Langkah Perintah Internal:
1. **Matikan Master**:
   ```bash
   docker stop mysql-master
   ```
2. **Promosi Replica 1 di MySQL**:
   ```sql
   STOP REPLICA;
   RESET REPLICA ALL;
   SET GLOBAL read_only = OFF;
   SET GLOBAL super_read_only = OFF;
   ```
3. **Uji Coba Query SELECT & INSERT pada Master Baru (Replica 1)**:
   ```sql
   -- Membaca data eksisting
   SELECT * FROM company_db.employees;

   -- Menulis data baru ke Master Baru
   INSERT INTO company_db.employees (name, position) VALUES ('David Failover', 'DevOps Lead');
   ```

---

### 🔵 Skenario 3: 1 Master + 1 Replica -> Tambah 1 Replica Lagi (Scale-Out)

**Tujuan**: Menambahkan node Replica baru (`mysql-replica2`) ke klaster secara dinamis tanpa mengganggu Master yang sedang berjalan.

#### Langkah Manual / Eksekusi Script:
```bash
./scripts/test-scenario-3.sh
```

#### Langkah Perintah Internal:
1. **Jalankan Node Replica 2**:
   ```bash
   docker-compose up -d mysql-replica2
   ```
2. **Hubungkan Replica 2 ke Master via GTID**:
   ```bash
   ./scripts/02-setup-replica2.sh
   ```
3. **Uji Coba INSERT di Master & SELECT di Kedua Replica**:
   ```sql
   -- Di Master
   INSERT INTO company_db.employees (name, position) VALUES ('Eve Scaleout', 'QA Engineer');

   -- Di Replica 1
   SELECT * FROM company_db.employees;

   -- Di Replica 2
   SELECT * FROM company_db.employees;
   ```

---

### 🟡 Skenario 4: Progresif 1 DB Standalone -> Master -> Replica 1 -> Replica 2

**Tujuan**: Menguji alur bertahap (progresif) di mana aplikasi dimulai dari 1 database tunggal (DB1), kemudian dipromosikan menjadi Master, ditambahkan Replica 1 (DB2), dan kemudian ditambahkan Replica 2 (DB3).

#### Eksekusi Script:
```bash
./scripts/test-scenario-4.sh
```

#### Tahapan Skenario 4:
1. **Tahap 1**: Menyalakan DB1 (`mysql-master`) saja secara standalone, melakukan query `INSERT` & `SELECT`.
2. **Tahap 2**: Mengonfigurasi dan memeriksa status DB1 sebagai Master (GTID & `repl_user`).
3. **Tahap 3**: Menyalakan DB2 (`mysql-replica1`), mereplikasikan dari DB1, melakukan `INSERT` ke DB1, dan membuktikan data terbaca di DB1 dan DB2 via `SELECT`.
4. **Tahap 4**: Menyalakan DB3 (`mysql-replica2`), mereplikasikan dari DB1, membuktikan `SELECT` di DB1, DB2, dan DB3, kemudian melakukan `INSERT` baru di DB1, dan membuktikan hasil akhir terbaca di DB1, DB2, dan DB3.

---

### 🟣 Skenario 5: Progresif Complete + Failover Master & Promosi Replica

**Tujuan**: Menggabungkan seluruh alur progresif (Skenario 4) lalu melakukan simulasi kegagalan (*Master Down*) pada DB1, mempromosikan DB2 menjadi Master Baru, dan mengalihkan DB3 agar mereplikasi dari DB2.

#### Eksekusi Script:
```bash
./scripts/test-scenario-5.sh
```

#### Catatan Penting Mengenai Failover & Promosi:
> [!IMPORTANT]
> **Apakah proses Failover & Promosi ini Otomatis atau Manual?**
> - **Secara bawaan (Native MySQL Replication)**: Proses ini adalah **MANUAL**. MySQL standar tidak memiliki mekanisme *auto-failover* otomatis bawaan tanpa bantuan orchestrator pihak ketiga (seperti *Orchestrator*, *ProxySQL*, *MHA*, atau *MySQL InnoDB Cluster*).
> - **Langkah Manual yang Dieksekusi**:
>   1. Mematikan DB1 (`docker stop mysql-master`).
>   2. Mempromosikan DB2 (`mysql-replica1`) menjadi Master Baru dengan menghentikan replikasinya (`STOP REPLICA; RESET REPLICA ALL;`) dan mematikan mode Read-Only (`SET GLOBAL read_only = OFF; SET GLOBAL super_read_only = OFF;`).
>   3. Menyiapkan akun `repl_user` di DB2.
>   4. Mengarahkan DB3 (`mysql-replica2`) agar mendownload log transaksi dari Master Baru (`mysql-replica1`).

#### Tahapan Skenario 5:
1. **Tahap 1 s/d 4**: Membangun lingkungan progresif (DB1 Standalone -> DB1 Master -> DB2 Replica -> DB3 Replica) dan menguji penguncian Read-Only.
2. **Tahap 5 (Failover)**:
   - Mematikan DB1 (`mysql-master`).
   - Promosi DB2 (`mysql-replica1`) menjadi **Master Baru**.
   - Mengalihkan DB3 (`mysql-replica2`) agar mereplikasi dari DB2.
   - Melakukan `SELECT` di semua DB yang hidup (DB2 & DB3) sebelum INSERT.
   - Melakukan `INSERT` data baru pada **Master Baru (DB2)**.
   - Melakukan `SELECT` kembali di DB2 & DB3 untuk membuktikan data baru tereplikasi secara real-time dari DB2 ke DB3.

---

### 🔴 Skenario 6: Kompleks (Progresif + Failover + DB4 Join + Failback ke DB1)

**Tujuan**: Menguji alur lengkap end-to-end dari penyiapan 1 DB Standalone, promosi Master, replikasi ke DB2 & DB3, simulasi Failover ke DB2, penambahan node DB4 (`mysql-replica3`), hingga prosedur **Failback** mengembalikan DB1 yang baru pulih sebagai Primary Master secara aman tanpa kehilangan data.

#### Eksekusi Script:
```bash
./scripts/test-scenario-6.sh
```

#### Catatan Prosedur Failback (Pemulihan DB1 Kembali Menjadi Master):
> [!NOTE]
> **Langkah Failback Bertahap:**
> 1. **Re-integrasi DB1 sebagai Replica Sementara dari DB2**:
>    DB1 dinyalakan kembali, lalu disambungkan sebagai Replica dari DB2 (`SOURCE_AUTO_POSITION = 1`). GTID secara otomatis menyerap seluruh transaksi baru yang terjadi saat DB1 sedang mati.
> 2. **Kunci Penulisan pada DB2**:
>    Mengunci DB2 (`read_only = ON`) agar tidak ada data baru yang masuk saat transisi.
> 3. **Promosi DB1 Menjadi Primary Master Kembali**:
>    Menghentikan replikasi DB1 dan membuka akses *Write* (`read_only = OFF`).
> 4. **Dialihkan Seluruh Replica ke DB1**:
>    DB2, DB3, dan DB4 dialihkan kembali agar mengekor ke DB1 (`mysql-master`).

#### Tahapan Skenario 6:
1. **Tahap 1 s/d 5**: Menjalankan alur progresif awal dan simulasi Failover (DB1 mati, DB2 jadi Master Baru, DB3 mengekor DB2).
2. **Tahap 6 (Join DB4)**: Menyalakan DB4 (`mysql-replica3`), mereplikasikan ke DB2, melakukan `INSERT` ke DB2, dan memverifikasi `SELECT` di DB2, DB3, dan DB4.
3. **Tahap 7 (Failback ke DB1)**: Menyalakan kembali DB1, re-integrasi DB1 sebagai replica dari DB2 untuk sync data via GTID, mempromosikan DB1 kembali menjadi Primary Master, dan mengarahkan DB2, DB3, DB4 ke DB1.
4. **Tahap 8 (Verifikasi Akhir)**: Melakukan `INSERT` ke DB1 (Primary Master) dan memverifikasi data terbaru tersinkronisasi ke seluruh 4 database (DB1, DB2, DB3, DB4).

---

### 🌐 SkenARIO 7: Enterprise Architecture (ProxySQL + Golang Echo v5 REST API)

**Tujuan**: Menguji arsitektur enterprise lengkap dengan **Golang Echo v5 REST API** yang terhubung ke **ProxySQL (Port 6033)** untuk penanganan *Smart Query Routing*, *Explicit Transactions*, *Failover*, dan *Failback* tanpa ORM.

#### Eksekusi Script:
```bash
./scripts/test-scenario-7.sh
```

#### Endpoint REST API Golang Echo v5 (`http://localhost:8080`):
- `GET /api/health` -> Status kesehatan API & koneksi DB.
- `GET /api/employees` -> **Select Biasa** (Di-routing otomatis oleh ProxySQL ke Replicas).
- `POST /api/employees` -> **Insert Biasa** (Di-routing otomatis oleh ProxySQL ke Master).
- `POST /api/employees/transaction` -> **Explicit Transaction (`db.BeginTx()`)** (Seluruh `SELECT` & `INSERT` di dalam transaksi otomatis dikunci ke Master).

---

### 📘 CATATAN ARSITEKTUR & MANAJEMEN PROXYSQL

> [!NOTE]
> **1. Arsitektur 2 Port ProxySQL & Database SQLite Internal**
> - **Apakah perlu install SQLite lagi secara terpisah?** -> **TIDAK PERLU.** Engine SQLite sudah **tertanam (*embedded/built-in*)** secara otomatis di dalam biner ProxySQL.
> - **Bagaimana cara mengakses Database SQLite internal ProxySQL tersebut?**
>   ProxySQL menyediakan antarmuka berprotokol MySQL di **Port 6032**. Anda cukup menggunakan perintah client `mysql` biasa ke Port `6032`:
>   ```bash
>   mysql -uadmin -padmin -h127.0.0.1 -P6032
>   # Atau via docker container:
>   docker exec -it proxysql mysql -uadmin -padmin -h127.0.0.1 -P6032
>   ```
> - **Port 6033 (Data Port)**: Pintu koneksi aplikasi (Golang/Backend). ProxySQL menerima query SQL biasa dari aplikasi dan meneruskannya ke MySQL Cluster.
> - **Port 6032 (Admin Port)**: Pintu manajemen internal ProxySQL berbasis database SQLite internal. Tempat administrator mengeksekusi query konfigurasi internal (User: `admin`, Pass: `admin`).

> [!IMPORTANT]
> **2. Arsitektur 3-Tier Dynamic Configuration (Zero-Downtime)**
> ProxySQL **tidak memerlukan restart** atau edit file `proxysql.cnf` saat menambahkan/menghapus node database secara live di production:
> 1. **RUNTIME (Memory)**: Konfigurasi yang sedang aktif melayani query saat ini.
> 2. **DISK (SQLite DB `/var/lib/proxysql/proxysql.db`)**: Tempat penyimpanan konfigurasi secara permanen.
> 3. **CONFIG FILE (`proxysql.cnf`)**: Hanya dibaca saat ProxySQL di-boot pertama kali dari kondisi kosong (*bootstrap*).

> [!TIP]
> **3. Cara Menambah Node DB Baru Secara Live di Production (Via Admin Port 6032)**
> ```sql
> -- Masuk ke Admin Interface ProxySQL CLI (Port 6032):
> mysql -uadmin -padmin -h127.0.0.1 -P6032
>
> -- A. Masukkan node DB baru ke Hostgroup 20 (Read Replicas):
> INSERT INTO mysql_servers (hostgroup_id, hostname, port, max_connections) 
> VALUES (20, 'mysql-replica4', 3306, 200);
>
> -- B. Terapkan secara instan ke RUNTIME (Langsung melayani query saat itu juga):
> LOAD MYSQL SERVERS TO RUNTIME;
>
> -- C. Simpan permanen ke DISK (agar tidak hilang jika container ProxySQL di-restart):
> SAVE MYSQL SERVERS TO DISK;
> ```

---

## 🔍 Perintah Debugging & Monitoring Paling Penting

1. **Cek Status Replikasi di Replica**:
   ```sql
   SHOW REPLICA STATUS\G;
   ```
   *Indikator Penting:*
   - `Replica_IO_Running: Yes`
   - `Replica_SQL_Running: Yes`
   - `Seconds_Behind_Master: 0`

2. **Cek Transaction GTID**:
   ```sql
   SHOW MASTER STATUS\G; -- Di Master
   SELECT @@global.gtid_executed; -- Di Node mana saja
   ```

3. **Cek Status Read Only**:
   ```sql
   SELECT @@global.read_only, @@global.super_read_only;
   ```
