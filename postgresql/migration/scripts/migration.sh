#!/usr/bin/env bash
# ==========================================
# MIGRATION SCRIPT - Skenario Lengkap
# ==========================================
# Script ini menyediakan semua operasi migration yang umum digunakan.
# Cocok untuk pembelajaran dan penggunaan sehari-hari.
#
# Penggunaan:
#   ./scripts/migration.sh <command> [arguments]
#
# Contoh:
#   ./scripts/migration.sh up          # Apply semua migration
#   ./scripts/migration.sh down 1      # Rollback 1 migration
#   ./scripts/migration.sh status      # Lihat status migration
#   ./scripts/migration.sh create add_roles  # Buat migration baru
# ==========================================

set -euo pipefail

# ==========================================
# KONFIGURASI
# ==========================================
# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Database connection (LANGSUNG ke PostgreSQL, BUKAN PgBouncer!)
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-postgres}"
DB_NAME="${DB_NAME:-migration_db}"
DB_SSLMODE="${DB_SSLMODE:-disable}"

# DSN untuk migration CLI
DATABASE_URL="postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=${DB_SSLMODE}"

# Direktori migration files
MIGRATIONS_DIR="./migrations/sql"

# Direktori proyek
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ==========================================
# FUNGSI HELPER
# ==========================================

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  ${BOLD}$1${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${BOLD}📌 $1${NC}"
}

# Cek apakah migrate CLI terinstall
check_migrate_cli() {
    if ! command -v migrate &> /dev/null; then
        print_error "migrate CLI tidak ditemukan!"
        echo ""
        echo "Instalasi:"
        echo "  # Menggunakan Go"
        echo "  go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest"
        echo ""
        echo "  # Menggunakan Homebrew (macOS)"
        echo "  brew install golang-migrate"
        echo ""
        echo "  # Atau gunakan Docker"
        echo "  docker compose run --rm migrate migrate -help"
        echo ""
        exit 1
    fi
    print_info "migrate CLI ditemukan: $(which migrate)"
}

# Cek koneksi database
check_db_connection() {
    print_info "Mengecek koneksi ke database..."
    if pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" &> /dev/null; then
        print_success "Database tersedia di ${DB_HOST}:${DB_PORT}"
    else
        print_warning "pg_isready gagal, mencoba koneksi langsung..."
    fi
}

# ==========================================
# PERINTAH MIGRATION
# ==========================================

# --- 1. SETUP: Start Docker services ---
cmd_setup() {
    print_header "SETUP - Menjalankan Docker Services"

    cd "${PROJECT_DIR}"

    print_step "1. Menjalankan PostgreSQL dan PgBouncer..."
    docker compose up -d postgres pgbouncer

    print_step "2. Menunggu PostgreSQL siap..."
    local max_wait=30
    local count=0
    while ! docker compose exec postgres pg_isready -U postgres -d migration_db &> /dev/null; do
        count=$((count + 1))
        if [ $count -ge $max_wait ]; then
            print_error "PostgreSQL tidak siap setelah ${max_wait} detik"
            exit 1
        fi
        echo -n "."
        sleep 1
    done
    echo ""

    print_success "PostgreSQL siap!"
    print_success "PgBouncer siap di port 6432!"

    echo ""
    print_info "PostgreSQL: localhost:5432"
    print_info "PgBouncer:  localhost:6432"
    print_info "Database:   ${DB_NAME}"
}

