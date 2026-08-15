#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE} 🚀 SKENARIO DEMO DC & DRC FAILOVER - REVERSE SYNC   ${NC}"
echo -e "${BLUE}=====================================================${NC}"

check_api() {
  echo -e "\n${YELLOW}Checking API endpoint via HAProxy (http://localhost:8080/api/notes)...${NC}"
  if command -v jq >/dev/null 2>&1; then
    curl -s http://localhost:8080/api/notes | jq .
  else
    curl -s http://localhost:8080/api/notes
  fi
  echo ""
}

case "$1" in
  "step1"|"normal")
    echo -e "\n${GREEN}[FASE 1] Memulai Operasional Normal di DC Utama...${NC}"
    docker compose up --build -d
    echo -e "${YELLOW}Menunggu service siap... (10 detik)${NC}"
    sleep 10
    
    echo -e "\n${GREEN}1. Membuat Catatan Pertama di DC Utama...${NC}"
    curl -s -X POST http://localhost:8080/api/notes \
         -H "Content-Type: application/json" \
         -d '{"title":"Catatan DC 1", "content":"Dibuat di Main DC Jakarta sebelum bencana"}'
    echo ""
    check_api
    ;;

  "step2"|"failover")
    echo -e "\n${RED}[FASE 2] Simulating Failover: Mematikan DC Utama (Jakarta)...${NC}"
    docker stop app-dc postgres-dc
    sleep 3

    echo -e "\n${YELLOW}Routing beralih ke DRC Surabaya. Mempromosikan DB DRC menjadi Read-Write...${NC}"
    docker exec postgres-drc psql -U postgres -d dcdrc_db -c "SELECT pg_promote();"
    sleep 3

    echo -e "\n${GREEN}2. Membuat Catatan Kedua di DRC Surabaya...${NC}"
    curl -s -X POST http://localhost:8080/api/notes \
         -H "Content-Type: application/json" \
         -d '{"title":"Catatan DRC 2", "content":"Dibuat di DRC Surabaya saat DC Utama mati"}'
    echo ""
    check_api
    ;;

  "step3"|"failback")
    echo -e "\n${YELLOW}[FASE 3] Reverse Sync Data dari DRC kembali ke DC Utama...${NC}"
    
    echo "1. Membuat physical replication slot di DRC..."
    docker exec postgres-drc psql -U postgres -d dcdrc_db -c "SELECT * FROM pg_create_physical_replication_slot('dc_resync_slot');" || true

    echo "2. Menyalakan postgres-dc dan melakukan pull snapshot terbaru dari DRC..."
    docker start postgres-dc
    sleep 3
    docker exec postgres-dc sh -c "
      su - postgres -c 'pg_ctl stop -D /var/lib/postgresql/data -m immediate' || true
      rm -rf /var/lib/postgresql/data/*
      PGPASSWORD=replica_password pg_basebackup -h postgres-drc -D /var/lib/postgresql/data -U replicator -vP -R -S dc_resync_slot -X stream
      chmod 700 /var/lib/postgresql/data
    "
    docker restart postgres-dc
    sleep 5

    echo "3. Mempromosikan postgres-dc kembali menjadi Primary Read-Write..."
    docker exec postgres-dc psql -U postgres -d dcdrc_db -c "SELECT pg_promote();"
    docker start app-dc
    sleep 3

    echo "4. Mengembalikan postgres-drc menjadi Standby Replica..."
    docker restart postgres-drc
    sleep 3
    docker exec -d postgres-drc sh -c "/scripts/init-drc.sh"
    sleep 5

    echo -e "\n${GREEN}✅ Failback Selesai! Verifikasi seluruh data di DC Utama:${NC}"
    check_api
    ;;

  "all")
    $0 step1
    echo -e "\n${YELLOW}Tekan Enter untuk melanjutkan ke FASE 2 (Failover ke DRC)...${NC}"
    read -r
    $0 step2
    echo -e "\n${YELLOW}Tekan Enter untuk melanjutkan ke FASE 3 (Failback & Reverse Sync ke DC)...${NC}"
    read -r
    $0 step3
    ;;

  *)
    echo "Penggunaan: $0 {normal|failover|failback|all}"
    echo "  ./run-failover-demo.sh normal   -> Fase 1: Jalankan cluster & INSERT di DC"
    echo "  ./run-failover-demo.sh failover -> Fase 2: Matikan DC, promote DRC, INSERT di DRC"
    echo "  ./run-failover-demo.sh failback -> Fase 3: Resync data DRC ke DC & aktifkan DC kembali"
    echo "  ./run-failover-demo.sh all      -> Jalankan seluruh skenario secara interaktif"
    exit 1
    ;;
esac
