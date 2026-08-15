package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"distributed_database/internal/sharding"
)

func main() {
	// Buat ring hash dengan 3 Virtual Nodes per server (agar penyebaran lebih merata)
	ring := sharding.NewConsistentHash(3)

	// Daftarkan 3 server database kita ke dalam cincin
	nodes := []string{
		"http://localhost:8081", // Node A
		"http://localhost:8082", // Node B
		"http://localhost:8083", // Node C
	}
	for _, node := range nodes {
		ring.Add(node)
	}

	// Simulasi menyimpan (Write) 5 buah data
	dataToSave := map[string]string{
		"user:101": "Budi",
		"user:102": "Siti",
		"user:103": "Agus",
		"user:104": "Dian",
		"user:105": "Eko",
	}

	fmt.Println("=== PROSES PENYIMPANAN DATA (WRITE) ===")
	for key, value := range dataToSave {
		// Tanya ke cincin: "Siapa yang bertanggung jawab untuk kunci ini?"
		targetNode := ring.Get(key)
		
		url := fmt.Sprintf("%s/set?key=%s", targetNode, key)
		req, _ := http.NewRequest("POST", url, bytes.NewBufferString(value))
		client := &http.Client{}
		resp, err := client.Do(req)
		
		if err != nil {
			log.Fatalf("Gagal menyimpan ke %s: %v", targetNode, err)
		}
		
		body, _ := ioutil.ReadAll(resp.Body)
		resp.Body.Close()
		fmt.Printf("Key '%s' diarahkan ke -> %s (Response: %s)\n", key, targetNode, string(body))
	}

	fmt.Println("\n=== PROSES PENGAMBILAN DATA (READ) ===")
	// Simulasi membaca (Read) data yang sama
	for key := range dataToSave {
		// Harus diarahkan ke node yang SAMA PERSIS dengan saat menyimpan
		targetNode := ring.Get(key)
		
		url := fmt.Sprintf("%s/get?key=%s", targetNode, key)
		resp, err := http.Get(url)
		
		if err != nil {
			log.Fatalf("Gagal membaca dari %s: %v", targetNode, err)
		}
		
		body, _ := ioutil.ReadAll(resp.Body)
		resp.Body.Close()
		fmt.Printf("Membaca '%s' dari %s -> %s\n", key, targetNode, string(body))
	}
}
