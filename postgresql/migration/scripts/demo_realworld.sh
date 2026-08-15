#!/usr/bin/env bash
# ==========================================
# DEMO REAL-WORLD - Skenario Migration Nyata
# ==========================================
# Script ini mensimulasikan alur kerja migration yang realistis:
#
# Cerita:
#   Anda sedang membangun sistem e-commerce sederhana.
#   Seiring waktu, requirement berubah dan database perlu diperbarui.
#
# Alur:
#   1. Buat tabel users → tambahkan data user
#   2. Tambahkan kolom email → update user yang ada
#   3. Buat tabel products → tambahkan data produk
#   4. Buat tabel orders → buat pesanan
#   5. Tambahkan index → cek performa query
#   6. Rollback demo → lihat efek rollback pada data
#
# Penggunaan:
#   ./scripts/demo_realworld.sh
# ==========================================

set -euo pipefail

# ==========================================
# KONFIGURASI
# ==========================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATIONS_DIR="./migrations/sql"

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"
DB_NAME="${DB_NAME:-migration_db}"
DB_SSLMODE="${DB_SSLMODE:-disable}"

DATABASE_URL="postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=${DB_SSLMODE}"

# ==========================================
# HELPER FUNCTIONS
# ==========================================

print_banner() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}                                                              ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}   ${BOLD}🚀 DEMO REAL-WORLD: Database Migration in Action${NC}          ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}   ${DIM}Simulasi alur kerja migration pada proyek e-commerce${NC}      ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}                                                              ${BLUE}║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_chapter() {
    local chapter_num="$1"
    local title="$2"
    local desc="$3"
    echo ""
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${MAGENTA}  📖 BAB ${chapter_num}: ${BOLD}${title}${NC}"
    echo -e "${DIM}  ${desc}${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_narration() {
    echo -e "${CYAN}  📝 $1${NC}"
}

print_sql() {
    echo -e "${DIM}  SQL: $1${NC}"
}

print_result() {
    echo -e "${GREEN}  ✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}  ⚠️  $1${NC}"
}

print_info() {
    echo -e "${CYAN}  ℹ️  $1${NC}"
}

print_data() {
    echo -e "${BOLD}  📊 Data saat ini:${NC}"
}

pause() {
    echo ""
    echo -e "${DIM}  ─── Tekan Enter untuk lanjut ke langkah berikutnya ───${NC}"
    read -r
}

# Jalankan SQL di PostgreSQL via Docker
run_sql() {
    docker compose exec -T postgres psql -U postgres -d migration_db -c "$1" 2>/dev/null
}

# Jalankan SQL dan tampilkan dengan format rapi
run_sql_pretty() {
    echo ""
    docker compose exec -T postgres psql -U postgres -d migration_db \
        --pset=border=2 --pset=format=wrapped -c "$1" 2>/dev/null
    echo ""
}

# Jalankan migration up N
migrate_up() {
    local n="${1:-}"
    if [ -z "$n" ]; then
        migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" up 2>&1
    else
        migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" up "$n" 2>&1
    fi
}

# Jalankan migration down N
migrate_down() {
    local n="${1:-1}"
    migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" down "$n" 2>&1
}

# Lihat versi migration saat ini
migrate_version() {
    migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" version 2>&1 || echo "belum ada migration"
}

# ==========================================
# CEK PRASYARAT
# ==========================================

check_prerequisites() {
    echo -e "${BOLD}🔍 Mengecek prasyarat...${NC}"

    # Cek migrate CLI
    if ! command -v migrate &> /dev/null; then
        echo -e "${RED}❌ migrate CLI tidak ditemukan!${NC}"
        echo "Install: go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest"
        exit 1
    fi
    echo -e "  ${GREEN}✓${NC} migrate CLI tersedia"

    # Cek Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker tidak ditemukan!${NC}"
        exit 1
    fi
    echo -e "  ${GREEN}✓${NC} Docker tersedia"

    echo ""
}

# ==========================================
# SETUP INFRASTRUCTURE
# ==========================================

