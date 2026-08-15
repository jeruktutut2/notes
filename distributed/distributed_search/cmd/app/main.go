package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"strings"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
)

// Artikel merepresentasikan dokumen yang akan kita simpan di Elasticsearch
type Artikel struct {
	ID      string `json:"id"`
	Judul   string `json:"judul"`
	Konten  string `json:"konten"`
	Kategori string `json:"kategori"`
}

func main() {
	// 1. Inisialisasi Elasticsearch Client
	cfg := elasticsearch.Config{
		Addresses: []string{"http://localhost:9200"},
	}
	es, err := elasticsearch.NewClient(cfg)
	if err != nil {
		log.Fatalf("Error creating the client: %s", err)
	}

	// Cek koneksi
	res, err := es.Info()
	if err != nil {
		log.Fatalf("Error getting response: %s", err)
	}
	defer res.Body.Close()
	log.Println("✅ Berhasil terhubung ke Elasticsearch")

	indexName := "artikel_tech"

	// 2. Data Dummy untuk di-index
	data := []Artikel{
		{ID: "1", Judul: "Belajar Golang Dasar", Konten: "Golang adalah bahasa yang sangat cepat dan dibuat oleh Google. Cocok untuk backend.", Kategori: "Pemrograman"},
		{ID: "2", Judul: "Mengenal Distributed Systems", Konten: "Sistem terdistribusi membagi beban ke banyak server. Konsepnya sulit tapi seru.", Kategori: "Arsitektur"},
		{ID: "3", Judul: "Tutorial Elasticsearch", Konten: "Elasticsearch menggunakan inverted index untuk pencarian teks super cepat seperti Google.", Kategori: "Database"},
		{ID: "4", Judul: "Go untuk Backend", Konten: "Banyak perusahaan pindah ke Go karena performa concurrency yang luar biasa.", Kategori: "Pemrograman"},
	}

	// 3. Proses Indexing (Menyimpan data ke Elasticsearch)
	log.Println("📥 Mulai memasukkan (Indexing) data artikel...")
	for _, doc := range data {
		docJSON, _ := json.Marshal(doc)
		req := bytes.NewReader(docJSON)

		res, err := es.Index(
			indexName,
			req,
			es.Index.WithDocumentID(doc.ID),
			es.Index.WithRefresh("true"), // Paksa refresh agar langsung bisa dicari
		)
		if err != nil {
			log.Fatalf("Gagal index dokumen %s: %s", doc.ID, err)
		}
		res.Body.Close()
	}
	log.Println("✅ 4 Artikel berhasil di-index.")

	// Jeda sejenak untuk memastikan index siap
	time.Sleep(1 * time.Second)

	// 4. Proses Pencarian Teks Bebas (Full-Text Search)
	keyword := "go backend"
	log.Printf("\n🔍 Mencari artikel dengan kata kunci: '%s'\n", keyword)

	// Query JSON untuk Elasticsearch (Mencari di field 'Judul' atau 'Konten')
	query := fmt.Sprintf(`{
		"query": {
			"multi_match": {
				"query": "%s",
				"fields": ["judul", "konten"]
			}
		}
	}`, keyword)

	res, err = es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex(indexName),
		es.Search.WithBody(strings.NewReader(query)),
		es.Search.WithTrackTotalHits(true),
		es.Search.WithPretty(),
	)
	if err != nil {
		log.Fatalf("Error getting response: %s", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		log.Fatalf("Error dari Elasticsearch: %s", res.String())
	}

	// Parse Response JSON
	var result map[string]interface{}
	if err := json.NewDecoder(res.Body).Decode(&result); err != nil {
		log.Fatalf("Error parsing the response body: %s", err)
	}

	// Tampilkan Hasil
	hits := result["hits"].(map[string]interface{})["hits"].([]interface{})
	fmt.Printf("Ditemukan %d artikel yang relevan:\n", len(hits))
	fmt.Println("-----------------------------------------------------")
	for i, hit := range hits {
		source := hit.(map[string]interface{})["_source"].(map[string]interface{})
		score := hit.(map[string]interface{})["_score"].(float64)
		
		fmt.Printf("%d. [Skor: %.2f] %s\n", i+1, score, source["judul"])
		fmt.Printf("   %s\n", source["konten"])
		fmt.Println("-----------------------------------------------------")
	}
}
