package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"sync"
	"time"

	"distributed_id_generation/internal/snowflake"
)

func main() {
	// 1. Ambil Node ID dari Environment Variable.
	// Jika ada 10 server API, jalankan dengan NODE_ID=1, NODE_ID=2, dst.
	nodeIDStr := os.Getenv("NODE_ID")
	nodeID := int64(1) // Default ke Node 1
	if nodeIDStr != "" {
		id, err := strconv.ParseInt(nodeIDStr, 10, 64)
		if err == nil {
			nodeID = id
		}
	}

	fmt.Printf("🔧 Menyalakan ID Generator di Mesin/Node ID: %d\n", nodeID)
	generator := snowflake.NewIDGenerator(nodeID)

	// Simulasi request bersamaan di dalam server yang sama.
	// Kita generate 50.000 ID menggunakan banyak Goroutine secara konkuren.
	var wg sync.WaitGroup
	var mu sync.Mutex
	
	// Set digunakan untuk mengecek duplikasi
	generatedIDs := make(map[int64]bool)
	duplicateCount := 0

	fmt.Println("🚀 Mulai men-generate 50.000 ID secara bersamaan (Konkuren)...")
	start := time.Now()

	totalRequest := 50000
	workers := 100

	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < (totalRequest / workers); j++ {
				id := generator.GenerateID()
				
				// Cek duplikasi (Simpan ke memory - hanya untuk tes)
				mu.Lock()
				if generatedIDs[id] {
					duplicateCount++
				}
				generatedIDs[id] = true
				mu.Unlock()
			}
		}()
	}

	wg.Wait()
	duration := time.Since(start)

	fmt.Println("==================================================")
	fmt.Printf("✅ Total ID yang di-generate : %d\n", len(generatedIDs))
	fmt.Printf("⏳ Waktu eksekusi            : %v\n", duration)
	fmt.Printf("❌ Jumlah ID Duplikat        : %d\n", duplicateCount)
	fmt.Println("==================================================")

	// Contoh format ID yang dihasilkan
	sampleID := generator.GenerateID()
	fmt.Printf("\nContoh ID yang dihasilkan: %d\n", sampleID)
}
