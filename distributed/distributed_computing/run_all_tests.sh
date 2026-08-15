#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Computing (MapReduce)"
echo "====================================================="

echo "[1/3] Build Master & Worker..."
go build -o mr_master cmd/master/main.go
go build -o mr_worker cmd/worker/main.go

echo "[2/3] Menyalakan Master di background..."
./mr_master &
MASTER_PID=$!
sleep 1

echo "[3/3] Menyalakan 3 Worker secara bersamaan..."
echo "-----------------------------------------------------"
WORKER_ID="Worker-A" ./mr_worker &
WORKER_A_PID=$!

WORKER_ID="Worker-B" ./mr_worker &
WORKER_B_PID=$!

WORKER_ID="Worker-C" ./mr_worker &
WORKER_C_PID=$!

echo "Semua node berjalan! Silakan amati bagaimana Master mendistribusikan task (Map & Reduce) secara adil ke Worker A, B, dan C melalui RPC."
echo "-----------------------------------------------------"

# Tunggu master selesai (script master akan exit otomatis jika pekerjaan selesai)
wait $MASTER_PID

echo ""
echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $WORKER_A_PID $WORKER_B_PID $WORKER_C_PID 2>/dev/null || true
rm -f mr_master mr_worker
echo "🎉 Selesai!"
