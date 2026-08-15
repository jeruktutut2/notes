#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 4: Progresif 1 DB Standalone -> Master -> Replica 1 -> Replica 2"
echo "=========================================================================="

echo -e "\n🧹 0. Membersihkan lingkungan sebelumnya (docker compose down)..."
docker compose down -v 2>/dev/null || true

echo -e "\n--------------------------------------------------------------------------"
echo "🟢 TAHAP 1: Hanya 1 DB (DB1 / mysql-master) yang hidup (Insert & Select)"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-master --wait

echo -e "\n> Melakukan INSERT data awal ke DB1 (mysql-master)..."
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Data Tahap 1 (DB1 Standalone)', 'Standalone Engine');
"

echo -e "\n> [SELECT] Membaca data pada DB1 (mysql-master):"
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n--------------------------------------------------------------------------"
echo "👑 TAHAP 2: Menyiapkan DB1 (mysql-master) sebagai Master Replikasi (GTID)"
echo "--------------------------------------------------------------------------"
echo "> Memeriksa status GTID & Master pada DB1..."
docker exec -i mysql-master mysql -uroot -prootpassword -e "
SELECT @@global.gtid_mode AS gtid_mode, @@global.enforce_gtid_consistency AS gtid_consistency;
SHOW MASTER STATUS\G
"

echo -e "\n--------------------------------------------------------------------------"
echo "🔵 TAHAP 3: Menyalakan DB2 (mysql-replica1), Replikasi dari DB1, Insert & Select"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-replica1 --wait

echo -e "\n> Menghubungkan DB2 (mysql-replica1) ke Master (DB1)..."
"$(dirname "$0")/01-setup-replica1.sh"

sleep 1

echo -e "\n> Melakukan INSERT data baru ke DB1 (mysql-master)..."
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Data Tahap 3 (Replikasi DB1-DB2)', 'Replica 1 Active');
"

sleep 1

echo -e "\n> [SELECT DB1] Membaca data di DB1 (mysql-master):"
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n> [SELECT DB2] Membaca data di DB2 (mysql-replica1):"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n> [UJI WRITE DB2] Mencoba INSERT langsung di DB2 (mysql-replica1)..."
set +e
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Illegal Insert DB2', 'Test Write DB2');
" 2>&1
set -e

echo -e "\n--------------------------------------------------------------------------"
echo "🟣 TAHAP 4: Menyalakan DB3 (mysql-replica2), Replikasi dari DB1, Select & Insert"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-replica2 --wait

echo -e "\n> Menghubungkan DB3 (mysql-replica2) ke Master (DB1)..."
"$(dirname "$0")/02-setup-replica2.sh"

sleep 1

echo -e "\n> [SELECT SEBELUM INSERT BARU] Membaca data di DB1, DB2, dan DB3:"
echo "--- DB1 (mysql-master) ---"
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB2 (mysql-replica1) ---"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB3 (mysql-replica2) ---"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"

echo -e "\n> Melakukan INSERT data baru ke DB1 (mysql-master)..."
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Data Tahap 4 (Replikasi DB1-DB2-DB3)', 'Replica 2 Active');
"

sleep 1

echo -e "\n> [SELECT SETELAH INSERT BARU] Membaca data di DB1, DB2, dan DB3:"
echo "--- DB1 (mysql-master) ---"
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB2 (mysql-replica1) ---"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB3 (mysql-replica2) ---"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"

echo -e "\n> [UJI WRITE DB3] Mencoba INSERT langsung di DB3 (mysql-replica2)..."
set +e
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Illegal Insert DB3', 'Test Write DB3');
" 2>&1
set -e

echo -e "\n✅ SKENARIO 4 SELESAI: Berhasil menguji alur progresif dari 1 DB Standalone -> DB Master -> Replikasi DB2 -> Replikasi DB3."

echo -e "\n🧹 Menghentikan environment..."
docker compose down