setup_infrastructure() {
    echo -e "${BOLD}🐳 Menyiapkan infrastructure...${NC}"
    echo ""

    cd "${PROJECT_DIR}"

    # Stop yang sudah ada
    docker compose down -v 2>/dev/null || true

    # Start PostgreSQL dan PgBouncer
    docker compose up -d postgres pgbouncer

    echo ""
    echo -e "  ${DIM}Menunggu PostgreSQL siap...${NC}"
    local count=0
    while ! docker compose exec -T postgres pg_isready -U postgres -d migration_db &> /dev/null; do
        count=$((count + 1))
        if [ $count -ge 30 ]; then
            echo -e "${RED}❌ PostgreSQL tidak siap setelah 30 detik${NC}"
            exit 1
        fi
        echo -n "."
        sleep 1
    done
    echo ""

    echo -e "  ${GREEN}✓${NC} PostgreSQL siap di port 5432"
    echo -e "  ${GREEN}✓${NC} PgBouncer siap di port 6432"
    echo ""
}

# ==========================================
# BAB 1: MEMULAI PROYEK - CREATE USERS TABLE
# ==========================================

chapter_1() {
    print_chapter "1" "MEMULAI PROYEK" \
        "Hari pertama development. Tim backend butuh tabel users."

    print_narration "Product Manager meminta: 'Kita butuh sistem user management.'"
    print_narration "Backend developer membuat migration pertama..."
    echo ""

    # Tampilkan isi migration
    echo -e "${BOLD}  📄 Migration file: 000001_create_users_table.up.sql${NC}"
    echo -e "${DIM}  ┌──────────────────────────────────────────────────────────┐${NC}"
    echo -e "${DIM}  │ CREATE TABLE users (                                     │${NC}"
    echo -e "${DIM}  │   id          BIGSERIAL PRIMARY KEY,                     │${NC}"
    echo -e "${DIM}  │   username    VARCHAR(100) NOT NULL UNIQUE,              │${NC}"
    echo -e "${DIM}  │   full_name   VARCHAR(255) NOT NULL DEFAULT '',          │${NC}"
    echo -e "${DIM}  │   password    VARCHAR(255) NOT NULL,                     │${NC}"
    echo -e "${DIM}  │   is_active   BOOLEAN NOT NULL DEFAULT true,             │${NC}"
    echo -e "${DIM}  │   created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),        │${NC}"
    echo -e "${DIM}  │   updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()         │${NC}"
    echo -e "${DIM}  │ );                                                       │${NC}"
    echo -e "${DIM}  │ + trigger auto-update updated_at                         │${NC}"
    echo -e "${DIM}  └──────────────────────────────────────────────────────────┘${NC}"
    echo ""

    print_narration "Menjalankan: migrate up 1"
    migrate_up 1
    print_result "Migration 1 berhasil! Tabel users telah dibuat."

    pause

    # ── INSERT DATA ──
    print_narration "Sekarang kita daftarkan beberapa user pertama..."
    echo ""

    print_sql "INSERT INTO users (username, full_name, password) VALUES ..."
    echo ""

    run_sql "
    INSERT INTO users (username, full_name, password) VALUES
        ('admin',  'Administrator',    'hashed_admin_123'),
        ('budi',   'Budi Santoso',     'hashed_budi_456'),
        ('siti',   'Siti Rahayu',      'hashed_siti_789'),
        ('andi',   'Andi Wijaya',      'hashed_andi_012'),
        ('dewi',   'Dewi Lestari',     'hashed_dewi_345');
    "

    print_result "5 user berhasil didaftarkan!"
    echo ""

    print_data
    run_sql_pretty "SELECT id, username, full_name, is_active, created_at FROM users ORDER BY id;"

    print_info "Perhatikan: belum ada kolom email dan phone_number!"
    print_info "Versi migration saat ini: $(migrate_version)"

    pause

    # ── UPDATE DATA ──
    print_narration "Admin meminta: nonaktifkan akun 'andi' karena sudah resign."
    echo ""

    print_sql "UPDATE users SET is_active = false WHERE username = 'andi';"
    run_sql "UPDATE users SET is_active = false WHERE username = 'andi';"
    print_result "User 'andi' dinonaktifkan."

    echo ""
    print_narration "Verifikasi - lihat perubahan pada kolom is_active dan updated_at:"
    run_sql_pretty "SELECT id, username, is_active, updated_at FROM users ORDER BY id;"

    print_info "Perhatikan: updated_at untuk 'andi' berubah otomatis (trigger bekerja!)"

    pause
}