# --- 2. CREATE: Buat migration baru ---
cmd_create() {
    local name="${1:-}"
    if [ -z "$name" ]; then
        print_error "Nama migration diperlukan!"
        echo "  Penggunaan: ./scripts/migration.sh create <nama_migration>"
        echo "  Contoh:     ./scripts/migration.sh create add_roles_table"
        exit 1
    fi

    print_header "CREATE - Membuat Migration Baru: ${name}"

    cd "${PROJECT_DIR}"
    check_migrate_cli

    print_step "Membuat file migration..."
    migrate create -ext sql -dir "${MIGRATIONS_DIR}" -seq "${name}"

    print_success "Migration '${name}' berhasil dibuat!"
    echo ""
    print_info "File yang dibuat:"
    ls -la "${MIGRATIONS_DIR}" | tail -2

    echo ""
    print_warning "PENTING: Jangan lupa edit file .up.sql dan .down.sql!"
    print_info "File .up.sql  = SQL untuk apply perubahan"
    print_info "File .down.sql = SQL untuk rollback perubahan"
}

# --- 3. UP: Apply semua migration ---
cmd_up() {
    print_header "UP - Apply Semua Migration"

    cd "${PROJECT_DIR}"
    check_migrate_cli
    check_db_connection

    print_step "Menjalankan semua migration..."
    echo -e "${CYAN}DSN: postgres://${DB_USER}:****@${DB_HOST}:${DB_PORT}/${DB_NAME}${NC}"
    echo ""

    if migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" up; then
        print_success "Semua migration berhasil di-apply!"
    else
        local exit_code=$?
        if [ $exit_code -eq 0 ]; then
            print_info "Tidak ada migration baru yang perlu di-apply"
        else
            print_error "Migration gagal! (exit code: ${exit_code})"
            echo ""
            print_warning "Jika state 'dirty', gunakan:"
            echo "  ./scripts/migration.sh force <version>"
            exit 1
        fi
    fi

    cmd_version
}

# --- 4. UP N: Apply N migration ---
cmd_up_n() {
    local n="${1:-1}"

    print_header "UP ${n} - Apply ${n} Migration"

    cd "${PROJECT_DIR}"
    check_migrate_cli
    check_db_connection

    print_step "Menjalankan ${n} migration..."

    if migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" up "${n}"; then
        print_success "${n} migration berhasil di-apply!"
    fi

    cmd_version
}

# --- 5. DOWN: Rollback N migration ---
cmd_down() {
    local n="${1:-1}"

    print_header "DOWN ${n} - Rollback ${n} Migration"

    cd "${PROJECT_DIR}"
    check_migrate_cli
    check_db_connection

    print_warning "Ini akan ROLLBACK ${n} migration!"
    echo ""

    print_step "Melakukan rollback ${n} migration..."

    if migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" down "${n}"; then
        print_success "Rollback ${n} migration berhasil!"
    fi

    cmd_version
}

# --- 6. DOWN ALL: Rollback semua migration ---
cmd_down_all() {
    print_header "DOWN ALL - Rollback Semua Migration"

    cd "${PROJECT_DIR}"
    check_migrate_cli
    check_db_connection

    print_warning "⚠️  PERINGATAN: Ini akan menghapus SEMUA tabel dan data!"
    echo ""
    read -p "Apakah Anda yakin? (ketik 'yes' untuk konfirmasi): " confirm
    if [ "$confirm" != "yes" ]; then
        print_info "Dibatalkan."
        exit 0
    fi

    print_step "Melakukan rollback SEMUA migration..."

    if echo "y" | migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" down; then
        print_success "Semua migration berhasil di-rollback!"
    fi

    cmd_version
}

# --- 7. FORCE: Set versi migration (fix dirty state) ---
cmd_force() {
    local version="${1:-}"
    if [ -z "$version" ]; then
        print_error "Versi diperlukan!"
        echo "  Penggunaan: ./scripts/migration.sh force <version>"
        echo "  Contoh:     ./scripts/migration.sh force 3"
        echo ""
        print_info "Gunakan ini ketika migration dalam state 'dirty'."
        print_info "Versi 0 = sebelum migration pertama (clean slate)."
        exit 1
    fi

    print_header "FORCE - Set Versi ke ${version}"

    cd "${PROJECT_DIR}"
    check_migrate_cli

    print_warning "Ini akan memaksa versi migration ke ${version} tanpa menjalankan SQL!"
    echo ""

    print_step "Memaksa versi ke ${version}..."

    if migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" force "${version}"; then
        print_success "Versi berhasil dipaksa ke ${version}!"
    fi

    cmd_version
}

