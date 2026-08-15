#!/bin/bash
set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/backups/app_db_backup_${TIMESTAMP}.sql"
LATEST_BACKUP_LINK="/backups/app_db_latest.sql"

echo "=========================================================================="
echo "   TAHAP 3: PENGUJIAN AUTOMATED BACKUP & DISASTER RECOVERY RESTORE"
echo "=========================================================================="

echo "[1/4] Menjalankan Logical Backup dari Backup Agent Container..."
docker exec -i backup-agent bash -c "
mkdir -p /backups
pg_dump -h citus-coordinator -U postgres -d app_db --clean --if-exists > ${BACKUP_FILE}
cp ${BACKUP_FILE} ${LATEST_BACKUP_LINK}
"
echo "File backup berhasil dibuat: ${BACKUP_FILE}"
ls -lh ./backups/

echo "[2/4] Menyiapkan Database Baru 'restore_db' untuk Simulasi Disaster Recovery..."
docker exec -i citus-coordinator psql -U postgres -c "DROP DATABASE IF EXISTS restore_db;"
docker exec -i citus-coordinator psql -U postgres -c "CREATE DATABASE restore_db;"

echo "[3/4] Melakukan Pemulihan (Restore) Data dari Backup ke 'restore_db'..."
docker exec -i backup-agent bash -c "
psql -h citus-coordinator -U postgres -d restore_db -f ${LATEST_BACKUP_LINK}
"

echo "[4/4] Verifikasi Integritas Data Hasil Restore..."
ORIGINAL_COUNT=$(docker exec -i citus-coordinator psql -U postgres -d app_db -t -c "SELECT count(*) FROM users;" | tr -d ' ')
RESTORED_COUNT=$(docker exec -i citus-coordinator psql -U postgres -d restore_db -t -c "SELECT count(*) FROM users;" | tr -d ' ')

echo "Jumlah Record Original (app_db)   : ${ORIGINAL_COUNT}"
echo "Jumlah Record Restored (restore_db): ${RESTORED_COUNT}"

if [ "${ORIGINAL_COUNT}" -eq "${RESTORED_COUNT}" ]; then
    echo "SUCCESS: Integritas Data 100% Cocok!"
else
    echo "ERROR: Data Mismatch setelah restore!"
    exit 1
fi

echo "=========================================================================="
echo "   TAHAP 3 BERHASIL DIVERIFIKASI!"
echo "=========================================================================="