# ==========================================
# BAB 2: ALTER TABLE - TAMBAH KOLOM EMAIL
# ==========================================

chapter_2() {
    print_chapter "2" "KEBUTUHAN BARU: EMAIL & TELEPON" \
        "Minggu ke-2. PM meminta fitur login via email & notifikasi SMS."

    print_narration "Product Manager: 'User perlu bisa login pakai email juga.'"
    print_narration "Product Manager: 'Dan kita butuh nomor telepon untuk OTP.'"
    echo ""
    print_narration "Backend developer TIDAK mengedit migration sebelumnya!"
    print_narration "Melainkan membuat migration BARU untuk menambah kolom."
    echo ""

    echo -e "${BOLD}  📄 Migration file: 000002_add_email_to_users.up.sql${NC}"
    echo -e "${DIM}  ┌──────────────────────────────────────────────────────────┐${NC}"
    echo -e "${DIM}  │ ALTER TABLE users ADD COLUMN email VARCHAR(255);         │${NC}"
    echo -e "${DIM}  │ ALTER TABLE users ADD CONSTRAINT users_email_unique      │${NC}"
    echo -e "${DIM}  │     UNIQUE (email);                                      │${NC}"
    echo -e "${DIM}  │ ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);   │${NC}"
    echo -e "${DIM}  └──────────────────────────────────────────────────────────┘${NC}"
    echo ""

    print_narration "Menjalankan: migrate up 1"
    migrate_up 1
    print_result "Migration 2 berhasil! Kolom email & phone_number ditambahkan."

    pause

    # ── Lihat perubahan skema ──
    print_narration "Lihat struktur tabel setelah alter:"
    run_sql_pretty "\d users"

    print_info "Kolom email dan phone_number berhasil ditambahkan!"
    print_info "Data lama tetap aman — kolom baru bernilai NULL."

    pause

    # ── UPDATE DATA LAMA ──
    print_narration "Sekarang update user yang sudah ada dengan email & telepon mereka..."
    echo ""

    print_sql "UPDATE users SET email = '...', phone_number = '...' WHERE ..."
    echo ""

    run_sql "
    UPDATE users SET email = 'admin@company.com',     phone_number = '081234567890' WHERE username = 'admin';
    UPDATE users SET email = 'budi@gmail.com',         phone_number = '082345678901' WHERE username = 'budi';
    UPDATE users SET email = 'siti@yahoo.com',         phone_number = '083456789012' WHERE username = 'siti';
    UPDATE users SET email = 'andi@gmail.com',         phone_number = '084567890123' WHERE username = 'andi';
    UPDATE users SET email = 'dewi@outlook.com',       phone_number = '085678901234' WHERE username = 'dewi';
    "

    print_result "Semua user lama sudah punya email & phone!"

    echo ""
    print_data
    run_sql_pretty "SELECT id, username, full_name, email, phone_number, is_active FROM users ORDER BY id;"

    pause

    # ── INSERT DATA BARU ──
    print_narration "User baru mendaftar — kali ini SUDAH dengan email & telepon:"
    echo ""

    run_sql "
    INSERT INTO users (username, full_name, password, email, phone_number) VALUES
        ('rudi',   'Rudi Hermawan',  'hashed_rudi_678',  'rudi@gmail.com',    '086789012345'),
        ('maya',   'Maya Sari',      'hashed_maya_901',  'maya@company.com',  '087890123456'),
        ('fajar',  'Fajar Nugroho',  'hashed_fajar_234', 'fajar@startup.io',  '088901234567');
    "

    print_result "3 user baru berhasil didaftarkan dengan email & phone!"

    echo ""
    print_data
    run_sql_pretty "SELECT id, username, email, phone_number, is_active FROM users ORDER BY id;"

    print_info "Total user sekarang: 8 orang"
    print_info "Versi migration: $(migrate_version)"

    pause
}

# ==========================================
# BAB 3: TABEL BARU - PRODUCTS
# ==========================================

