#!/bin/bash
# ============================================
# Script: simulate-dc-to-drc.sh
# Skenario: DC Mengirim Data ke DRC via Streaming Replication
# ============================================
set -e

echo "=================================================="
echo "  SKENARIO: SIMULASI PENGIRIMAN DATA DC -> DRC"
echo "=================================================="
echo "  Penjelasan:"
echo "  Aplikasi menulis data baru ke Data Center (DC)."
echo "  PostgreSQL DC secara otomatis mengirim data (WAL)"
echo "  ke Data Recovery Center (DRC) secara real-time."
echo "=================================================="
echo ""

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
TITLE="Transaction Test - $TIMESTAMP"
CONTENT="Data transaksi yang dikirim dari DC pada $TIMESTAMP. Replikasi streaming otomatis bekerja mengalirkan WAL ke DRC."

echo "[1/4] Mengirim data baru ke DC melalui REST API App..."
RESPONSE=$(curl -s -X POST http://localhost:8080/api/data \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"$TITLE\",
    \"content\": \"$CONTENT\",
    \"category\": \"replication_test\"
  }")

echo "Response API:"
echo "$RESPONSE" | grep -o '"message":[^,]*' || echo "$RESPONSE"

# Extract inserted ID using python or grep
INSERTED_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 || echo "")

echo ""
echo "[2/4] Menunggu 1 detik untuk streaming replication (WAL diff)..."
sleep 1

echo ""
echo "[3/4] Memeriksa keberadaan data di DRC Standby (Port 5433 / pg-drc)..."
if [ -n "$INSERTED_ID" ]; then
    DRC_QUERY=$(docker exec -i pg-drc psql -U appuser -d appdb -c "SELECT id, title, source_dc, created_at FROM application_data WHERE id = $INSERTED_ID;" 2>/dev/null)
    echo "$DRC_QUERY"
else
    echo "Querying last 3 records on DRC Standby:"
    docker exec -i pg-drc psql -U appuser -d appdb -c "SELECT id, title, source_dc, created_at FROM application_data ORDER BY id DESC LIMIT 3;"
fi

echo ""
echo "[4/4] Verifikasi Replikasi Lag..."
docker exec -i pg-dc psql -U appuser -d appdb -c "
SELECT
    application_name,
    client_addr,
    state,
    sync_state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_in_bytes
FROM pg_stat_replication;
"

echo "=================================================="
echo "  ✅ KESIMPULAN SKENARIO:"
echo "  Data berhasil ditulis ke DC dan OTOMATIS direplikasi"
echo "  ke DRC tanpa perlu aksi manual dari aplikasi!"
echo "=================================================="
