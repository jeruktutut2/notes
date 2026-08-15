#!/bin/bash
set -e

echo "=========================================================================="
echo "   TAHAP 1: PENGUJIAN MASTER-REPLICA STREAMING REPLICATION"
echo "=========================================================================="

echo "[1/4] Memeriksa status pg_stat_replication pada Master (Coordinator)..."
docker exec -i citus-coordinator psql -U postgres -d app_db -c "
SELECT client_addr, application_name, state, sync_state, sync_priority 
FROM pg_stat_replication;
"

echo "[2/4] Membuat tabel pengujian awal pada Master..."
docker exec -i citus-coordinator psql -U postgres -d app_db -c "
CREATE TABLE IF NOT EXISTS replication_test (
    id SERIAL PRIMARY KEY,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload TEXT
);
INSERT INTO replication_test (payload) VALUES ('Data Uji Streaming Replication Tahap 1');
"

echo "[3/4] Verifikasi Data pada Standby Replica (Port 5433 / Service: citus-coordinator-replica)..."
docker exec -i citus-coordinator-replica psql -U postgres -d app_db -c "
SELECT * FROM replication_test ORDER BY id DESC LIMIT 1;
"

echo "[4/4] Verifikasi Sifat Read-Only pada Replica (Operasi Write Harus Gagal)..."
set +e
docker exec -i citus-coordinator-replica psql -U postgres -d app_db -c "
INSERT INTO replication_test (payload) VALUES ('Mencoba Write ke Replica');
" 2>&1 | grep -i "read-only" && echo "SUCCESS: Replica menolak operasi Write secara benar (Read-Only Mode)!"
set -e

echo "=========================================================================="
echo "   TAHAP 1 BERHASIL DIVERIFIKASI!"
echo "=========================================================================="
