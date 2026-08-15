#!/usr/bin/env bash
set -e

echo "=================================================================="
echo "🚀 SKENARIO PROGRESIF: Scale-Up & Scale-Down (1 ➔ 2 ➔ 3 ➔ 2 Workers)"
echo "=================================================================="

# ------------------------------------------------------------------
# PHASE 0: Reset Cluster
# ------------------------------------------------------------------
echo ""
echo "🧹 [PHASE 0] Membersihkan container & volume lama..."
docker compose down -v

# ------------------------------------------------------------------
# PHASE 1: Start dengan 1 Worker DB (worker1)
# ------------------------------------------------------------------
echo ""
echo "=================================================================="
echo "📌 PHASE 1: Menjalankan Cluster dengan 1 Worker DB (worker1)"
echo "=================================================================="
docker compose up -d coordinator pgbouncer worker1

echo "⏳ Menunggu coordinator & worker1 siap (TCP)..."
until docker compose exec -T coordinator pg_isready -h coordinator -U postgres -d citus_db > /dev/null 2>&1; do sleep 1; done
until docker compose exec -T coordinator pg_isready -h worker1 -U postgres -d citus_db > /dev/null 2>&1; do sleep 1; done
sleep 2

echo "➕ Mendaftarkan worker1 ke Coordinator..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
DO \$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_dist_node WHERE nodename = 'worker1') THEN
        PERFORM citus_add_node('worker1', 5432);
    END IF;
END \$$;
"

echo "🔄 Membuat Distributed Tables..."
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

echo "📝 [PHASE 1] INSERT Batch 1 (3 Data Users)..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
INSERT INTO users (name, email, country) VALUES
('Budi Santoso', 'budi@example.com', 'Indonesia'),
('Siti Aminah', 'siti@example.com', 'Indonesia'),
('John Doe', 'john@example.com', 'USA');
"

echo ""
echo "📊 [PHASE 1] SELECT Data Users & Lokasi Shard (Saat 1 Worker):"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT id, name, email, country FROM users ORDER BY id;
"
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

sleep 2

# ------------------------------------------------------------------
# PHASE 2: Tambahkan Worker ke-2 (worker2) & Rebalance
# ------------------------------------------------------------------
echo ""
echo "=================================================================="
echo "📌 PHASE 2: Menambahkan Worker ke-2 (worker2) ke Cluster"
echo "=================================================================="
docker compose up -d worker2

echo "⏳ Menunggu worker2 siap (TCP)..."
until docker compose exec -T coordinator pg_isready -h worker2 -U postgres -d citus_db > /dev/null 2>&1; do sleep 1; done
sleep 3

echo "➕ Mendaftarkan worker2 ke Coordinator..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
DO \$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_dist_node WHERE nodename = 'worker2') THEN
        PERFORM citus_add_node('worker2', 5432);
    END IF;
END \$$;
"
sleep 2

echo "⚖️  Memindahkan (Rebalance) Shards secara synchronous ke 2 Workers..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT rebalance_table_shards('users');
"

echo "📝 [PHASE 2] INSERT Batch 2 (3 Data Users Baru)..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
INSERT INTO users (name, email, country) VALUES
('Alice Smith', 'alice@example.com', 'UK'),
('Rudi Hermawan', 'rudi@example.com', 'Indonesia'),
('Dewi Lestari', 'dewi@example.com', 'Indonesia');
"

echo ""
echo "📊 [PHASE 2] SELECT Data Users & Lokasi Shard (Saat 2 Workers):"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT id, name, email, country FROM users ORDER BY id;
"
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
echo "📊 Jumlah Total Shards per Worker Node saat 2 Workers:"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT nodename, count(*) as total_shards 
FROM pg_dist_placement 
JOIN pg_dist_node ON pg_dist_placement.groupid = pg_dist_node.groupid 
GROUP BY nodename
ORDER BY nodename;
"

sleep 3

# ------------------------------------------------------------------
# PHASE 3: Tambahkan Worker ke-3 (worker3) & Rebalance
# ------------------------------------------------------------------
echo ""
echo "=================================================================="
echo "📌 PHASE 3: Menambahkan Worker ke-3 (worker3) ke Cluster"
echo "=================================================================="
docker compose up -d worker3

echo "⏳ Menunggu worker3 siap (TCP)..."
until docker compose exec -T coordinator pg_isready -h worker3 -U postgres -d citus_db > /dev/null 2>&1; do sleep 1; done
sleep 3

echo "➕ Mendaftarkan worker3 ke Coordinator..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
DO \$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_dist_node WHERE nodename = 'worker3') THEN
        PERFORM citus_add_node('worker3', 5432);
    END IF;
END \$$;
"
sleep 2

echo "⚖️  Memindahkan (Rebalance) Shards secara synchronous ke 3 Workers..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT rebalance_table_shards('users');
"

echo "📝 [PHASE 3] INSERT Batch 3 (3 Data Users Baru lagi)..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
INSERT INTO users (name, email, country) VALUES
('Michael Scott', 'michael@example.com', 'USA'),
('Pam Beesly', 'pam@example.com', 'USA'),
('Jim Halpert', 'jim@example.com', 'USA');
"

echo ""
echo "📊 [PHASE 3] SELECT Data Users & Lokasi Shard (Saat 3 Workers):"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT id, name, email, country FROM users ORDER BY id;
"
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

sleep 3

# ------------------------------------------------------------------
# PHASE 4: Scale-Down (Draining & Removing worker2)
# ------------------------------------------------------------------
echo ""
echo "=================================================================="
echo "🔻 PHASE 4: Scale-Down (Evakuasi & Hapus worker2 dari Cluster)"
echo "=================================================================="

echo "1️⃣  Meng-evakuasi (Drain) seluruh pecahan shard dari worker2 ke worker1 & worker3..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT citus_drain_node('worker2', 5432);
"

echo "2️⃣  Menghapus node worker2 dari metadata Citus Cluster..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT citus_remove_node('worker2', 5432);
"

echo "3️⃣  Mematikan container worker2..."
docker compose stop worker2

echo ""
echo "📊 [PHASE 4] SELECT Data Users & Lokasi Shard (Setelah worker2 Dihapus):"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT id, name, email, country FROM users ORDER BY id;
"
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
echo "--- 📊 Rekap Jumlah Total Shards per Node (Hanya worker1 & worker3) ---"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT nodename, count(*) as total_shards 
FROM pg_dist_placement 
JOIN pg_dist_node ON pg_dist_placement.groupid = pg_dist_node.groupid 
GROUP BY nodename
ORDER BY nodename;
"

sleep 3

# ------------------------------------------------------------------
# PHASE 5: Shutdown
# ------------------------------------------------------------------
echo ""
echo "🛑 [PHASE 5] Mematikan & membersihkan cluster (Docker Compose Down)..."
docker compose down -v

echo "=================================================================="
echo "✅ Skenario Progresif Scale-Up & Scale-Down Selesai!"
echo "=================================================================="
