package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	clientv3 "go.etcd.io/etcd/client/v3"
	"go.etcd.io/etcd/client/v3/concurrency"
)

func main() {
	nodeID := os.Getenv("NODE_ID")
	if nodeID == "" {
		nodeID = "Node-X"
	}

	log.Printf("🤖 [%s] Menyala. Mencoba terhubung ke etcd...", nodeID)

	// 1. Konek ke klaster etcd
	cli, err := clientv3.New(clientv3.Config{
		Endpoints:   []string{"localhost:2379"},
		DialTimeout: 5 * time.Second,
	})
	if err != nil {
		log.Fatalf("Gagal connect ke etcd: %v", err)
	}
	defer cli.Close()

	// 2. Buat sesi (Session) yang memiliki *lease* (TTL)
	// Jika node ini mati tiba-tiba, sesi akan kadaluarsa dan melepaskan jabatan Leader
	session, err := concurrency.NewSession(cli, concurrency.WithTTL(5))
	if err != nil {
		log.Fatalf("Gagal membuat sesi: %v", err)
	}
	defer session.Close()

	// 3. Buat objek Election dengan nama "my-election"
	// Semua node yang bergabung dengan nama yang sama akan bersaing
	election := concurrency.NewElection(session, "/my-election")

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Tangkap sinyal CTRL+C agar bisa resign (mundur dari leader) dengan anggun
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		log.Printf("🛑 [%s] Menerima sinyal mati. Mundur dari jabatan (Resign)...", nodeID)
		election.Resign(context.Background())
		cancel()
		os.Exit(0)
	}()

	// 4. Bersaing menjadi Leader (Blokir sampai berhasil jadi leader)
	log.Printf("⏳ [%s] Mengantre menjadi LEADER...", nodeID)
	
	// Fungsi Campaign() akan menahan eksekusi (nge-block) JIKA ada node lain yang sedang memegang jabatan Leader.
	// Baris di bawah ini baru akan terlewati jika node ini dinobatkan sebagai Leader.
	if err := election.Campaign(ctx, nodeID); err != nil {
		log.Fatalf("Kesalahan saat kampanye: %v", err)
	}

	// === ZONA LEADER ===
	// Mulai dari titik ini, Node kita sudah resmi menjadi LEADER.
	log.Printf("👑 [%s] SAYA SEKARANG LEADER!", nodeID)
	
	// Simulasi tugas eksklusif sang Leader
	for i := 1; i <= 5; i++ {
		log.Printf("👑 [%s] Mengerjakan tugas khusus leader... (%d/5)", nodeID, i)
		time.Sleep(2 * time.Second)
	}

	// Setelah selesai, sang Leader memilih untuk mundur (Resign)
	log.Printf("👋 [%s] Pekerjaan selesai. Saya mundur (Resign) dari Leader.", nodeID)
	
	// Resign akan memberikan kesempatan pada node lain yang sedang mengantre (ng-block di fungsi Campaign)
	if err := election.Resign(context.Background()); err != nil {
		log.Printf("Gagal resign: %v", err)
	}
}
