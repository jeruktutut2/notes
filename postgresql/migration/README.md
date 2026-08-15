# 📦 Panduan Lengkap Database Migration
## Golang Echo v5 + PgBouncer + PostgreSQL

---

## 📖 Daftar Isi

- [Apa itu Database Migration?](#apa-itu-database-migration)
- [Arsitektur Proyek](#arsitektur-proyek)
- [Mengapa PgBouncer?](#mengapa-pgbouncer)
- [Struktur Proyek](#struktur-proyek)
- [Cara Menjalankan](#cara-menjalankan)
- [Penjelasan Migration Files](#penjelasan-migration-files)
- [Perintah Migration](#perintah-migration)
- [API Endpoints](#api-endpoints)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Apa itu Database Migration?

**Database Migration** adalah teknik untuk mengelola perubahan skema database secara terstruktur dan terlacak (versioned). Bayangkan seperti "Git untuk database" — setiap perubahan dicatat dalam file terpisah, bisa di-apply (up) atau di-rollback (down).

### Kenapa Perlu Migration?

| Tanpa Migration | Dengan Migration |
|:---|:---|
| Perubahan database manual via SQL langsung | Perubahan terdokumentasi dalam file |
| Tidak tahu siapa mengubah apa | Setiap perubahan bisa di-review via Git |
| Sulit rollback jika ada error | Rollback otomatis dengan `migrate down` |
| Tim dev bisa punya skema yang berbeda | Semua dev punya skema yang sama |
| Deployment manual dan rawan error | Deployment otomatis dan konsisten |

### Konsep Dasar

```
Versi 0 (kosong)
    │
    ▼  000001_create_users_table.up.sql
Versi 1 (tabel users ada)
    │
    ▼  000002_add_email_to_users.up.sql
Versi 2 (kolom email ditambahkan)
    │
    ▼  000003_create_products_table.up.sql
Versi 3 (tabel products ada)
    │
    ▼  ... dan seterusnya
```

Setiap migration punya **2 file**:
- **`.up.sql`** — SQL untuk menerapkan perubahan (maju)
- **`.down.sql`** — SQL untuk membatalkan perubahan (mundur/rollback)

---

## Arsitektur Proyek

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Go App        │────▶│   PgBouncer     │────▶│   PostgreSQL    │
│   (Echo v5)     │     │   (port 6432)   │     │   (port 5432)   │
│                 │     │                 │     │                 │
│   port 8080     │     │   Connection    │     │   Database      │
│                 │     │   Pooler        │     │   Server        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                       ▲
┌─────────────────┐                                    │
│   migrate CLI   │────────────────────────────────────┘
│   (langsung!)   │    ⚠️ BYPASS PgBouncer
└─────────────────┘
```

### Alur Koneksi

1. **Aplikasi** → PgBouncer (port 6432) → PostgreSQL (port 5432)
   - Untuk operasi CRUD normal
   - Mendapat benefit connection pooling

2. **Migration** → PostgreSQL (port 5432) langsung
   - HARUS bypass PgBouncer
   - Karena migration menggunakan **advisory lock** yang tidak kompatibel dengan PgBouncer mode transaction

---

## Mengapa PgBouncer?

### Masalah Tanpa PgBouncer

PostgreSQL membuat **1 proses untuk setiap koneksi**. Jika ada 100 user simultaneous:
- 100 proses PostgreSQL berjalan
- Setiap proses ~10MB RAM
- Total: ~1GB RAM hanya untuk koneksi!

### Solusi dengan PgBouncer

PgBouncer bertindak sebagai **proxy** antara aplikasi dan PostgreSQL:

```
200 koneksi client  →  PgBouncer  →  20 koneksi ke PostgreSQL
(dari aplikasi)        (pooler)      (sangat efisien!)
```

### Mode Pool

| Mode | Kapan Koneksi Dikembalikan | Use Case |
|:---|:---|:---|
| **session** | Saat client disconnect | Legacy app |
| **transaction** ⭐ | Setelah transaksi selesai | Web app (recommended!) |
| **statement** | Setelah setiap SQL statement | Sangat restrictive |

### ⚠️ PgBouncer & Migration

**PENTING**: Migration tool (golang-migrate) menggunakan `pg_advisory_lock` untuk mencegah race condition. Advisory lock ini **TIDAK KOMPATIBEL** dengan PgBouncer mode `transaction` karena:

1. Advisory lock terikat pada **session** (koneksi fisik)
2. Di mode transaction, koneksi fisik bisa berubah antar transaksi
3. Lock bisa "hilang" saat koneksi dikembalikan ke pool

**Solusi**: Migration CLI harus terhubung **langsung ke PostgreSQL** (port 5432), bukan melalui PgBouncer (port 6432).

---

## Struktur Proyek

```
migration/
├── cmd/
│   └── api/
│       └── main.go                  # Entry point: Echo v5 server
├── internal/
│   ├── config/
│   │   └── config.go                # Konfigurasi dari env vars
│   ├── database/
│   │   └── database.go              # Koneksi DB + auto-migration
│   ├── handler/
│   │   └── user_handler.go          # HTTP handlers (CRUD)
│   ├── model/
│   │   └── user.go                  # Struct & DTO
│   └── repository/
│       └── user_repository.go       # Query database
├── migrations/
│   ├── embed.go                     # Embed SQL ke Go binary
│   ├── sql/                         # File SQL migration
│   │   ├── 000001_create_users_table.up.sql
│   │   ├── 000001_create_users_table.down.sql
│   │   ├── 000002_add_email_to_users.up.sql
│   │   ├── 000002_add_email_to_users.down.sql
│   │   ├── 000003_create_products_table.up.sql
│   │   ├── 000003_create_products_table.down.sql
│   │   ├── 000004_create_orders_table.up.sql
│   │   ├── 000004_create_orders_table.down.sql
│   │   ├── 000005_add_index_and_constraints.up.sql
│   │   └── 000005_add_index_and_constraints.down.sql
├── pgbouncer/
│   ├── pgbouncer.ini                # Konfigurasi PgBouncer
│   └── userlist.txt                 # Auth users
├── scripts/
│   └── migration.sh                 # Script automasi migration
├── docker-compose.yml               # Orchestrasi Docker
├── Dockerfile                       # Multi-stage build
├── Makefile                         # Shortcut commands
├── go.mod
└── go.sum
```

---

## Cara Menjalankan

### Prasyarat

- Docker & Docker Compose
- Go 1.25+ (untuk development lokal)
- golang-migrate CLI (opsional, bisa pakai Docker)

### Quick Start

```bash
# 1. Clone proyek
cd /path/to/migration

# 2. Start semua services (PostgreSQL + PgBouncer + App)
docker compose up -d

# 3. Cek status
docker compose ps

# 4. Test API
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/users
```

### Menggunakan Script

```bash
# Start infrastructure saja (tanpa app)
./scripts/migration.sh setup

# Apply semua migration
./scripts/migration.sh up

# Lihat status
./scripts/migration.sh status

# Jalankan demo interaktif
./scripts/migration.sh demo
```

### Menggunakan Makefile

```bash
make help          # Lihat semua perintah
make setup         # Start PostgreSQL + PgBouncer
make up            # Apply semua migration
make status        # Lihat status
make psql          # Masuk ke PostgreSQL shell
make psql-tables   # Lihat daftar tabel
```

---

## Penjelasan Migration Files

### Migration 1: Create Users Table

```sql
-- 000001_create_users_table.up.sql
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    username    VARCHAR(100) NOT NULL UNIQUE,
    full_name   VARCHAR(255) NOT NULL DEFAULT '',
    password    VARCHAR(255) NOT NULL,
    is_active   BOOLEAN NOT NULL DEFAULT true,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Konsep yang dipelajari:**
- `BIGSERIAL` — Auto-increment 64-bit integer
- `UNIQUE` — Constraint unik
- `TIMESTAMPTZ` — Timestamp dengan timezone
- `DEFAULT NOW()` — Nilai default saat insert
- **Trigger** untuk auto-update `updated_at`

### Migration 2: Alter Table (Add Column)

```sql
-- 000002_add_email_to_users.up.sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);
ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);
```

**Konsep yang dipelajari:**
- `ALTER TABLE ADD COLUMN` — Menambah kolom ke tabel yang sudah ada
- `ADD CONSTRAINT` — Menambah constraint dengan nama eksplisit
- Mengapa nama constraint penting (untuk rollback yang bersih)

### Migration 3: Foreign Key

```sql
-- 000003_create_products_table.up.sql
CREATE TABLE products (
    ...
    created_by BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ...
);
```

**Konsep yang dipelajari:**
- `REFERENCES` — Foreign key constraint
- `ON DELETE CASCADE` — Hapus otomatis data terkait
- `DECIMAL(12, 2)` — Tipe data untuk harga
- `COMMENT ON TABLE/COLUMN` — Dokumentasi di level database

### Migration 4: Enum, Generated Column, Check Constraint

```sql
-- 000004_create_orders_table.up.sql
CREATE TYPE order_status AS ENUM ('pending', 'processing', ...);

CREATE TABLE order_items (
    ...
    quantity    INTEGER CHECK (quantity > 0),
    subtotal    DECIMAL GENERATED ALWAYS AS (quantity * unit_price) STORED,
    ...
);
```

**Konsep yang dipelajari:**
- `CREATE TYPE ... AS ENUM` — Custom enum type
- `CHECK` constraint — Validasi di level database
- `GENERATED ALWAYS AS ... STORED` — Kolom yang dihitung otomatis
- Junction table (many-to-many relationship)

### Migration 5: Index & Performance

```sql
-- 000005_add_index_and_constraints.up.sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;
CREATE INDEX idx_products_name ON products USING gin(to_tsvector('simple', name));
```

**Konsep yang dipelajari:**
- `CREATE INDEX` — Index biasa untuk pencarian cepat
- **Partial Index** (`WHERE condition`) — Index hanya untuk subset data
- **GIN Index** — Full-text search
- **Composite Index** — Index multi-kolom
- Kapan membuat index terpisah (bukan di migration CREATE TABLE)

---

## Perintah Migration

### Via Script

| Perintah | Fungsi |
|:---|:---|
| `./scripts/migration.sh setup` | Start Docker (PostgreSQL + PgBouncer) |
| `./scripts/migration.sh up` | Apply semua migration |
| `./scripts/migration.sh up 3` | Apply 3 migration |
| `./scripts/migration.sh down 1` | Rollback 1 migration |
| `./scripts/migration.sh down-all` | Rollback semua migration |
| `./scripts/migration.sh version` | Lihat versi saat ini |
| `./scripts/migration.sh goto 3` | Pindah ke versi 3 |
| `./scripts/migration.sh force 2` | Paksa versi ke 2 (fix dirty) |
| `./scripts/migration.sh fresh` | Drop semua & apply ulang |
| `./scripts/migration.sh create add_roles` | Buat migration baru |
| `./scripts/migration.sh status` | Lihat status lengkap |
| `./scripts/migration.sh cleanup` | Stop Docker services |
| `./scripts/migration.sh demo` | Demo interaktif |

### Via Makefile

```bash
make up                    # Apply semua migration
make down                  # Rollback 1 migration
make fresh                 # Fresh migration
make create name=add_roles # Buat migration baru
make status                # Lihat status
make psql                  # Masuk PostgreSQL shell
make pgbouncer-stats       # Lihat statistik PgBouncer
```

### Via Docker (tanpa install CLI lokal)

```bash
# Apply migration via Docker
docker compose run --rm migrate \
  migrate -path=/migrations \
  -database "postgres://postgres:postgres@postgres:5432/migration_db?sslmode=disable" \
  up

# Rollback via Docker
docker compose run --rm migrate \
  migrate -path=/migrations \
  -database "postgres://postgres:postgres@postgres:5432/migration_db?sslmode=disable" \
  down 1
```

---

## API Endpoints

Setelah semua services berjalan, API tersedia di `http://localhost:8080`:

| Method | Endpoint | Fungsi |
|:---|:---|:---|
| GET | `/` | Info aplikasi |
| GET | `/health` | Health check |
| GET | `/api/users` | List semua users |
| GET | `/api/users/:id` | Detail user |
| POST | `/api/users` | Buat user baru |
| PUT | `/api/users/:id` | Update user |
| DELETE | `/api/users/:id` | Hapus user |

### Contoh Request

```bash
# Buat user baru
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "secret123"
  }'

# List users
curl http://localhost:8080/api/users

# Detail user
curl http://localhost:8080/api/users/1

# Update user
curl -X PUT http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"full_name": "John Updated"}'

# Hapus user
curl -X DELETE http://localhost:8080/api/users/1
```

---

## Best Practices

### ✅ Yang HARUS Dilakukan

1. **Satu migration = satu perubahan logis**
   - Jangan campur perubahan yang tidak terkait dalam satu migration

2. **Selalu tulis file .down.sql**
   - Pastikan rollback berfungsi dengan benar

3. **Gunakan nama constraint eksplisit**
   ```sql
   -- ✅ Baik: nama eksplisit
   ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);

   -- ❌ Buruk: nama otomatis (sulit rollback)
   ALTER TABLE users ADD UNIQUE (email);
   ```

4. **Test migration di environment development dulu**
   - Jalankan `up` dan `down` sebelum deploy ke production

5. **Commit migration files ke Git**
   - Migration files adalah bagian dari source code

6. **Gunakan `IF NOT EXISTS` / `IF EXISTS`**
   ```sql
   CREATE TABLE IF NOT EXISTS users (...);
   DROP TABLE IF EXISTS users;
   ```

### ❌ Yang JANGAN Dilakukan

1. **Jangan edit migration yang sudah di-apply di production**
   - Buat migration baru untuk memperbaiki

2. **Jangan hapus migration files**
   - Histori migration harus lengkap

3. **Jangan jalankan migration via PgBouncer**
   - Selalu langsung ke PostgreSQL

4. **Jangan buat migration yang merusak data**
   - Gunakan `ADD COLUMN` bukan `DROP TABLE` + `CREATE TABLE`

5. **Jangan lupa backup sebelum migration di production**

---

## Troubleshooting

### 1. Migration Dirty State

```
error: Dirty database version X. Fix and force version.
```

**Solusi:**
```bash
# Cek migration yang gagal, perbaiki SQL-nya
# Lalu force ke versi sebelumnya
./scripts/migration.sh force <version-sebelumnya>

# Apply ulang
./scripts/migration.sh up
```

### 2. PgBouncer Connection Error

```
error: connection refused (port 6432)
```

**Solusi:**
```bash
# Cek apakah PgBouncer berjalan
docker compose ps pgbouncer

# Cek logs PgBouncer
docker compose logs pgbouncer

# Restart PgBouncer
docker compose restart pgbouncer
```

### 3. Advisory Lock Error

```
error: try lock failed
```

**Penyebab**: Migration dijalankan melalui PgBouncer (bukan langsung ke PostgreSQL).

**Solusi**: Pastikan migration menggunakan port 5432 (PostgreSQL), bukan 6432 (PgBouncer).

### 4. Authentication Error

```
error: password authentication failed
```

**Solusi:**
```bash
# Pastikan userlist.txt berisi hash yang benar
# Generate MD5 hash:
echo -n "passwordusername" | md5sum
# Contoh: echo -n "postgrespostgres" | md5sum

# Format di userlist.txt:
# "postgres" "md5<hash>"
```

### 5. Port Already in Use

```bash
# Cek siapa yang menggunakan port
lsof -i :5432
lsof -i :6432

# Kill proses yang menggunakan port
kill -9 <PID>
```

---

## Teknologi yang Digunakan

| Teknologi | Versi | Fungsi |
|:---|:---|:---|
| Go | 1.25+ | Bahasa pemrograman |
| Echo | v5.3.1 | Web framework |
| pgx | v5.7.4 | PostgreSQL driver |
| golang-migrate | v4.18.2 | Migration library |
| PostgreSQL | 16 | Database |
| PgBouncer | latest | Connection pooler |
| Docker | latest | Containerization |

---

## Lisensi

Proyek ini dibuat untuk tujuan pembelajaran. Bebas digunakan dan dimodifikasi.
