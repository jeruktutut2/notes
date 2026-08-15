#!/bin/bash
# ============================================
# Script: failback.sh
# Skenario: Eksekusi Failback (Mengembalikan Operasi ke DC)
# ============================================
set -e

echo "=================================================="
echo "  SKENARIO: PROSES FAILBACK (MENGEMBALIKAN PERAN KE DC)"
echo "=================================================="
echo "  Penjelasan CARA MELAKUKAN FAILBACK:"
echo "  1. DC yang telah pulih dikloning ulang dari DRC (pg_basebackup)"
echo "     agar data baru yang dibuat di DRC selama failover ikut tersinkron."
echo "  2. DC dijadikan Primary utama kembali."
echo "  3. DRC dikembalikan statusnya menjadi Standby (re-attach streaming)."
echo "  4. Target aplikasi dialihkan kembali ke DC."
echo "=================================================="
echo ""

echo "[1/6] Menyalakan kembali server Data Center (pg-dc)..."
docker start pg-dc || true
sleep 3

echo ""
echo "[2/6] Menyinkronkan data baru dari DRC (Promoted) kembali ke DC..."
echo "  Kloning data DRC -> DC menggunakan pg_basebackup..."
docker exec -i pg-dc bash -c "
  rm -rf /var/lib/postgresql/data/*
  PGPASSWORD=replicator_pass pg_basebackup -h pg-drc -p 5432 -U replicator -D /var/lib/postgresql/data -Fp -Xs -R -P
  chmod 0700 /var/lib/postgresql/data
"

echo ""
echo "[3/6] Mempromosikan DC kembali menjadi Primary Utama..."
# Remove standby.signal on DC so it starts as Primary
docker exec -i pg-dc bash -c "rm -f /var/lib/postgresql/data/standby.signal"
docker restart pg-dc
sleep 5

echo "  Verifikasi status DC (Must be Primary):"
docker exec -i pg-dc psql -U appuser -d appdb -c "SELECT pg_is_in_recovery();"

# Re-create replication slot on DC
docker exec -i pg-dc psql -U appuser -d appdb -c "SELECT pg_create_physical_replication_slot('drc_slot');" || true

echo ""
echo "[4/6] Mengembalikan DRC menjadi Standby (Replication Receiver)..."
docker exec -i pg-drc bash -c "
  rm -rf /var/lib/postgresql/data/pgdata/*
  PGPASSWORD=replicator_pass pg_basebackup -h pg-dc -p 5432 -U replicator -D /var/lib/postgresql/data/pgdata -Fp -Xs -R -P --slot=drc_slot
  chmod 0700 /var/lib/postgresql/data/pgdata
"
docker restart pg-drc
sleep 5

echo "  Verifikasi status DRC (Must be Standby / in recovery = true):"
docker exec -i pg-drc psql -U appuser -d appdb -c "SELECT pg_is_in_recovery();"

echo ""
echo "[5/6] Mengalihkan target aplikasi kembali ke DC via API..."
FAILBACK_RES=$(curl -s -X POST http://localhost:8080/api/failback)
echo "  Response API: $FAILBACK_RES"

echo ""
echo "[6/6] Memverifikasi Replikasi Streaming DC -> DRC aktif kembali..."
sleep 2
docker exec -i pg-dc psql -U appuser -d appdb -c "SELECT client_addr, state, sync_state FROM pg_stat_replication;"

echo ""
echo "=================================================="
echo "  ✅ PROSES FAILBACK SELESAI & BERHASIL!"
echo "=================================================="
echo "  - Operasi utama telah dikembalikan penuh ke DC"
echo "  - DC kembali berstatus Primary (Read-Write)"
echo "  - DRC kembali berstatus Standby (Read-Only Replica)"
echo "  - Streaming Replication DC -> DRC aktif kembali!"
echo "=================================================="
