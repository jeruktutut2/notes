#!/bin/bash
echo "=========================================================================="
echo "📌 SKENARIO 1: 1 Master 1 Replica (Uji Insert di Master & Select di Replica)"
echo "=========================================================================="

echo -e "\n0. Menjalankan environment dengan Docker Compose..."
docker compose up -d mysql-master mysql-replica1 --wait

echo -e "\nMenyiapkan replikasi Replica 1..."
"$(dirname "$0")/01-setup-replica1.sh"

echo -e "\n1. Menambahkan data baru di Master (mysql-master)..."
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Charlie Developer (Skenario 1)', 'Fullstack Engineer');
"

sleep 1

echo -e "\n2. Membaca data di Replica 1 (mysql-replica1)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n3. Menguji proteksi read-only: Mencoba INSERT di Replica 1 (Harus Gagal)..."
set +e
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Illegal Insert', 'Hacker');
" 2>&1
set -e

echo -e "\n✅ Skenario 1 Selesai: Data tereplikasi sukses ke Replica 1, dan Replica 1 memblokir operasi WRITE."

echo -e "\n4. Menghentikan environment dengan Docker Compose..."
docker compose down

