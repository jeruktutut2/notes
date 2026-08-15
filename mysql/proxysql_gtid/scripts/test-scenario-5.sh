#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 5: Progresif Complete + Failover Master & Promosi Replica"
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

echo -e "\n> [UJI WRITE DB3] Mencoba INSERT langsung di DB3 (mysql-replica2)..."
set +e
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Illegal Insert DB3', 'Test Write DB3');
" 2>&1
set -e

echo -e "\n--------------------------------------------------------------------------"
echo "🔴 TAHAP 5: FAILOVER & PROMOSI MASTER BARU (DB1 Stop -> DB2 Master Baru)"
echo "--------------------------------------------------------------------------"
echo "📘 CATATAN PENJELASAN FAILOVER:"
echo "   1. Apakah proses failover ini Otomatis atau Manual?"
echo "      -> JAWABAN: Secara default pada MySQL Replikasi standar, proses ini MANUAL."
echo "         MySQL tidak memiliki bawaan auto-failover tanpa bantuan tools eksternal"
echo "         (seperti Orchestrator, ProxySQL, MHA, atau MySQL InnoDB Cluster)."
echo "   2. Perintah/Script yang digunakan untuk Promosi Manual:"
echo "      a) Matikan Master Lama (docker stop mysql-master)"
echo "      b) Hentikan replikasi di Replica pilihan (DB2): STOP REPLICA; RESET REPLICA ALL;"
echo "      c) Matikan mode Read-Only di DB2: SET GLOBAL read_only=OFF; SET GLOBAL super_read_only=OFF;"
echo "      d) Buat user replikasi di DB2 agar DB3 bisa mereplikasi dari DB2"
echo "      e) Arahkan DB3 ke DB2: CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-replica1'"

echo -e "\n1. Mematikan DB1 (mysql-master)..."
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

echo -e "\n4. [SELECT SEMUA DB HIDUP SEBELUM INSERT BARU]:"
echo "--- DB2 (Master Baru: mysql-replica1) ---"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB3 (Replica dari DB2: mysql-replica2) ---"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"

echo -e "\n5. Melakukan INSERT data baru ke MASTER BARU (DB2 / mysql-replica1)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Data Tahap 5 (Failover DB2 Master)', 'New Primary Master');
"

sleep 1

echo -e "\n6. [SELECT SEMUA DB HIDUP SETELAH INSERT DI MASTER BARU]:"
echo "--- DB2 (Master Baru: mysql-replica1) ---"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"
echo "--- DB3 (Replica dari DB2: mysql-replica2) ---"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "SELECT id, name, position FROM employees;"

echo -e "\n✅ SKENARIO 5 SELESAI: Failover manual berhasil! DB2 sukses dipromosikan jadi Master Baru dan DB3 mereplikasi dari DB2."

echo -e "\n🧹 Menghentikan environment..."
docker compose down
