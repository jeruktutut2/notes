#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 6: Kompleks (Master Failover -> DB4 Join -> Failback ke DB1 Original Master)"
echo "=========================================================================="

echo -e "\n🧹 0. Membersihkan lingkungan sebelumnya..."
docker compose down -v 2>/dev/null || true

echo -e "\n--------------------------------------------------------------------------"
echo "🟢 TAHAP 1: Menyalakan DB1, DB2, DB3, Orchestrator & ProxySQL"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-master mysql-replica1 mysql-replica2 orchestrator proxysql haproxy --wait
"$(dirname "$0")/01-setup-replica1.sh"
"$(dirname "$0")/02-setup-replica2.sh"
"$(dirname "$0")/04-register-orchestrator.sh"

echo -e "\n--------------------------------------------------------------------------"
echo "🔴 TAHAP 2: FAILOVER TEST (DB1 Stop -> DB2 Master Baru -> Update ProxySQL)"
echo "--------------------------------------------------------------------------"
docker stop mysql-master

docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = 0;
SET GLOBAL read_only = 0;
CREATE USER IF NOT EXISTS 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
EOF

docker exec -i mysql-replica2 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-replica1',
    SOURCE_PORT=3306,
    SOURCE_USER='repl_user',
    SOURCE_PASSWORD='repl_password',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF

docker exec -i proxysql mysql -uadmin -padmin -h127.0.0.1 -P6032 <<EOF
UPDATE mysql_servers SET hostgroup_id=10 WHERE hostname='mysql-replica1';
UPDATE mysql_servers SET hostgroup_id=20 WHERE hostname='mysql-master';
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
EOF

sleep 2

echo -e "\n--------------------------------------------------------------------------"
echo "🟠 TAHAP 3: Tambah DB4 (mysql-replica3), Replikasi ke DB2 & Register di ProxySQL"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-replica3 --wait

docker exec -i mysql-replica3 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-replica1',
    SOURCE_PORT=3306,
    SOURCE_USER='repl_user',
    SOURCE_PASSWORD='repl_password',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
SET GLOBAL read_only = ON;
SET GLOBAL super_read_only = ON;
EOF

curl -s "http://localhost:3000/api/discover/mysql-replica3/3306" > /dev/null || true
sleep 2

echo -e "\n--------------------------------------------------------------------------"
echo "🔄 TAHAP 4: PROSES FAILBACK (Restore DB1 -> Sync GTID -> Promosi DB1 Master -> Routing)"
echo "--------------------------------------------------------------------------"
docker start mysql-master
docker compose up -d mysql-master --wait

docker exec -i mysql-master mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-replica1',
    SOURCE_PORT=3306,
    SOURCE_USER='repl_user',
    SOURCE_PASSWORD='repl_password',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
SET GLOBAL read_only = ON;
SET GLOBAL super_read_only = ON;
EOF

sleep 3

docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
SET GLOBAL read_only = ON;
SET GLOBAL super_read_only = ON;
EOF

docker exec -i mysql-master mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = 0;
SET GLOBAL read_only = 0;
EOF

docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-master', SOURCE_PORT=3306, SOURCE_USER='repl_user', SOURCE_PASSWORD='repl_password', SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF
docker exec -i mysql-replica2 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-master', SOURCE_PORT=3306, SOURCE_USER='repl_user', SOURCE_PASSWORD='repl_password', SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF
docker exec -i mysql-replica3 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-master', SOURCE_PORT=3306, SOURCE_USER='repl_user', SOURCE_PASSWORD='repl_password', SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF

docker exec -i proxysql mysql -uadmin -padmin -h127.0.0.1 -P6032 <<EOF
UPDATE mysql_servers SET hostgroup_id=10 WHERE hostname='mysql-master';
UPDATE mysql_servers SET hostgroup_id=20 WHERE hostname='mysql-replica1';
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
EOF

sleep 2
echo -e "\n✅ SKENARIO 6 SELESAI: Failback sukses! DB1 kembali menjadi Primary Master, dan seluruh DB2, DB3, DB4 mereplikasi dari DB1."

docker compose down -v
