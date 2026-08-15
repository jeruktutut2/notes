# 🐬 Enterprise MySQL Master-Replica GTID dengan Orchestrator, ProxySQL & HAProxy

Dokumentasi ini berisi arsitektur, panduan konfigurasi, dan skenario pengujian lengkap untuk mekanisme **MySQL Primary-Replica (Master-Replica) Replication** menggunakan **GTID (Global Transaction Identifier)**, **Orchestrator** (Topology & Automatic Failover Management), **ProxySQL** (Layer 7 Smart Query Routing & R/W Splitting), **HAProxy** (Layer 4 Load Balancer Entry Point), dan **Golang Echo v5 REST API**.

---

## 🏗️ Arsitektur Sistem Enterprise

```
                       [ Client / Golang REST API (Port 8080) ]
                                          │
                                          ▼
                [ HAProxy Load Balancer (Port 3306) | Stats (Port 8404) ]
                                          │
                                          ▼
                   [ ProxySQL Smart Query Router (Port 6033/6032) ]
                       │                                  │
          (Hostgroup 10: Writer)               (Hostgroup 20: Readers)
                       │                                  │
                       ▼                                  ▼
             ┌──────────────────┐               ┌──────────────────┐
             │   mysql-master   │               │  mysql-replica1  │
             │   (Port 3306)    │               │   (Port 3307)    │
             └────────┬─────────┘               └────────┬─────────┘
                      │                                  │
                      ├──────────────────────────────────┼─────────────────────────┐
                      ▼                                  ▼                         ▼
             ┌──────────────────┐               ┌──────────────────┐     ┌──────────────────┐
             │  mysql-replica2  │               │  mysql-replica3  │     │   Orchestrator   │
             │   (Port 3308)    │               │   (Port 3309)    │     │   (Port 3000)    │
             └──────────────────┘               └──────────────────┘     └──────────────────┘
```

### Komponen Utama:
1. **HAProxy** (`Port 3306` Data, `Port 8404` Stats GUI):
   - Bertindak sebagai single entry point Layer 4 Load Balancer untuk aplikasi.
   - Mengisolasikan infrastruktur database dari aplikasi client dan mendistribusikan lalu lintas secara teratur ke ProxySQL.
2. **ProxySQL** (`Port 6033` Data, `Port 6032` Admin CLI):
   - Smart Layer 7 Query Router yang memisahkan lalu lintas Read dan Write secara otomatis.
   - Hostgroup `10` dialokasikan untuk Primary Master (Write), dan Hostgroup `20` untuk Replicas (Read).
3. **Orchestrator** (`Port 3000` Web GUI & REST API):
   - Layanan manajemen topologi dan otomatisasi failover berbasis GTID.
   - Memantau kesehatan node database secara real-time. Jika Primary Master mengalami crash (`DeadMaster`), Orchestrator akan mempromosikan replika yang paling mutakhir secara otomatis tanpa kehilangan data.
4. **MySQL 8.0 Cluster dengan GTID**:
   - Replikasi mutakhir menggunakan `SOURCE_AUTO_POSITION = 1`.
   - Node: `mysql-master`, `mysql-replica1`, `mysql-replica2`, `mysql-replica3`.
5. **Golang Echo v5 REST API** (`Port 8080`):
   - REST API yang terhubung ke database via HAProxy.

---

## 📂 Struktur Directory Project

```
orchestrator_proxysql_haproxy/
├── config/
│   ├── master.cnf              # Konfigurasi MySQL Master (server-id=1, GTID)
│   ├── replica1.cnf            # Konfigurasi MySQL Replica 1 (server-id=2, read_only=ON)
│   ├── replica2.cnf            # Konfigurasi MySQL Replica 2 (server-id=3, read_only=ON)
│   ├── replica3.cnf            # Konfigurasi MySQL Replica 3 (server-id=4, read_only=ON)
│   ├── orchestrator.json       # Konfigurasi Orchestrator (Backend SQLite, GTID topology)
│   ├── proxysql.cnf            # Konfigurasi ProxySQL Layer 7 Router & Hostgroups
│   └── haproxy.cfg             # Konfigurasi HAProxy L4 Load Balancer & Stats
├── app/                        # Aplikasi REST API Golang Echo v5
│   ├── Dockerfile
│   ├── go.mod
│   ├── go.sum
│   ├── main.go                 # Entrypoint Echo v5 (Port 8080)
│   ├── db/client.go            # Koneksi database/sql ke HAProxy (Port 3306)
│   ├── models/employee.go      # Struct & DTOs
│   └── handlers/
│       └── employee_handler.go # REST API Handlers (GET, POST, Transaction)
├── init/
│   └── 01-master-init.sql      # Schema, seed data, user replikasi & user orchestrator
├── scripts/
│   ├── 01-setup-replica1.sh    # Menghubungkan Replica 1 ke Master
│   ├── 02-setup-replica2.sh    # Menghubungkan Replica 2 ke Master
│   ├── 03-setup-replica3.sh    # Menghubungkan Replica 3 ke Master
│   ├── 04-register-orchestrator.sh # Menghubungkan topologi ke Orchestrator
│   ├── test-scenario-1.sh      # Skenario 1: 1 Master 1 Replica (HAProxy + ProxySQL)
│   ├── test-scenario-2.sh      # Skenario 2: Master Failover (Orchestrator & ProxySQL)
│   ├── test-scenario-3.sh      # Skenario 3: Scale-Out (Tambah Replica 2 & Orchestrator)
│   ├── test-scenario-4.sh      # Skenario 4: Progresif 1 DB Standalone -> Master -> Replica 1 -> Replica 2
│   ├── test-scenario-5.sh      # Skenario 5: Progresif Complete + Failover Master via Orchestrator
│   ├── test-scenario-6.sh      # Skenario 6: Kompleks (Failover -> Replica 3 Join -> Failback ke Master Original)
│   └── test-scenario-7.sh      # Skenario 7: Enterprise Architecture Complete (HAProxy + ProxySQL + Orchestrator + API)
├── docker-compose.yml          # Definisikan 8 Service (mysql x4, orchestrator, proxysql, haproxy, golang-app)
└── README.md                  # Dokumentasi lengkap
```