# --- 8. VERSION: Lihat versi migration saat ini ---
cmd_version() {
    print_header "VERSION - Versi Migration Saat Ini"

    cd "${PROJECT_DIR}"
    check_migrate_cli

    print_step "Mengecek versi..."

    local version_output
    version_output=$(migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" version 2>&1) || true

    echo ""
    echo -e "  ${BOLD}Versi saat ini: ${GREEN}${version_output}${NC}"
    echo ""
}

# --- 9. GOTO: Pindah ke versi tertentu ---
cmd_goto() {
    local version="${1:-}"
    if [ -z "$version" ]; then
        print_error "Versi tujuan diperlukan!"
        echo "  Penggunaan: ./scripts/migration.sh goto <version>"
        echo "  Contoh:     ./scripts/migration.sh goto 3"
        exit 1
    fi

    print_header "GOTO - Pindah ke Versi ${version}"

    cd "${PROJECT_DIR}"
    check_migrate_cli
    check_db_connection

    print_warning "Ini akan menjalankan UP atau DOWN migration untuk mencapai versi ${version}!"
    echo ""

    print_step "Pindah ke versi ${version}..."

    if migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" goto "${version}"; then
        print_success "Berhasil pindah ke versi ${version}!"
    fi

    cmd_version
}

# --- 10. FRESH: Drop semua & apply ulang ---
cmd_fresh() {
    print_header "FRESH - Drop Semua & Apply Ulang"

    cd "${PROJECT_DIR}"
    check_migrate_cli
    check_db_connection

    print_warning "⚠️  PERINGATAN: Ini akan MENGHAPUS semua data dan membuat ulang dari awal!"
    echo ""
    read -p "Apakah Anda yakin? (ketik 'yes' untuk konfirmasi): " confirm
    if [ "$confirm" != "yes" ]; then
        print_info "Dibatalkan."
        exit 0
    fi

    print_step "1. Drop semua migration..."
    echo "y" | migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" drop || true

    print_step "2. Apply semua migration dari awal..."
    if migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" up; then
        print_success "Fresh migration berhasil!"
    fi

    cmd_version
}

# --- 11. STATUS: Cek status database ---
cmd_status() {
    print_header "STATUS - Status Database & Migration"

    cd "${PROJECT_DIR}"

    echo -e "${BOLD}🔧 Konfigurasi:${NC}"
    echo "  Host:     ${DB_HOST}"
    echo "  Port:     ${DB_PORT}"
    echo "  User:     ${DB_USER}"
    echo "  Database: ${DB_NAME}"
    echo ""

    # Cek Docker services
    echo -e "${BOLD}🐳 Docker Services:${NC}"
    if docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null; then
        echo ""
    else
        print_warning "Docker compose tidak berjalan"
    fi

    # Cek koneksi database
    echo -e "${BOLD}💾 Database:${NC}"
    check_db_connection

    # Cek versi migration
    if command -v migrate &> /dev/null; then
        echo ""
        echo -e "${BOLD}📊 Migration:${NC}"
        local version_output
        version_output=$(migrate -path "${MIGRATIONS_DIR}" -database "${DATABASE_URL}" version 2>&1) || true
        echo "  Versi saat ini: ${version_output}"
    fi

    # List tabel yang ada
    echo ""
    echo -e "${BOLD}📋 Tabel dalam database:${NC}"
    docker compose exec -T postgres psql -U postgres -d migration_db -c \
        "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;" 2>/dev/null || \
        print_warning "Gagal listing tabel (PostgreSQL mungkin belum berjalan)"

    # Cek migration files
    echo ""
    echo -e "${BOLD}📁 Migration files:${NC}"
    if [ -d "${MIGRATIONS_DIR}" ]; then
        ls -la "${MIGRATIONS_DIR}"/*.sql 2>/dev/null | awk '{print "  " $NF}' || echo "  (kosong)"
    else
        print_warning "Direktori ${MIGRATIONS_DIR} tidak ditemukan"
    fi
}

# --- 12. CLEANUP: Stop Docker services ---
cmd_cleanup() {
    print_header "CLEANUP - Menghentikan Docker Services"

    cd "${PROJECT_DIR}"

    print_step "Menghentikan semua services..."
    docker compose down

    print_success "Semua services dihentikan!"

    echo ""
    read -p "Hapus volume data PostgreSQL juga? (y/n): " remove_vol
    if [ "$remove_vol" = "y" ]; then
        docker compose down -v
        print_success "Volume data dihapus!"
    fi
}

# --- 13. DEMO: Jalankan demo lengkap ---
cmd_demo() {
    print_header "DEMO - Skenario Migration Lengkap"

    cd "${PROJECT_DIR}"
    check_migrate_cli

    echo -e "${BOLD}Demo ini akan menunjukkan alur migration dari awal sampai akhir.${NC}"
    echo ""

    # Step 1: Setup
    print_step "STEP 1: Setup Docker services"
    cmd_setup
    sleep 2

    # Step 2: Cek status awal
    print_step "STEP 2: Cek status awal (belum ada migration)"
    cmd_version 2>/dev/null || print_info "Belum ada migration"
    echo ""
    read -p "Tekan Enter untuk lanjut..." _

    # Step 3: Apply migration satu per satu
    print_step "STEP 3: Apply migration 1 (create_users_table)"
    cmd_up_n 1
    echo ""
    read -p "Tekan Enter untuk lanjut..." _

    print_step "STEP 4: Apply migration 2 (add_email_to_users)"
    cmd_up_n 1
    echo ""
    read -p "Tekan Enter untuk lanjut..." _

    print_step "STEP 5: Apply migration 3 (create_products_table)"
    cmd_up_n 1
    echo ""
    read -p "Tekan Enter untuk lanjut..." _

    # Step 4: Lihat status setelah 3 migration
    print_step "STEP 6: Lihat status setelah 3 migration"
    cmd_status
    echo ""
    read -p "Tekan Enter untuk lanjut..." _

    # Step 5: Rollback 1 migration
    print_step "STEP 7: Rollback 1 migration (products table dihapus)"
    cmd_down 1
    echo ""
    read -p "Tekan Enter untuk lanjut..." _

    # Step 6: Apply sisanya
    print_step "STEP 8: Apply semua migration yang tersisa"
    cmd_up
    echo ""
    read -p "Tekan Enter untuk lanjut..." _

    # Step 7: Final status
    print_step "STEP 9: Status final"
    cmd_status

    echo ""
    print_success "Demo selesai! 🎉"
    echo ""
    echo "Anda bisa:"
    echo "  - Akses API:    curl http://localhost:8080/"
    echo "  - List users:   curl http://localhost:8080/api/users"
    echo "  - Cleanup:      ./scripts/migration.sh cleanup"
}

# ==========================================
# DOCKER MIGRATION COMMANDS
# ==========================================
# Untuk menjalankan migration via Docker (tanpa install migrate CLI lokal)

cmd_docker_up() {
    print_header "DOCKER UP - Apply Migration via Docker"

    cd "${PROJECT_DIR}"

    docker compose run --rm migrate \
        migrate -path=/migrations \
        -database "postgres://postgres:postgres@postgres:5432/migration_db?sslmode=disable" \
        up

    print_success "Migration via Docker berhasil!"
}

cmd_docker_down() {
    local n="${1:-1}"

    print_header "DOCKER DOWN ${n} - Rollback via Docker"

    cd "${PROJECT_DIR}"

    docker compose run --rm migrate \
        migrate -path=/migrations \
        -database "postgres://postgres:postgres@postgres:5432/migration_db?sslmode=disable" \
        down "${n}"

    print_success "Rollback via Docker berhasil!"
}

# ==========================================
# MAIN - Command Router
# ==========================================

show_usage() {
    echo ""
    echo -e "${BOLD}Migration Script - Panduan Penggunaan${NC}"
    echo ""
    echo "Penggunaan:"
    echo "  ./scripts/migration.sh <command> [arguments]"
    echo ""
    echo "Commands:"
    echo -e "  ${GREEN}setup${NC}              Start Docker services (PostgreSQL + PgBouncer)"
    echo -e "  ${GREEN}create${NC} <name>      Buat migration baru"
    echo -e "  ${GREEN}up${NC}                 Apply semua migration"
    echo -e "  ${GREEN}up${NC} <n>             Apply n migration"
    echo -e "  ${GREEN}down${NC} [n]           Rollback n migration (default: 1)"
    echo -e "  ${GREEN}down-all${NC}           Rollback SEMUA migration"
    echo -e "  ${GREEN}force${NC} <version>    Set versi (fix dirty state)"
    echo -e "  ${GREEN}version${NC}            Lihat versi migration saat ini"
    echo -e "  ${GREEN}goto${NC} <version>     Pindah ke versi tertentu"
    echo -e "  ${GREEN}fresh${NC}              Drop semua & apply ulang"
    echo -e "  ${GREEN}status${NC}             Lihat status database & migration"
    echo -e "  ${GREEN}cleanup${NC}            Stop Docker services"
    echo -e "  ${GREEN}demo${NC}               Jalankan demo interaktif (basic)"
    echo -e "  ${GREEN}real${NC}               Jalankan demo real-world (lengkap + data)"
    echo ""
    echo "Docker Commands (tanpa install migrate CLI lokal):"
    echo -e "  ${YELLOW}docker-up${NC}          Apply migration via Docker"
    echo -e "  ${YELLOW}docker-down${NC} [n]    Rollback migration via Docker"
    echo ""
    echo "Environment Variables:"
    echo "  DB_HOST       Database host (default: localhost)"
    echo "  DB_PORT       Database port (default: 5432)"
    echo "  DB_USER       Database user (default: postgres)"
    echo "  DB_PASSWORD   Database password (default: postgres)"
    echo "  DB_NAME       Database name (default: migration_db)"
    echo ""
    echo "Contoh:"
    echo "  ./scripts/migration.sh setup          # Start services"
    echo "  ./scripts/migration.sh up             # Apply semua"
    echo "  ./scripts/migration.sh down 2         # Rollback 2 step"
    echo "  ./scripts/migration.sh create add_roles  # Buat migration baru"
    echo "  ./scripts/migration.sh demo           # Demo interaktif"
    echo ""
}

# Parse command
COMMAND="${1:-help}"
shift || true

case "${COMMAND}" in
    setup)      cmd_setup ;;
    create)     cmd_create "$@" ;;
    up)
        if [ $# -gt 0 ]; then
            cmd_up_n "$@"
        else
            cmd_up
        fi
        ;;
    down)       cmd_down "$@" ;;
    down-all)   cmd_down_all ;;
    force)      cmd_force "$@" ;;
    version)    cmd_version ;;
    goto)       cmd_goto "$@" ;;
    fresh)      cmd_fresh ;;
    status)     cmd_status ;;
    cleanup)    cmd_cleanup ;;
    demo)       cmd_demo ;;
    real)       "${PROJECT_DIR}/scripts/demo_realworld.sh" ;;
    docker-up)  cmd_docker_up ;;
    docker-down) cmd_docker_down "$@" ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Command tidak dikenal: ${COMMAND}"
        show_usage
        exit 1
        ;;
esac
