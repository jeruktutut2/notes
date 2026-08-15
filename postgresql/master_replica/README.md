# PostgreSQL Enterprise High Availability Cluster dengan Patroni, etcd, HAProxy & PgBouncer

Proyek ini menyediakan arsitektur **PostgreSQL Enterprise High Availability & Read-Replication** modern menggunakan **Patroni**, **etcd**, **HAProxy**, **PgBouncer**, dan **Golang Echo v5 API**.

---

## 🏗️ Topologi & Arsitektur Lengkap

```
                               +------------------------+
                               |   Golang Echo Backend  |
                               |      (Port 8080)       |
                               +-----------+------------+
                                           |
                                        PgBouncer
                                       (Port 6432)
                                           |
                   +-----------------------+-----------------------+
                   | (db_write)                                    | (db_read)
                   v                                               v
           +---------------+                               +---------------+
           | HAProxy:5000  |                               | HAProxy:5001  |
           | (Write Front) |                               |  (Read Front) |
           +-------+-------+                               +-------+-------+
                   | (HTTP Check GET /primary)                     | (HTTP Check GET /replica)
                   v                                               v
    +------------------------------+             +----------------------------------+
    |  postgres_node1 (Leader)     |             |  postgres_node2 / node3 / node4  |
    |  (Patroni + Postgres:5432)   |             |  (Patroni + Postgres:5432)       |
    +--------------+---------------+             +-----------------+----------------+
                   |                                               |
                   +-----------------------+-----------------------+
                                           |
                               +-----------v------------+
                               |   etcd (DCS: 2379)     |
                               | (Cluster Leader State) |
                               +------------------------+
```

### ✨ Fitur Utama Patroni Cluster:
1. **Automated Failover**: Ketika Primary/Leader server mati, Patroni & etcd secara otomatis memilih Leader baru (misal `postgres_node2`) dalam kurun waktu **5-10 detik**.
2. **Dynamic HAProxy Routing**: HAProxy menggunakan HTTP health check Patroni (`GET /primary` di Port 8008). HAProxy secara otomatis mengarahkan trafik *WRITE* ke mana pun Primary server berada tanpa mengubah konfigurasi `haproxy.cfg`.
3. **Zero Manual Scripting**: Tidak memerlukan perintah `pg_promote()` manual, edit file konfigurasi manual, atau restart container saat terjadi failover.

---

## 📁 Struktur Direktori & File

| File / Folder | Deskripsi |
| :--- | :--- |
| [`docker-compose.yml`](file:///Users/bsa/Documents/por/postgresql/master_replica/docker-compose.yml) | Definisi service container: `etcd`, Patroni Postgres nodes (`postgres_node1`, `postgres_node2`, `postgres_node3`, `postgres_node4`), `haproxy`, `pgbouncer`, dan `app_echo`. |
| [`Dockerfile.patroni`](file:///Users/bsa/Documents/por/postgresql/master_replica/Dockerfile.patroni) | Build Docker image PostgreSQL 15 dengan `patroni` & `psycopg2`. |
| [`config/patroni/patroni.yml.template`](file:///Users/bsa/Documents/por/postgresql/master_replica/config/patroni/patroni.yml.template) | Templat konfigurasi Patroni (etcd endpoint, auto init SQL, REST API port 8008). |
| [`config/haproxy/haproxy.cfg`](file:///Users/bsa/Documents/por/postgresql/master_replica/config/haproxy/haproxy.cfg) | Konfigurasi HAProxy Load Balancer dengan Patroni HTTP Check (`/primary` port 5000, `/replica` port 5001). |
| [`config/pgbouncer/pgbouncer.ini`](file:///Users/bsa/Documents/por/postgresql/master_replica/config/pgbouncer/pgbouncer.ini) | Konfigurasi PgBouncer connection pool (`db_write` -> `haproxy:5000`, `db_read` -> `haproxy:5001`). |
| [`main.go`](file:///Users/bsa/Documents/por/postgresql/master_replica/main.go) & [`Dockerfile`](file:///Users/bsa/Documents/por/postgresql/master_replica/Dockerfile) | Aplikasi backend Golang Echo v5 dengan endpoint `/api/users` (POST/GET) dan `/api/status`. |
| [`scenario_1_basic.sh`](file:///Users/bsa/Documents/por/postgresql/master_replica/scenario_1_basic.sh) | Skenario 1: Spin up cluster Patroni + etcd, cek status cluster via `patronictl`, HAProxy stats UI, & API. |
| [`scenario_2_failover.sh`](file:///Users/bsa/Documents/por/postgresql/master_replica/scenario_2_failover.sh) | Skenario 2: **Automated Failover**. Mematikan Node 1, Patroni + etcd otomatis promote Leader baru, HAProxy otomatis route traffic WRITE tanpa intervensi manual. |
| [`scenario_3_add_replica.sh`](file:///Users/bsa/Documents/por/postgresql/master_replica/scenario_3_add_replica.sh) | Skenario 3: Dynamic Scale Out Node ke-4 (`postgres_node4`) via Patroni. |
| [`scenario_playground.sh`](file:///Users/bsa/Documents/por/postgresql/master_replica/scenario_playground.sh) | Skenario Playground: Tempat uji coba & eksperimen bebas (Insert/Select via Direct DB1 & Golang Echo API). |
| [`scenario_clean.sh`](file:///Users/bsa/Documents/por/postgresql/master_replica/scenario_clean.sh) | Skenario Cleanup: Menghentikan semua container, etcd data, & volume persistent. |

---

## 🚀 Panduan Eksekusi Langkah demi Langkah

### Skenario 1: Cluster Inisialisasi & Basic Read/Write Routing

```bash
cd /Users/bsa/Documents/por/postgresql/master_replica
./scenario_1_basic.sh
```

---

### Skenario 2: Automated Patroni Failover Test

```bash
./scenario_2_failover.sh
```

---

### Skenario 3: Dynamic Scale Out Node ke-4

```bash
./scenario_3_add_replica.sh
```

---

### Skenario Cleanup: Membersihkan Total Cluster, etcd & Volume Data

```bash
./scenario_clean.sh
```

---

## 🛠️ Perintah Debugging Useful

| Tujuan | Perintah |
| :--- | :--- |
| Dashboard Web HAProxy | Buka `http://localhost:7000` di browser |
| Cek Status Cluster Patroni | `docker compose exec postgres_node1 patronictl -c /tmp/patroni.yml list` |
| Cek REST API Patroni | `curl http://localhost:8008/cluster` |
| Cek Log HAProxy | `docker compose logs -f haproxy` |
| Cek Log Node 1 | `docker compose logs -f postgres_node1` |
