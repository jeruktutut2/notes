#!/usr/bin/env bash
set -e

echo "=================================================="
echo "📊 CITUS SHARDING CLUSTER STATUS"
echo "=================================================="

echo "🖥️  Active Worker Nodes (from pg_dist_node):"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT nodeid, nodename, nodeport, isactive, noderole 
FROM pg_dist_node 
ORDER BY nodeid;
"

echo "📌 Shard Placements per Worker Node:"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT nodename, count(*) as total_shards 
FROM pg_dist_placement 
JOIN pg_dist_node ON pg_dist_placement.groupid = pg_dist_node.groupid 
GROUP BY nodename 
ORDER BY nodename;
"

echo "📈 Total Table Row Counts (Queried via Coordinator):"
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
SELECT 
    (SELECT count(*) FROM users) as total_users,
    (SELECT count(*) FROM orders) as total_orders,
    (SELECT count(*) FROM product_categories) as total_product_categories;
"

echo "=================================================="
