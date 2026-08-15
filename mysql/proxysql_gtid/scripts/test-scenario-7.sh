#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 7: Enterprise Architecture (ProxySQL + Golang Echo v5 REST API)"
echo "=========================================================================="

echo -e "\n🧹 0. Membersihkan lingkungan sebelumnya (docker compose down)..."
docker compose down -v 2>/dev/null || true

echo -e "\n--------------------------------------------------------------------------"
echo "🟢 TAHAP 1: Menyalakan DB1 (mysql-master) & DB Initializing"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-master --wait

echo -e "\n--------------------------------------------------------------------------"
echo "🔵 TAHAP 2: Menyalakan DB2 (mysql-replica1) & DB3 (mysql-replica2)"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-replica1 mysql-replica2 --wait
"$(dirname "$0")/01-setup-replica1.sh"
"$(dirname "$0")/02-setup-replica2.sh"

echo -e "\n--------------------------------------------------------------------------"
echo "⚙️ TAHAP 3: Menyalakan ProxySQL & Aplikasi Golang Echo v5 REST API"
echo "--------------------------------------------------------------------------"
docker compose up -d proxysql golang-app --wait

echo -e "\n> Memeriksa Healthcheck Aplikasi REST API Golang Echo v5:"
curl -s http://localhost:8080/api/health | grep -o '"status":"UP"' && echo " ✅ Golang Echo v5 API Ready!"

echo -e "\n--------------------------------------------------------------------------"
echo "🚀 TAHAP 4: Uji Coba Golang REST API (Insert Biasa, Select Biasa, Transaksi Explicit)"
echo "--------------------------------------------------------------------------"

echo -e "\n1. [REST API POST /api/employees] - INSERT BIASA (ProxySQL melempar ke Master)..."
curl -s -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{"name": "Eko Golang (Normal Insert)", "position": "Backend Engineer"}'
echo ""

sleep 1

echo -e "\n2. [REST API GET /api/employees] - SELECT BIASA (ProxySQL melempar ke Replicas)..."
curl -s http://localhost:8080/api/employees
echo ""

sleep 1

echo -e "\n3. [REST API POST /api/employees/transaction] - TRANSAKSI EXPLICIT (SELECT + INSERT di Master)..."
curl -s -X POST http://localhost:8080/api/employees/transaction \
  -H "Content-Type: application/json" \
  -d '{"name": "Tx Financial Audit (App Tx)", "position": "Fintech Specialist"}'
echo ""

sleep 1

echo -e "\n--------------------------------------------------------------------------"
echo "🔴 TAHAP 5: FAILOVER TEST (DB1 Stop -> DB2 Master Baru -> Update ProxySQL)"
echo "--------------------------------------------------------------------------"
echo "1. Mematikan DB1 (mysql-master)..."
docker stop mysql-master

echo -e "\n2. Mempromosikan DB2 (mysql-replica1) menjadi MASTER BARU..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = 0;
SET GLOBAL read_only = 0;
CREATE USER IF NOT EXISTS 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
EOF

echo -e "\n3. Mengarahkan DB3 (mysql-replica2) agar mengekor ke Master Baru (DB2)..."
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

echo -e "\n4. Meng-update ProxySQL Hostgroup (DB2 -> Master Hostgroup 10)..."
docker exec -i proxysql mysql -uadmin -padmin -h127.0.0.1 -P6032 <<EOF
UPDATE mysql_servers SET hostgroup_id=10 WHERE hostname='mysql-replica1';
UPDATE mysql_servers SET hostgroup_id=20 WHERE hostname='mysql-master';
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
EOF

sleep 2

echo -e "\n5. [POST VIA REST API SETELAH FAILOVER] Melakukan INSERT melalui Golang API ke Master Baru (DB2)..."
curl -s -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{"name": "Post-Failover Golang Data", "position": "DevOps Architect"}'
echo ""

sleep 1

echo -e "\n6. [GET VIA REST API SETELAH FAILOVER] Membaca data seluruhnya:"
curl -s http://localhost:8080/api/employees
echo ""

echo -e "\n--------------------------------------------------------------------------"
echo "🟠 TAHAP 6: Tambah DB4 (mysql-replica3), Replikasi ke DB2 & Register di ProxySQL"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-replica3 --wait

echo -e "\n> Menghubungkan DB4 (mysql-replica3) ke Master Aktif (DB2)..."
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

sleep 2

echo -e "\n--------------------------------------------------------------------------"
echo "🔄 TAHAP 7: PROSES FAILBACK (Restore DB1 -> Sync GTID -> Promosi DB1 Master -> ProxySQL Routing)"
echo "--------------------------------------------------------------------------"
echo "1. Menyalakan kembali DB1 (mysql-master)..."
docker start mysql-master
docker compose up -d mysql-master --wait

echo -e "\n2. Re-integrasi DB1 sebagai Replica Sementara dari DB2 (Sync GTID)..."
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

echo "> Menunggu DB1 menyerap seluruh transaksi baru..."
sleep 3

echo -e "\n3. Mengunci DB2 menjadi Read-Only..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
SET GLOBAL read_only = ON;
SET GLOBAL super_read_only = ON;
EOF

echo -e "\n4. Mempromosikan DB1 kembali menjadi PRIMARY MASTER..."
docker exec -i mysql-master mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = 0;
SET GLOBAL read_only = 0;
EOF

echo -e "\n5. Mengarahkan seluruh Replica (DB2, DB3, DB4) mengekor kembali ke DB1..."
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

echo -e "\n6. Mengarahkan kembali ProxySQL Hostgroup (DB1 -> Master Hostgroup 10)..."
docker exec -i proxysql mysql -uadmin -padmin -h127.0.0.1 -P6032 <<EOF
UPDATE mysql_servers SET hostgroup_id=10 WHERE hostname='mysql-master';
UPDATE mysql_servers SET hostgroup_id=20 WHERE hostname='mysql-replica1';
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
EOF

sleep 2

echo -e "\n--------------------------------------------------------------------------"
echo "✨ TAHAP 8: Uji Coba REST API Setelah Failback (Master Sembuh DB1)"
echo "--------------------------------------------------------------------------"
echo -e "\n1. [POST VIA REST API] Melakukan INSERT melalui Golang API ke Master Pulih (DB1)..."
curl -s -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{"name": "Final Restored Golang Entry", "position": "Principal Architect"}'
echo ""

sleep 1

echo -e "\n2. [GET VIA REST API] Membaca data seluruhnya melalui Golang REST API:"
curl -s http://localhost:8080/api/employees
echo ""

echo -e "\n✅ SKENARIO 7 SELESAI SELURUHNYA: Sukses menguji arsitektur Enterprise Golang Echo v5 + ProxySQL + Failover + Failback!"

echo -e "\n🧹 Menghentikan environment..."
docker compose down
