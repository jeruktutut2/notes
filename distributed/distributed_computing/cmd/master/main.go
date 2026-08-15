package main

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"net/rpc"
	"sync"
	"time"

	"distributed_computing/internal/mapreduce"
)

type Master struct {
	mu           sync.Mutex
	mapTasks     []string
	mapDone      int
	reduceDone   int
	totalMaps    int
	totalReduces int
}

func (m *Master) GetTask(args *struct{}, reply *mapreduce.Task) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	// 1. Apakah masih ada Map task?
	if m.mapDone < m.totalMaps {
		for i, filename := range m.mapTasks {
			if filename != "" {
				reply.Type = mapreduce.TaskTypeMap
				reply.TaskID = i
				reply.Filename = filename
				// Tandai task sedang diproses (dihapus sementara dari daftar antrean)
				m.mapTasks[i] = "" 
				log.Printf("Memberikan Map Task #%d (%s)", i, filename)
				return nil
			}
		}
		reply.Type = mapreduce.TaskTypeWait
		return nil
	}

	// 2. Jika Map selesai, apakah masih ada Reduce task?
	if m.reduceDone < m.totalReduces {
		// Sederhananya, kita asumsikan hanya ada 1 Reduce task untuk simulasi ini
		reply.Type = mapreduce.TaskTypeReduce
		reply.TaskID = 0
		log.Printf("Memberikan Reduce Task")
		m.reduceDone++ // Anggap langsung selesai (tanpa retry di simulasi ini)
		return nil
	}

	// 3. Semua selesai
	reply.Type = mapreduce.TaskTypeExit
	return nil
}

func (m *Master) ReportTask(args *mapreduce.TaskResult, reply *struct{}) error {
	m.mu.Lock()
	defer m.mu.Unlock()

	if args.Type == mapreduce.TaskTypeMap {
		m.mapDone++
		log.Printf("Map Task #%d Selesai! (Total Map Done: %d/%d)", args.TaskID, m.mapDone, m.totalMaps)
	} else if args.Type == mapreduce.TaskTypeReduce {
		log.Printf("Reduce Task Selesai!")
	}
	return nil
}

func main() {
	// Dummy data (3 file yang perlu diproses)
	files := []string{"data_1.txt", "data_2.txt", "data_3.txt"}
	
	m := &Master{
		mapTasks:     files,
		totalMaps:    len(files),
		totalReduces: 1,
	}

	rpc.RegisterName("MasterRPC", m)
	rpc.HandleHTTP()
	
	l, err := net.Listen("tcp", ":1234")
	if err != nil {
		log.Fatal("Master error:", err)
	}

	log.Println("🧠 Master berjalan di port :1234...")
	
	go http.Serve(l, nil)

	// Tunggu sampai semua beres
	for {
		m.mu.Lock()
		if m.mapDone == m.totalMaps && m.reduceDone == m.totalReduces {
			m.mu.Unlock()
			break
		}
		m.mu.Unlock()
		time.Sleep(1 * time.Second)
	}
	
	log.Println("✅ Semua pekerjaan MapReduce telah selesai. Master berhenti.")
	time.Sleep(1 * time.Second) // Beri waktu worker untuk menerima status EXIT
}
