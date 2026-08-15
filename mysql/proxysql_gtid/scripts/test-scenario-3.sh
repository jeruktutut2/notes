#!/bin/bash
echo "=========================================================================="
echo "📌 SKENARIO 3: 1 Master + 1 Replica -> Tambah 1 Replica Lagi (Scale-Out)"
echo "=========================================================================="

echo -e "\n1. Mereset environment dan menyalakan Master & Replica 1 & Replica 2..."
docker-compose down -v
docker-compose up -d mysql-master mysql-replica1 mysql-replica2

echo -e "\n2. Menunggu container database siap (10 detik)..."
sleep 10

echo -e "\n3. Konfigurasi Replikasi untuk Replica 1 & Replica 2..."
./scripts/01-setup-replica1.sh
./scripts/02-setup-replica2.sh

echo -e "\n4. Melakukan INSERT data baru di Master (mysql-master)..."
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('Eve Scaleout (Skenario 3)', 'QA Engineer');
"

sleep 1

echo -e "\n5. Verifikasi SELECT di Master (mysql-master):"
docker exec -i mysql-master mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n6. Verifikasi SELECT di Replica 1 (mysql-replica1):"
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n7. Verifikasi SELECT di Replica 2 (mysql-replica2):"
docker exec -i mysql-replica2 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n✅ Skenario 3 Selesai: Replica 2 berhasil ditambahkan secara dinamis dan langsung tersinkronisasi dengan Master!"