---

## 🛠️ Detail Konfigurasi Layanan

### 1. MySQL Master (`config/master.cnf`)
```ini
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog_format = ROW
gtid_mode = ON
enforce_gtid_consistency = ON
default_authentication_plugin = mysql_native_password
```

### 2. MySQL Replicas (`config/replica1.cnf`, `replica2.cnf`, `replica3.cnf`)
```ini
[mysqld]
server-id = 2 # Unik untuk setiap node (Replica 2 = 3, Replica 3 = 4)
log-bin = mysql-bin
binlog_format = ROW
gtid_mode = ON
enforce_gtid_consistency = ON
read_only = ON
super_read_only = ON
default_authentication_plugin = mysql_native_password
```

### 3. Orchestrator (`config/orchestrator.json`)
```json
{
  "Debug": true,
  "ListenAddress": ":3000",
  "MySQLTopologyUser": "orc_client",
  "MySQLTopologyPassword": "orc_password",
  "BackendDB": "sqlite3",
  "SQLite3DataFile": "/var/lib/orchestrator/orchestrator.sqlite",
  "DiscoverByShowSlaveHosts": true,
  "ApplyMySQLPromotionAfterMasterFailover": true,
  "RecoverMasterCluster": true
}
```

### 4. ProxySQL (`config/proxysql.cnf`)
```cnf
mysql_servers =
(
    { hostgroup_id=10, hostname="mysql-master", port=3306, max_connections=200 },
    { hostgroup_id=20, hostname="mysql-replica1", port=3306, max_connections=200 },
    { hostgroup_id=20, hostname="mysql-replica2", port=3306, max_connections=200 }
)
```

### 5. HAProxy (`config/haproxy.cfg`)
```haproxy
frontend mysql-frontend
    bind *:3306
    mode tcp
    default_backend proxysql-backend

backend proxysql-backend
    mode tcp
    balance roundrobin
    option tcp-check
    server proxysql1 proxysql:6033 check inter 2s fall 3 rise 2

frontend stats
    mode http
    bind *:8404
    stats enable
    stats uri /stats
```

---

## 🧪 Skenario Pengujian

### 🟢 Skenario 1: 1 Master + 1 Replica (HAProxy + ProxySQL + Orchestrator)
Menguji replikasi dasar, pengintegrasian topologi ke Orchestrator, dan pemutaran query via HAProxy & ProxySQL.
```bash
./scripts/test-scenario-1.sh
```

---

### 🔴 Skenario 2: Failover Master Dikelola oleh Orchestrator & ProxySQL
Mematikan Master utama (`mysql-master`), lalu Orchestrator secara otomatis/terpandu mempromosikan `mysql-replica1` menjadi Master Baru, dan ProxySQL mengarahkan lalulintas WRITE ke Master Baru.
```bash
./scripts/test-scenario-2.sh
```

---

### 🔵 Skenario 3: Scale-Out (1 Master + 2 Replicas + Orchestrator)
Menambahkan node `mysql-replica2` ke dalam klaster, yang langsung terdeteksi oleh Orchestrator dan didaftarkan di ProxySQL Reader Hostgroup.
```bash
./scripts/test-scenario-3.sh
```

---

### 🟡 Skenario 4: Progresif 1 DB Standalone -> Master -> Replica 1 -> Replica 2
Menguji alur pembentukan klaster secara bertahap mulai dari 1 database tunggal hingga menjadi klaster multi-replica.
```bash
./scripts/test-scenario-4.sh
```

---

### 🟣 Skenario 5: Progresif Complete + Failover Master via Orchestrator
Menggabungkan alur bertahap dari Skenario 4, dilanjutkan dengan simulasi crash Master dan promosi otomatis oleh Orchestrator.
```bash
./scripts/test-scenario-5.sh
```

---

### 🟠 Skenario 6: Kompleks (Failover -> Replica 3 Join -> Failback ke Master Original)
Menguji skenario bencana lengkap: Failover ke DB2, penambahan DB4 (`mysql-replica3`), diikuti proses **Failback** untuk memulihkan DB1 kembali sebagai Primary Master.
```bash
./scripts/test-scenario-6.sh
```

---

### 🚀 Skenario 7: Enterprise Integration Complete (HAProxy + ProxySQL + Orchestrator + Golang REST API)
Pengujian end-to-end lengkap dari REST API Golang Echo v5 melalui HAProxy, ProxySQL, Orchestrator, hingga database MySQL GTID beserta uji coba failover & failback live.
```bash
./scripts/test-scenario-7.sh
```

---

## 📊 Akses Dashboard & Command Useful

- **Orchestrator Web GUI**: `http://localhost:3000`
- **HAProxy Stats Dashboard**: `http://localhost:8404/stats`
- **Golang REST API Healthcheck**: `http://localhost:8080/api/health`
- **ProxySQL Admin CLI**:
  ```bash
  docker exec -it proxysql mysql -uadmin -padmin -h127.0.0.1 -P6032
  ```
- **Orchestrator Topology API**:
  ```bash
  curl -s http://localhost:3000/api/topology-tabulated
  ```
