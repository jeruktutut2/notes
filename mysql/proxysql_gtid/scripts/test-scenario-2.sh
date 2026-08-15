#!/bin/bash
echo "=========================================================================="
echo "📌 SKENARIO 2: Master OFF -> Promote Replica 1 jadi Master Baru (Failover)"
echo "=========================================================================="

echo -e "\n1. Mematikan node Master lama (mysql-master)..."
docker stop mysql-master

echo -e "\n2. Menghentikan replikasi & Mengubah Replica 1 menjadi Master Baru (Disable Read-Only)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = OFF;
SET GLOBAL read_only = OFF;
EOF

echo -e "\n3. Membaca data yang ada di Master Baru (mysql-replica1)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n4. Melakukan INSERT data baru pada Master Baru (mysql-replica1)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('David Failover (Skenario 2)', 'DevOps Lead');
"

echo -e "\n5. Membaca kembali data di Master Baru untuk memastikan INSERT berhasil..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n✅ Skenario 2 Selesai: Replica 1 berhasil dipromosikan menjadi Master Baru dan menerima query INSERT & SELECT."