chapter_3() {
    print_chapter "3" "FITUR BARU: KATALOG PRODUK" \
        "Bulan ke-2. Saatnya membangun fitur utama: produk."

    print_narration "CTO: 'Kita mulai bangun fitur produk. Setiap produk punya owner (user).'"
    echo ""

    echo -e "${BOLD}  📄 Migration file: 000003_create_products_table.up.sql${NC}"
    echo -e "${DIM}  ┌──────────────────────────────────────────────────────────┐${NC}"
    echo -e "${DIM}  │ CREATE TABLE products (                                  │${NC}"
    echo -e "${DIM}  │   id          BIGSERIAL PRIMARY KEY,                     │${NC}"
    echo -e "${DIM}  │   name        VARCHAR(255) NOT NULL,                     │${NC}"
    echo -e "${DIM}  │   price       DECIMAL(12,2) NOT NULL DEFAULT 0.00,       │${NC}"
    echo -e "${DIM}  │   stock       INTEGER NOT NULL DEFAULT 0,                │${NC}"
    echo -e "${DIM}  │   sku         VARCHAR(50) NOT NULL UNIQUE,               │${NC}"
    echo -e "${DIM}  │   created_by  BIGINT REFERENCES users(id) ON DELETE ..., │${NC}"
    echo -e "${DIM}  │   ...                                                    │${NC}"
    echo -e "${DIM}  │ );                                                       │${NC}"
    echo -e "${DIM}  └──────────────────────────────────────────────────────────┘${NC}"
    echo ""

    print_narration "Menjalankan: migrate up 1"
    migrate_up 1
    print_result "Migration 3 berhasil! Tabel products dibuat."

    pause

    # ── INSERT PRODUCTS ──
    print_narration "Tim produk mulai menambahkan katalog..."
    echo ""

    run_sql "
    INSERT INTO products (name, description, price, stock, sku, created_by) VALUES
        ('Laptop Gaming X1',     'Laptop gaming 16GB RAM, RTX 4060',  15999000.00,  50,  'LAP-GM-001', 1),
        ('Mouse Wireless Pro',   'Mouse ergonomis 2.4GHz',              349000.00, 200,  'MOU-WL-001', 1),
        ('Keyboard Mechanical',  'Keyboard RGB cherry MX blue',         899000.00, 150,  'KEY-MC-001', 2),
        ('Monitor 27 inch 4K',   'Monitor IPS 4K 144Hz',              5499000.00,  30,  'MON-4K-001', 2),
        ('Headset Gaming RGB',   'Headset 7.1 surround sound',          599000.00, 100,  'HDS-GM-001', 3),
        ('Webcam HD 1080p',      'Webcam autofocus built-in mic',       449000.00,  75,  'WEB-HD-001', 7),
        ('USB Hub 7-Port',       'USB 3.0 hub with power adapter',      189000.00, 300,  'USB-HB-001', 7),
        ('SSD NVMe 1TB',         'SSD M.2 NVMe Gen4 read 7000MB/s',  1899000.00,  80,  'SSD-NV-001', 1);
    "

    print_result "8 produk berhasil ditambahkan!"
    echo ""

    print_data
    run_sql_pretty "SELECT id, name, price, stock, sku, created_by FROM products ORDER BY id;"

    pause

    # ── QUERY RELASI ──
    print_narration "Lihat siapa yang mendaftarkan setiap produk (JOIN dengan users):"
    echo ""

    run_sql_pretty "
    SELECT
        p.name AS produk,
        p.price AS harga,
        p.stock AS stok,
        u.full_name AS didaftarkan_oleh
    FROM products p
    JOIN users u ON p.created_by = u.id
    ORDER BY p.price DESC;
    "

    print_info "Foreign key memastikan setiap produk punya owner yang valid!"

    pause

    # ── UPDATE STOCK ──
    print_narration "Ada penjualan! Update stok beberapa produk..."
    echo ""

    run_sql "
    UPDATE products SET stock = stock - 5  WHERE sku = 'LAP-GM-001';
    UPDATE products SET stock = stock - 20 WHERE sku = 'MOU-WL-001';
    UPDATE products SET stock = stock - 10 WHERE sku = 'KEY-MC-001';
    UPDATE products SET stock = stock - 3  WHERE sku = 'MON-4K-001';
    "

    print_result "Stok produk diupdate setelah penjualan."

    echo ""
    print_narration "Lihat stok setelah penjualan:"
    run_sql_pretty "SELECT name, stock, sku FROM products ORDER BY stock ASC;"

    # ── NONAKTIFKAN PRODUK ──
    echo ""
    print_narration "Webcam HD dihentikan penjualannya (discontinued)..."
    run_sql "UPDATE products SET is_active = false WHERE sku = 'WEB-HD-001';"
    print_result "Webcam HD dinonaktifkan."

    run_sql_pretty "SELECT name, stock, is_active FROM products ORDER BY is_active DESC, name;"

    print_info "Versi migration: $(migrate_version)"

    pause
}

