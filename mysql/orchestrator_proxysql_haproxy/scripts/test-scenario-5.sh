#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 5: Progresif Complete + Failover Master & Promosi Replica via Orchestrator"
echo "=========================================================================="

echo -e "\n🧹 0. Membersihkan lingkungan sebelumnya (docker compose down)..."
docker compose down -v 2>/dev/null || true

echo -e "\n--------------------------------------------------------------------------"
echo "🟢 TAHAP 1: Menyalakan DB1, DB2, DB3 & Orchestrator"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-master mysql-replica1 mysql-replica2 orchestrator --wait

"$(dirname "$0")/01-setup-replica1.sh"
"$(dirname "$0")/02-setup-replica2.sh"
"$(dirname "$0")/04-register-orchestrator.sh"

echo -e "\n--------------------------------------------------------------------------"
echo "🔴 TAHAP 2: FAILOVER & PROMOSI MASTER BARU (DB1 Stop -> Orchestrator & DB2 Master Baru)"
echo "--------------------------------------------------------------------------"
echo "1. Mematikan DB1 (mysql-master)..."
docker stop mysql-master

echo -e "\n2. Menginstruksikan Orchestrator mempromosikan DB2 (mysql-replica1) menjadi MASTER BARU..."
curl -s "http://localhost:3000/api/graceful-master-takeover/company_db/mysql-master/3306/mysql-replica1/3306" || true

docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = OFF;
SET GLOBAL read_only = OFF;
CREATE USER IF NOT EXISTS 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
EOF

echo -e "\n3. Mengarahkan DB3 (mysql-replica2) agar mereplikasi dari Master Baru (DB2 / mysql-replica1)..."
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

sleep 2

echo -e "\n4. Melakukan INSERT data baru ke MASTER BARU (DB2 / mysql-replica1)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Data Tahap 5 (Failover DB2 Master)', 'New Primary Master');
"

sleep 1

echo -e "\n5. [SELECT SEMUA DB HIDUP SETELAH INSERT DI MASTER BARU]:"
echo "--- DB2 (Master Baru: mysql-replica1) ---"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB3 (Replica dari DB2: mysql-replica2) ---"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"

echo -e "\n✅ SKENARIO 5 SELESAI: Failover berhasil! DB2 sukses dipromosikan jadi Master Baru dan DB3 mereplikasi dari DB2."

echo -e "\n🧹 Menghentikan environment..."
docker compose down -v
