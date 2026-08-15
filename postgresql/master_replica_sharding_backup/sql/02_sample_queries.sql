-- ============================================================================
-- QUERY PENGUJIAN SHARDING & AGREGASI PADA CITUS CLUSTER
-- ============================================================================

-- 1. Pengujian Distribution Shard Map (Melihat distribusi data fisik pada worker nodes)
SELECT nodename, count(*) AS shard_count
FROM citus_shards
GROUP BY nodename;

-- 2. Detail jumlah record per shard untuk tabel users
SELECT shardid, nodename, nodeport, result AS total_rows
FROM run_command_on_shards('users', 'SELECT count(*) FROM %s');

-- 3. Query Terdistribusi (Distributed Join & Aggregation across workers)
EXPLAIN ANALYZE
SELECT 
    u.country_code,
    count(DISTINCT u.user_id) AS total_users,
    count(o.order_id) AS total_orders,
    sum(o.total_amount) AS revenue
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'COMPLETED'
GROUP BY u.country_code
ORDER BY revenue DESC;
