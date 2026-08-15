#!/usr/bin/env bash
set -e

echo "=================================================="
echo "🚀 SKENARIO: Citus Cluster 1 Worker Database"
echo "=================================================="

# 1. Bersihkan cluster sebelumnya (Docker Compose Down)
echo "🧹 [1/7] Membersihkan container & volume lama..."
docker compose down -v

# 2. Jalankan container 1 Worker (coordinator, pgbouncer, worker1)
echo "📦 [2/7] Menjalankan container: coordinator, pgbouncer, worker1..."
docker compose up -d coordinator pgbouncer worker1

# 3. Tunggu hingga database siap menerima koneksi TCP
echo "⏳ [3/7] Menunggu database coordinator & worker1 siap (TCP)..."
until docker compose exec -T coordinator pg_isready -h coordinator -U postgres -d citus_db > /dev/null 2>&1; do
  sleep 1
done
until docker compose exec -T coordinator pg_isready -h worker1 -U postgres -d citus_db > /dev/null 2>&1; do
  sleep 1
done
sleep 2
echo "✅ Database coordinator & worker1 siap!"

# 4. Daftarkan worker1 ke Citus Coordinator
echo "➕ [4/7] Mendaftarkan worker1 ke metadata Citus..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
DO \$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_dist_node WHERE nodename = 'worker1') THEN
        PERFORM citus_add_node('worker1', 5432);
        RAISE NOTICE 'Node worker1 berhasil didaftarkan.';
    ELSE
        RAISE NOTICE 'Node worker1 sudah terdaftar.';
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
echo "📝 [5/7] Memasukkan (INSERT) data contoh ke tabel users..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
INSERT INTO users (name, email, country) VALUES
('Budi Santoso', 'budi@example.com', 'Indonesia'),
('Siti Aminah', 'siti@example.com', 'Indonesia'),
('John Doe', 'john@example.com', 'USA'),
('Alice Smith', 'alice@example.com', 'UK');
"

# 6. SELECT Data & Tampilkan Distribusi Shard
echo "📊 [6/7] Menampilkan (SELECT) data users dan status Sharding..."
echo ""
echo "--- Isi Tabel Users (Queried via Coordinator) ---"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT id, name, email, country, created_at FROM users;
"

echo ""
echo "--- Status Node Terdaftar (pg_dist_node) ---"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT nodeid, nodename, nodeport, isactive FROM pg_dist_node;
"

echo ""
echo "--- Penempatan Shards di Worker (pg_dist_placement) ---"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT nodename, count(*) as total_shards 
FROM pg_dist_placement 
JOIN pg_dist_node ON pg_dist_placement.groupid = pg_dist_node.groupid 
GROUP BY nodename;
"

sleep 3

# 7. Mematikan dan Membersihkan Cluster
echo ""
echo "🛑 [7/7] Mematikan dan membersihkan cluster (Docker Compose Down)..."
docker compose down -v

echo "=================================================="
echo "✅ Skenario 1 DB Worker selesai!"
echo "=================================================="