# ==========================================
# BAB 4: TABEL KOMPLEKS - ORDERS
# ==========================================

chapter_4() {
    print_chapter "4" "FITUR ORDER: ENUM, CHECK, GENERATED COLUMN" \
        "Bulan ke-3. Fitur pemesanan siap dibangun."

    print_narration "PM: 'User harus bisa pesan produk. Kita perlu order tracking.'"
    echo ""

    echo -e "${BOLD}  📄 Migration file: 000004_create_orders_table.up.sql${NC}"
    echo -e "${DIM}  ┌──────────────────────────────────────────────────────────┐${NC}"
    echo -e "${DIM}  │ CREATE TYPE order_status AS ENUM (                       │${NC}"
    echo -e "${DIM}  │   'pending','processing','shipped','delivered','cancel'  │${NC}"
    echo -e "${DIM}  │ );                                                       │${NC}"
    echo -e "${DIM}  │                                                          │${NC}"
    echo -e "${DIM}  │ CREATE TABLE orders (... status order_status ...);        │${NC}"
    echo -e "${DIM}  │ CREATE TABLE order_items (                               │${NC}"
    echo -e "${DIM}  │   ... quantity CHECK(quantity > 0),                      │${NC}"
    echo -e "${DIM}  │   subtotal GENERATED ALWAYS AS (qty * price) STORED      │${NC}"
    echo -e "${DIM}  │ );                                                       │${NC}"
    echo -e "${DIM}  └──────────────────────────────────────────────────────────┘${NC}"
    echo ""

    print_narration "Menjalankan: migrate up 1"
    migrate_up 1
    print_result "Migration 4 berhasil! Tabel orders & order_items dibuat."

    pause

    # ── BUAT ORDER ──
    print_narration "Pesanan pertama masuk! Budi membeli laptop dan mouse..."
    echo ""

    # Order 1: Budi
    run_sql "
    INSERT INTO orders (order_number, user_id, status, total_amount, notes)
    VALUES ('ORD-2026-0001', 2, 'pending', 16348000.00, 'Minta bubble wrap extra');
    "
    run_sql "
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
        (1, 1, 1, 15999000.00),
        (1, 2, 1,   349000.00);
    "
    print_result "Order #ORD-2026-0001 (Budi): Laptop + Mouse = Rp 16.348.000"

    echo ""
    print_narration "Siti juga memesan keyboard dan headset..."

    # Order 2: Siti
    run_sql "
    INSERT INTO orders (order_number, user_id, status, total_amount, notes)
    VALUES ('ORD-2026-0002', 3, 'pending', 2097000.00, NULL);
    "
    run_sql "
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
        (2, 3, 1, 899000.00),
        (2, 5, 2, 599000.00);
    "
    print_result "Order #ORD-2026-0002 (Siti): Keyboard + 2x Headset = Rp 2.097.000"

    echo ""
    print_narration "Rudi pesan banyak USB hub untuk kantor..."

    # Order 3: Rudi
    run_sql "
    INSERT INTO orders (order_number, user_id, status, total_amount, notes)
    VALUES ('ORD-2026-0003', 6, 'pending', 945000.00, 'Untuk kantor cabang');
    "
    run_sql "
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
        (3, 7, 5, 189000.00);
    "
    print_result "Order #ORD-2026-0003 (Rudi): 5x USB Hub = Rp 945.000"

    pause

    # ── LIHAT ORDERS ──
    print_data
    print_narration "Semua pesanan:"
    run_sql_pretty "
    SELECT
        o.order_number,
        u.full_name AS customer,
        o.status,
        o.total_amount AS total,
        o.notes
    FROM orders o
    JOIN users u ON o.user_id = u.id
    ORDER BY o.id;
    "

    print_narration "Detail item pesanan (perhatikan kolom subtotal = quantity × unit_price):"
    run_sql_pretty "
    SELECT
        o.order_number,
        p.name AS produk,
        oi.quantity AS qty,
        oi.unit_price AS harga_satuan,
        oi.subtotal
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    ORDER BY o.id, oi.id;
    "

    print_info "Kolom 'subtotal' dihitung OTOMATIS oleh PostgreSQL (GENERATED ALWAYS AS)!"

    pause

    # ── UPDATE ORDER STATUS ──
    print_narration "Tim warehouse memproses pesanan..."
    echo ""

    run_sql "UPDATE orders SET status = 'processing' WHERE order_number = 'ORD-2026-0001';"
    print_result "Order ORD-2026-0001 → processing"

    run_sql "UPDATE orders SET status = 'shipped' WHERE order_number = 'ORD-2026-0001';"
    print_result "Order ORD-2026-0001 → shipped"

    run_sql "UPDATE orders SET status = 'processing' WHERE order_number = 'ORD-2026-0002';"
    print_result "Order ORD-2026-0002 → processing"

    run_sql "UPDATE orders SET status = 'cancelled' WHERE order_number = 'ORD-2026-0003';"
    print_result "Order ORD-2026-0003 → cancelled (Rudi batal pesan)"

    echo ""
    print_narration "Status pesanan setelah update:"
    run_sql_pretty "
    SELECT
        o.order_number,
        u.full_name AS customer,
        o.status,
        o.total_amount AS total
    FROM orders o
    JOIN users u ON o.user_id = u.id
    ORDER BY o.id;
    "

    # ── DEMO CHECK CONSTRAINT ──
    echo ""
    print_narration "Coba masukkan order item dengan quantity = 0 (harusnya GAGAL)..."
    echo ""
    print_sql "INSERT INTO order_items ... quantity = 0"
    echo ""

    if run_sql "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (1, 3, 0, 899000.00);" 2>&1; then
        print_warning "Seharusnya gagal!"
    else
        print_result "GAGAL — CHECK constraint (quantity > 0) bekerja!"
        print_info "Database menjaga integritas data: quantity harus > 0"
    fi

    # ── DEMO ENUM CONSTRAINT ──
    echo ""
    print_narration "Coba set status order ke nilai yang tidak ada di enum..."
    echo ""
    print_sql "UPDATE orders SET status = 'selesai' WHERE ..."
    echo ""

    if run_sql "UPDATE orders SET status = 'selesai' WHERE order_number = 'ORD-2026-0001';" 2>&1; then
        print_warning "Seharusnya gagal!"
    else
        print_result "GAGAL — ENUM constraint bekerja!"
        print_info "Status hanya boleh: pending, processing, shipped, delivered, cancelled"
    fi

    print_info "Versi migration: $(migrate_version)"

    pause
}

