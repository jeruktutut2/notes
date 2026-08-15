#!/usr/bin/env bash
set -e

echo "=================================================="
echo "🚀 SKENARIO: Citus Cluster 2 Worker Databases"
echo "=================================================="

# 1. Bersihkan cluster sebelumnya (Docker Compose Down)
echo "🧹 [1/7] Membersihkan container & volume lama..."
docker compose down -v

# 2. Jalankan container 2 Workers (coordinator, pgbouncer, worker1, worker2)
echo "📦 [2/7] Menjalankan container: coordinator, pgbouncer, worker1, worker2..."
docker compose up -d coordinator pgbouncer worker1 worker2

# 3. Tunggu hingga database siap menerima koneksi TCP
echo "⏳ [3/7] Menunggu database coordinator, worker1, & worker2 siap (TCP)..."
until docker compose exec -T coordinator pg_isready -h coordinator -U postgres -d citus_db > /dev/null 2>&1; do
  sleep 1
done
until docker compose exec -T coordinator pg_isready -h worker1 -U postgres -d citus_db > /dev/null 2>&1; do
  sleep 1
done
until docker compose exec -T coordinator pg_isready -h worker2 -U postgres -d citus_db > /dev/null 2>&1; do
  sleep 1
done
sleep 2
echo "✅ Database coordinator, worker1, & worker2 siap!"

# 4. Daftarkan worker1 & worker2 ke Citus Coordinator
echo "➕ [4/7] Mendaftarkan worker1 & worker2 ke metadata Citus..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
DO \$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_dist_node WHERE nodename = 'worker1') THEN
        PERFORM citus_add_node('worker1', 5432);
        RAISE NOTICE 'Node worker1 berhasil didaftarkan.';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_dist_node WHERE nodename = 'worker2') THEN
        PERFORM citus_add_node('worker2', 5432);
        RAISE NOTICE 'Node worker2 berhasil didaftarkan.';
    END IF;
END \$$;
"

# Memastikan tabel users & orders terdistribusi (sharded)
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
DO \$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM citus_tables WHERE table_name = 'users'::regclass) THEN
        PERFORM create_distributed_table('users', 'id');
        PERFORM create_distributed_table('orders', 'user_id', colocate_with => 'users');
        PERFORM create_reference_table('product_categories');
    END IF;
END \$$;
" > /dev/null 2>&1

# 5. INSERT Data Pengguna Contoh
echo "📝 [5/7] Memasukkan (INSERT) 8 data contoh ke tabel users..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
INSERT INTO users (name, email, country) VALUES
('Budi Santoso', 'budi@example.com', 'Indonesia'),
('Siti Aminah', 'siti@example.com', 'Indonesia'),
('John Doe', 'john@example.com', 'USA'),
('Alice Smith', 'alice@example.com', 'UK'),
('Rudi Hermawan', 'rudi@example.com', 'Indonesia'),
('Dewi Lestari', 'dewi@example.com', 'Indonesia'),
('Michael Scott', 'michael@example.com', 'USA'),
('Pam Beesly', 'pam@example.com', 'USA');
"

# 6. SELECT Data & Tampilkan Pembuktian Sharding di Tiap-tiap DB Worker
echo "📊 [6/7] Menampilkan pembuktian Sharding langsung per-Worker Node..."
echo ""
echo "--- 🌐 [COORDINATOR VIEW] Seluruh Data Users Gabungan (8 User) ---"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT id, name, email, country FROM users ORDER BY id;
"

echo ""
echo "--- 🔍 [PEMBUKTIAN SHARDING] Lokasi Simpul Worker & Data Baris di Dalam Physical Shard Table ---"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT 
    s.nodename AS worker_node,
    s.shard_name,
    r.result AS data_rows_in_shard
FROM run_command_on_shards('users', \$$ SELECT string_agg('ID:' || id || ' (' || name || ')', ', ') FROM %s \$$) r
JOIN citus_shards s ON s.shardid = r.shardid
WHERE r.result IS NOT NULL AND r.result != ''
ORDER BY s.nodename, s.shardid;
"

echo ""
echo "--- 📊 Total Shard Terbagi per Worker Node (pg_dist_placement) ---"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT nodename, count(*) as total_shards 
FROM pg_dist_placement 
JOIN pg_dist_node ON pg_dist_placement.groupid = pg_dist_node.groupid 
GROUP BY nodename
ORDER BY nodename;
"

sleep 3

# 7. Mematikan dan Membersihkan Cluster
echo ""
echo "🛑 [7/7] Mematikan dan membersihkan cluster (Docker Compose Down)..."
docker compose down -v

echo "=================================================="
echo "✅ Skenario 2 DB Worker selesai!"
echo "=================================================="
