#!/bin/bash
set -e

# Pindah ke direktori script agar pemanggilan script lain lancar
cd "$(dirname "$0")"

echo "=========================================================="
echo "      SKENARIO BESAR: HIGH AVAILABILITY (HA) LENGKAP      "
echo "=========================================================="

echo -e "\n[Tahap 0] Membersihkan sisa environment sebelumnya..."
docker compose -f ../docker-compose.yml down -v || true
# Kembalikan pgbouncer config jika sebelumnya di-failover
perl -pi -e 's/host=pitr_replica/host=pitr_postgres/g' ../pgbouncer/pgbouncer.ini
rm -rf ../data/* ../archive/* ../backup/* ../replica_data/*

echo -e "\n[Tahap 1] Menjalankan Inisialisasi (Memulai DB & Base Backup)..."
./1_init_and_backup.sh

echo -e "\n[Tahap 2] Memasukkan data awal ke DB..."
curl -s -X POST http://localhost:8080/transactions -H "Content-Type: application/json" -d '{"amount": 150.00, "notes": "Data Awal 1"}' > /dev/null
curl -s -X POST http://localhost:8080/transactions -H "Content-Type: application/json" -d '{"amount": 250.00, "notes": "Data Awal 2"}' > /dev/null
sleep 2

echo -e "\n[Tahap 3] Mengatur Streaming Replication (Primary -> Replica)..."
./4_setup_replication.sh
echo -e "\nMenunggu 3 detik agar replikasi stabil..."
sleep 3

echo -e "\n[Tahap 4] Mengeksekusi Failover (Mematikan Primary, Promote Replica)..."
./5_failover.sh
echo -e "\nMenunggu 3 detik agar failover stabil..."
sleep 3

echo -e "\n[Tahap 5] Mengeksekusi Failback (Resync mantan Primary dgn pg_rewind)..."
./6_failback.sh

echo -e "\n=========================================================="
echo "    SKENARIO HA LENGKAP SELESAI DENGAN SUKSES!            "
echo "=========================================================="