# ==========================================
# BAB 5: INDEX & OPTIMASI
# ==========================================

chapter_5() {
    print_chapter "5" "OPTIMASI: INDEX & CONSTRAINTS" \
        "Bulan ke-4. Aplikasi mulai lambat. Saatnya optimasi."

    print_narration "DevOps: 'Query semakin lambat. Kita perlu index.'"
    print_narration "DBA: 'Dan tambahkan constraint untuk jaga integritas data.'"
    echo ""

    echo -e "${BOLD}  📄 Migration file: 000005_add_index_and_constraints.up.sql${NC}"
    echo -e "${DIM}  ┌──────────────────────────────────────────────────────────┐${NC}"
    echo -e "${DIM}  │ CREATE INDEX idx_users_email ON users(email);            │${NC}"
    echo -e "${DIM}  │ CREATE INDEX idx_users_active ON users(is_active)        │${NC}"
    echo -e "${DIM}  │     WHERE is_active = true;           -- partial index!  │${NC}"
    echo -e "${DIM}  │ CREATE INDEX idx_products_name ON products               │${NC}"
    echo -e "${DIM}  │     USING gin(to_tsvector(...));      -- full-text!      │${NC}"
    echo -e "${DIM}  │ CREATE INDEX idx_orders_user_status ON orders            │${NC}"
    echo -e "${DIM}  │     (user_id, status);                -- composite!      │${NC}"
    echo -e "${DIM}  │ ALTER TABLE products ADD CONSTRAINT                      │${NC}"
    echo -e "${DIM}  │     chk_products_price_positive CHECK (price >= 0);      │${NC}"
    echo -e "${DIM}  └──────────────────────────────────────────────────────────┘${NC}"
    echo ""

    print_narration "Menjalankan: migrate up 1"
    migrate_up 1
    print_result "Migration 5 berhasil! 12 index + 3 constraint ditambahkan."

    pause

    # ── LIHAT INDEX ──
    print_narration "Lihat semua index yang ada pada tabel users:"
    run_sql_pretty "
    SELECT indexname, indexdef
    FROM pg_indexes
    WHERE tablename = 'users'
    ORDER BY indexname;
    "

    pause

    # ── DEMO EXPLAIN ANALYZE ──
    print_narration "Bandingkan query DENGAN index vs tanpa index:"
    echo ""

    echo -e "${BOLD}  🔍 Query: Cari user aktif berdasarkan email${NC}"
    run_sql_pretty "EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'budi@gmail.com' AND is_active = true;"

    print_info "Index Scan menggunakan idx_users_email — jauh lebih cepat dari Seq Scan!"

    pause

    echo -e "${BOLD}  🔍 Query: Cari pesanan Budi yang sedang diproses${NC}"
    run_sql_pretty "EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 2 AND status = 'shipped';"

    print_info "Composite index idx_orders_user_status digunakan!"

    pause

    # ── DEMO CONSTRAINT ──
    print_narration "Coba masukkan produk dengan harga negatif (harusnya GAGAL)..."
    echo ""

    if run_sql "INSERT INTO products (name, price, stock, sku, created_by) VALUES ('Produk Ilegal', -100, 10, 'ILGL-001', 1);" 2>&1; then
        print_warning "Seharusnya gagal!"
    else
        print_result "GAGAL — CHECK constraint (price >= 0) bekerja!"
    fi

    echo ""
    print_narration "Coba update stok menjadi negatif (harusnya GAGAL)..."

    if run_sql "UPDATE products SET stock = -5 WHERE sku = 'LAP-GM-001';" 2>&1; then
        print_warning "Seharusnya gagal!"
    else
        print_result "GAGAL — CHECK constraint (stock >= 0) bekerja!"
        print_info "Database mencegah stok negatif. Integritas data terjaga!"
    fi

    print_info "Versi migration: $(migrate_version)"

    pause
}

