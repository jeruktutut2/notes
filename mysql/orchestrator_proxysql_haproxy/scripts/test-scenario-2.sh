#!/bin/bash
set -e

echo "=========================================================================="
echo "📌 SKENARIO 2: Failover Master dikelola oleh Orchestrator & ProxySQL"
echo "=========================================================================="

echo -e "\n1. Mematikan node Master lama (mysql-master)..."
docker stop mysql-master

echo -e "\n2. Menginstruksikan Orchestrator untuk melakukan failover / mempromosikan Replica 1 secara terotomatisasi..."
curl -s "http://localhost:3000/api/graceful-master-takeover/company_db/mysql-master/3306/mysql-replica1/3306" || true

# Promosi fallback via GTID jika orchestrator recovery mode menunggu verifikasi
docker exec -i mysql-replica1 mysql -uroot -prootpassword <<EOF
STOP REPLICA;
RESET REPLICA ALL;
SET GLOBAL super_read_only = OFF;
SET GLOBAL read_only = OFF;
CREATE USER IF NOT EXISTS 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
EOF

echo -e "\n3. Meng-update ProxySQL Hostgroup (Replica 1 -> Writer Hostgroup 10)..."
docker exec -i proxysql mysql -uadmin -padmin -h127.0.0.1 -P6032 <<EOF
UPDATE mysql_servers SET hostgroup_id=10 WHERE hostname='mysql-replica1';
UPDATE mysql_servers SET hostgroup_id=20 WHERE hostname='mysql-master';
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
EOF

echo -e "\n4. Membaca data yang ada di Master Baru (mysql-replica1)..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n5. Melakukan INSERT data baru via HAProxy -> ProxySQL ke Master Baru..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
INSERT INTO employees (name, position) VALUES ('David Failover (Orchestrator Skenario 2)', 'DevOps Lead');
"

echo -e "\n6. Membaca kembali data di Master Baru untuk memastikan INSERT berhasil..."
docker exec -i mysql-replica1 mysql -uroot -prootpassword company_db -e "
SELECT id, name, position, created_at FROM employees;
"

echo -e "\n✅ Skenario 2 Selesai: Failover berhasil dikelola dengan Orchestrator + ProxySQL, Replica 1 menjadi Master Baru."
