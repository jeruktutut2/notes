#!/bin/bash
set -e

echo "=========================================================================="
echo "   TAHAP 2: PENGUJIAN HORIZONTAL SHARDING (CITUS CLUSTER)"
echo "=========================================================================="

echo "[1/4] Mengaplikasikan Schema & Data Seeding Terdistribusi ke Master..."
docker exec -i citus-coordinator psql -U postgres -d app_db -f /sql/01_schema_and_sharding.sql

echo "[2/4] Memeriksa daftar Worker Nodes terdaftar pada Citus Cluster..."
docker exec -i citus-coordinator psql -U postgres -d app_db -c "
SELECT nodeid, nodename, nodeport, isactive FROM citus_get_active_worker_nodes();
"

echo "[3/4] Verifikasi Pembagian Shard secara Fisik di Worker Node 1 & Worker Node 2..."
docker exec -i citus-coordinator psql -U postgres -d app_db -c "
SELECT nodename, count(*) AS total_shards 
FROM citus_shards 
GROUP BY nodename;
"

echo "Distribusi Jumlah Record 'users' per Shard Fisik di Worker Nodes:"
docker exec -i citus-coordinator psql -U postgres -d app_db -c "
SELECT nodename, shardid, result AS total_rows 
FROM run_command_on_shards('users', 'SELECT count(*) FROM %s')
ORDER BY nodename, shardid
LIMIT 10;
"

echo "Total Record 'users' terdistribusi pada seluruh Cluster:"
docker exec -i citus-coordinator psql -U postgres -d app_db -c "SELECT count(*) AS total_users FROM users;"

echo "[4/4] Eksekusi Distributed Aggregation Query & Execution Plan..."
docker exec -i citus-coordinator psql -U postgres -d app_db -f /sql/02_sample_queries.sql

echo "=========================================================================="
echo "   TAHAP 2 BERHASIL DIVERIFIKASI!"
echo "=========================================================================="