# ==========================================
# BAB 6: ROLLBACK DEMO
# ==========================================

chapter_6() {
    print_chapter "6" "ROLLBACK: MEMBATALKAN MIGRATION" \
        "Situasi darurat. Fitur order ditarik kembali."

    print_narration "PM: 'Fitur order belum siap production. Rollback dulu.'"
    print_narration "Tim dev: 'Kita rollback 2 migration terakhir (index + orders).'"
    echo ""

    echo -e "${BOLD}  Sebelum rollback:${NC}"
    print_narration "Versi saat ini: $(migrate_version)"
    print_narration "Tabel yang ada:"
    run_sql_pretty "SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != 'schema_migrations' ORDER BY tablename;"

    pause

    # ── ROLLBACK 2 ──
    print_narration "Menjalankan: migrate down 2"
    print_warning "Ini akan menghapus tabel orders, order_items, dan semua index!"
    echo ""

    migrate_down 2

    print_result "Rollback 2 migration berhasil!"
    echo ""

    echo -e "${BOLD}  Setelah rollback:${NC}"
    print_narration "Versi saat ini: $(migrate_version)"
    print_narration "Tabel yang tersisa:"
    run_sql_pretty "SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != 'schema_migrations' ORDER BY tablename;"

    print_info "Tabel orders & order_items HILANG, tapi users & products tetap ada!"

    pause

    # ── DATA MASIH ADA ──
    print_narration "Data users dan products tetap aman setelah rollback:"
    echo ""

    print_data
    echo -e "${BOLD}  Users:${NC}"
    run_sql_pretty "SELECT id, username, email, is_active FROM users ORDER BY id;"

    echo -e "${BOLD}  Products:${NC}"
    run_sql_pretty "SELECT id, name, price, stock FROM products ORDER BY id;"

    print_info "Rollback hanya menghapus yang di-rollback, data lain aman!"

    pause

    # ── RE-APPLY ──
    print_narration "Setelah memperbaiki bug, apply ulang migration..."
    echo ""

    print_narration "Menjalankan: migrate up (apply semua yang belum)"
    migrate_up
    print_result "Migration berhasil di-apply ulang!"

    echo ""
    print_narration "Versi akhir: $(migrate_version)"
    print_narration "Semua tabel kembali:"
    run_sql_pretty "SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != 'schema_migrations' ORDER BY tablename;"

    print_info "Tapi data orders & order_items HILANG karena sudah di-rollback."
    print_warning "Ini kenapa rollback di production harus hati-hati — data bisa hilang!"

    pause
}

