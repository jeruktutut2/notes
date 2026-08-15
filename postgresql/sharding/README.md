# PostgreSQL Sharding Architecture dengan Citus Data, PgBouncer & Golang Echo

Repositori ini berisi solusi lengkap **PostgreSQL Database Sharding** menggunakan **Citus Data Extension**, dikombinasikan dengan **PgBouncer** (Connection Pooler) dan **Golang Echo REST API** (`Echo v5`).

---

## 🏗️ Arsitektur Sistem

```
                         [ Client / Golang Echo API ]
                                     │
                                     ▼ (Port 6432)
                               [ PgBouncer ]
                                     │
                                     ▼ (Port 5432)
                          [ Citus Coordinator Node ]
                                     │
        ┌───────────────┬────────────┼───────────────┬───────────────┐
        ▼               ▼            ▼               ▼               ▼
   [ Worker 1 ]   [ Worker 2 ]  [ Worker 3 ]   [ Worker 4 ]    [ Worker 5 ]
   (DB Shard 1)   (DB Shard 2)  (DB Shard 3)   (DB Shard 4)    (DB Shard 5)
```

---

## 🚀 Cara Memulai (Quick Start)

### 1. Jalankan Cluster (1 Coordinator + Worker Nodes + PgBouncer + API)

```bash
docker compose up -d
```

Periksa status kluster:
```bash
./scripts/check-shards.sh
```

---

## 📊 Skenario Horizontal Scaling (Scale-Up 1 s.d. 5 DB)

Gunakan skrip terautomasi [`scripts/scale-scenario.sh`](file:///Users/bsa/Documents/por/postgresql/sharding/scripts/scale-scenario.sh):

```bash
./scripts/scale-scenario.sh 1   # 1 Worker DB
./scripts/scale-scenario.sh 2   # 2 Worker DB
./scripts/scale-scenario.sh 3   # 3 Worker DB
./scripts/scale-scenario.sh 4   # 4 Worker DB
./scripts/scale-scenario.sh 5   # 5 Worker DB
```

---

## 🔻 Skenario Scale-Down (Jika Jumlah DB Berkurang)

Pengurangan simpul DB dilakukan dengan evakuasi pecahan data secara live (*Zero Data Loss*):

```bash
# Evakuasi shard dari worker5 ke worker lainnya lalu hapus worker5
./scripts/scale-down.sh worker5
```

---

## 🌐 Testing Golang Echo REST API (Echo v5)

### 1. Nambah Data (POST Single User) + Informasi Simpul DB Target
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"Siti Aminah","email":"siti@example.com","country":"Indonesia"}' \
  http://localhost:8080/users
```
**Response JSON:**
```json
{
  "data": {
    "id": 601,
    "name": "Siti Aminah",
    "email": "siti@example.com",
    "country": "Indonesia",
    "stored_in_db_node": "worker3",
    "shard_id": 102022
  },
  "message": "User data successfully added to sharded database",
  "sharding_info": {
    "distribution_key": "id",
    "distribution_val": 601,
    "shard_id": 102022,
    "stored_in_db_node": "worker3"
  }
}
```

### 2. Select Data Single User (GET /users/:id) + Informasi Simpul DB Asal
```bash
curl http://localhost:8080/users/601
```
**Response JSON:**
```json
{
  "user": {
    "id": 601,
    "name": "Siti Aminah",
    "email": "siti@example.com",
    "country": "Indonesia",
    "stored_in_db_node": "worker3",
    "shard_id": 102022
  },
  "orders": null,
  "sharding_info": {
    "fetched_from_db_node": "worker3",
    "shard_id": 102022
  }
}
```

### 3. Select List Users (GET /users)
```bash
curl "http://localhost:8080/users?limit=5"
```

### 4. Bulk Seed Data
```bash
curl -X POST "http://localhost:8080/seed?count=500"
```

### 5. Analytics Query Terdistribusi
```bash
curl http://localhost:8080/analytics
```
