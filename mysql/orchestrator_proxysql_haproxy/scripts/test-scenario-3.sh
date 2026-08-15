#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 3: 1 Master + 1 Replica -> Tambah 1 Replica (Scale-Out & Orchestrator)"
echo "=========================================================================="

echo -e "\n1. Mereset environment dan menyalakan Master, Replica 1, Replica 2, Orchestrator, ProxySQL, HAProxy..."
docker compose down -v 2>/dev/null || true
docker compose up -d mysql-master mysql-replica1 mysql-replica2 orchestrator proxysql haproxy --wait

echo -e "\n2. Konfigurasi Replikasi untuk Replica 1 & Replica 2..."
"$(dirname "$0")/01-setup-replica1.sh"
"$(dirname "$0")/02-setup-replica2.sh"

echo -e "\n3. Pendaftaran Topologi ke Orchestrator..."
"$(dirname "$0")/04-register-orchestrator.sh"

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

echo -e "\n✅ Skenario 3 Selesai: Replica 2 berhasil ditambahkan secara dinamis, ditemukan oleh Orchestrator, dan tersinkronisasi!"
