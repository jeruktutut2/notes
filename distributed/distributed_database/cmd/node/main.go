package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

func main() {
	nodeID := os.Getenv("NODE_ID")
	if nodeID == "" {
		nodeID = "Unknown-Node"
	}
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// In-memory Database (Sangat Sederhana)
	database := make(map[string]string)

	http.HandleFunc("/set", func(w http.ResponseWriter, r *http.Request) {
		key := r.URL.Query().Get("key")
		if key == "" {
			http.Error(w, "Key is required", http.StatusBadRequest)
			return
		}
		
		body, _ := ioutil.ReadAll(r.Body)
		value := string(body)
		
		database[key] = value
		log.Printf("[%s] Menyimpan data: %s => %s", nodeID, key, value)
		
		fmt.Fprintf(w, "OK. Disimpan di %s", nodeID)
	})

	http.HandleFunc("/get", func(w http.ResponseWriter, r *http.Request) {
		key := r.URL.Query().Get("key")
		value, exists := database[key]
		if !exists {
			log.Printf("[%s] Data tidak ditemukan: %s", nodeID, key)
			http.Error(w, "Not Found", http.StatusNotFound)
			return
		}
		
		log.Printf("[%s] Mengambil data: %s", nodeID, key)
		fmt.Fprintf(w, "%s (Data ini di-host oleh %s)", value, nodeID)
	})

	// Route khusus untuk menampilkan seluruh data (debug)
	http.HandleFunc("/dump", func(w http.ResponseWriter, r *http.Request) {
		var output []string
		for k, v := range database {
			output = append(output, fmt.Sprintf("%s: %s", k, v))
		}
		fmt.Fprintf(w, "=== Data di %s ===\n%s", nodeID, strings.Join(output, "\n"))
	})

	log.Printf("🗄️ Database Node [%s] berjalan di port %s", nodeID, port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
