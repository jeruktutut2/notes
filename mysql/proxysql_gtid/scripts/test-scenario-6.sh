#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 6: Skenario Kompleks (Tahap 1-5 + DB4 Join + Failback ke DB1)"
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

echo -e "\n> [SELECT DB1] Membaca data pada DB1 (mysql-master):"
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

echo -e "\n--------------------------------------------------------------------------"
echo "🔴 TAHAP 5: FAILOVER (DB1 Stop -> DB2 Master Baru -> DB3 Replikasi ke DB2)"
echo "--------------------------------------------------------------------------"
echo "1. Mematikan DB1 (mysql-master)..."
docker stop mysql-master

echo -e "\n2. Mempromosikan DB2 (mysql-replica1) menjadi MASTER BARU..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = OFF;
SET GLOBAL read_only = OFF;
CREATE USER IF NOT EXISTS 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
EOF

echo -e "\n3. Mengarahkan DB3 (mysql-replica2) agar mereplikasi dari Master Baru (DB2)..."
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

echo -e "\n--------------------------------------------------------------------------"
echo "🟠 TAHAP 6: Menambah DB Baru (DB4 / mysql-replica3) & Replikasi ke DB2"
echo "--------------------------------------------------------------------------"
docker compose up -d mysql-replica3 --wait

echo -e "\n> Menghubungkan DB4 (mysql-replica3) ke Master Aktif (DB2 / mysql-replica1)..."
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

echo -e "\n> Melakukan INSERT data baru ke DB2 (mysql-replica1)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Data Tahap 6 (DB4 Join Cluster)', 'Replica 3 Active');
"

sleep 1

echo -e "\n> [SELECT SEMUA DB AKTIF (DB2, DB3, DB4)]:"
echo "--- DB2 (Master Aktif: mysql-replica1) ---"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB3 (Replica dari DB2: mysql-replica2) ---"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB4 (Replica dari DB2: mysql-replica3) ---"
docker exec -i mysql-replica3 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"

echo -e "\n--------------------------------------------------------------------------"
echo "🔄 TAHAP 7: PROSES FAILBACK (Menyalakan Kembali DB1 -> Sync GTID -> Promosi DB1 Master)"
echo "--------------------------------------------------------------------------"
echo "📘 CATATAN PENJELASAN FAILBACK:"
echo "   1. DB1 dinyalakan kembali via docker start mysql-master."
echo "   2. DB1 TIDAK LANGSUNG jadi Master, tapi dijadikan REPLICA SEMENTARA dari DB2 terlebih dahulu."
echo "   3. GTID (SOURCE_AUTO_POSITION=1) secara otomatis mendeteksi transaksi 5 & 6 yang belum ada di DB1."
echo "   4. Setelah DB1 100% sync dengan DB2, DB2 dikunci (read_only=ON)."
echo "   5. DB1 dipromosikan kembali jadi Primary Master (read_only=OFF)."
echo "   6. Seluruh Replica (DB2, DB3, DB4) dialihkan kembali mengekor ke DB1."

echo -e "\n1. Menyalakan kembali DB1 (mysql-master)..."
docker start mysql-master
docker compose up -d mysql-master --wait

echo -e "\n2. Re-integrasi DB1 sebagai Replica Sementara dari DB2 (Sync Data via GTID)..."
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

echo "> Menunggu DB1 menyerap seluruh transaksi baru dari DB2..."
sleep 3

echo -e "\n3. Mengunci DB2 (Master Sementara) menjadi Read-Only..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
SET GLOBAL read_only = ON;
SET GLOBAL super_read_only = ON;
EOF

echo -e "\n4. Mempromosikan kembali DB1 (mysql-master) menjadi PRIMARY MASTER..."
docker exec -i mysql-master mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = OFF;
SET GLOBAL read_only = OFF;
EOF

echo -e "\n5. Mengarahkan seluruh Replica (DB2, DB3, DB4) mengekor kembali ke DB1 (mysql-master)..."
echo "> Mengarahkan DB2 (mysql-replica1) ke DB1..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-master',
    SOURCE_PORT=3306,
    SOURCE_USER='repl_user',
    SOURCE_PASSWORD='repl_password',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF

echo "> Mengarahkan DB3 (mysql-replica2) ke DB1..."
docker exec -i mysql-replica2 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-master',
    SOURCE_PORT=3306,
    SOURCE_USER='repl_user',
    SOURCE_PASSWORD='repl_password',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF

echo "> Mengarahkan DB4 (mysql-replica3) ke DB1..."
docker exec -i mysql-replica3 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-master',
    SOURCE_PORT=3306,
    SOURCE_USER='repl_user',
    SOURCE_PASSWORD='repl_password',
    SOURCE_AUTO_POSITION=1;
START REPLICA;
EOF

sleep 2

echo -e "\n--------------------------------------------------------------------------"
echo "✨ TAHAP 8: Uji Coba Write di Primary Master (DB1) & Select di Semua DB (DB1-DB4)"
echo "--------------------------------------------------------------------------"
echo -e "\n> Melakukan INSERT data baru ke Primary Master yang Pulih (DB1 / mysql-master)..."
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Data Tahap 8 (Failback Complete)', 'Primary Master Restored');
"

sleep 1

echo -e "\n> [SELECT SELURUH 4 DATABASE (DB1, DB2, DB3, DB4)]:"
echo "--- DB1 (Primary Master: mysql-master) ---"
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB2 (Replica 1: mysql-replica1) ---"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB3 (Replica 2: mysql-replica2) ---"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB4 (Replica 3: mysql-replica3) ---"
docker exec -i mysql-replica3 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"

echo -e "\n✅ SKENARIO 6 SELESAI SELURUHNYA: Sukses menguji 1 DB Standalone -> GTID Master -> Replikasi DB2 -> DB3 -> Failover DB2 Master -> Join DB4 -> Failback DB1 Master!"

echo -e "\n🧹 Menghentikan environment..."
docker compose down