# ==========================================
# SUMMARY
# ==========================================

print_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}   ${BOLD}🎉 DEMO SELESAI!${NC}                                          ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}                                                              ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    echo -e "${BOLD}📚 Ringkasan yang Anda pelajari:${NC}"
    echo ""
    echo -e "  ${GREEN}Bab 1${NC} ─ CREATE TABLE + INSERT + UPDATE + trigger auto-update"
    echo -e "  ${GREEN}Bab 2${NC} ─ ALTER TABLE + update data lama + insert data baru"
    echo -e "  ${GREEN}Bab 3${NC} ─ FOREIGN KEY + JOIN + update stock + soft-delete produk"
    echo -e "  ${GREEN}Bab 4${NC} ─ ENUM + CHECK + GENERATED column + constraint validation"
    echo -e "  ${GREEN}Bab 5${NC} ─ INDEX (partial, GIN, composite) + EXPLAIN ANALYZE"
    echo -e "  ${GREEN}Bab 6${NC} ─ ROLLBACK + re-apply + dampak pada data"
    echo ""
    echo -e "${BOLD}🔑 Poin Penting:${NC}"
    echo ""
    echo -e "  1. ${CYAN}Jangan edit migration yang sudah jalan${NC} — buat migration baru"
    echo -e "  2. ${CYAN}Migration harus bypass PgBouncer${NC} — karena advisory lock"
    echo -e "  3. ${CYAN}Selalu tulis .down.sql${NC} — untuk rollback yang bersih"
    echo -e "  4. ${CYAN}Rollback bisa menghapus data${NC} — hati-hati di production"
    echo -e "  5. ${CYAN}Gunakan constraint di database${NC} — jangan hanya di aplikasi"
    echo ""
    echo -e "${BOLD}🛠️  Langkah selanjutnya:${NC}"
    echo ""
    echo -e "  • Coba buat migration sendiri:"
    echo -e "    ${DIM}./scripts/migration.sh create add_categories${NC}"
    echo ""
    echo -e "  • Akses database langsung:"
    echo -e "    ${DIM}make psql${NC}"
    echo ""
    echo -e "  • Start API server:"
    echo -e "    ${DIM}docker compose up -d app${NC}"
    echo -e "    ${DIM}curl http://localhost:8080/api/users${NC}"
    echo ""
    echo -e "  • Lihat statistik PgBouncer:"
    echo -e "    ${DIM}make pgbouncer-stats${NC}"
    echo ""
}

# ==========================================
# MAIN
# ==========================================

main() {
    cd "${PROJECT_DIR}"

    print_banner
    check_prerequisites
    setup_infrastructure

    echo -e "${BOLD}Demo ini akan berjalan dalam 6 bab. Tekan Enter untuk mulai.${NC}"
    pause

    chapter_1
    chapter_2
    chapter_3
    chapter_4
    chapter_5
    chapter_6

    print_summary

    echo -e "${BOLD}🧹 Membersihkan environment (Docker compose down)...${NC}"
    docker compose down -v
}

main "$@"
