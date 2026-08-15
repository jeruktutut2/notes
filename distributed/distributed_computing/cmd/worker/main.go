package main

import (
	"log"
	"os"
	"time"

	"distributed_computing/internal/mapreduce"
)

func main() {
	workerID := os.Getenv("WORKER_ID")
	if workerID == "" {
		workerID = "Worker-Unknown"
	}

	log.Printf("👷 %s menyala. Menunggu instruksi dari Master...", workerID)

	for {
		task := mapreduce.CallGetTask()

		switch task.Type {
		case mapreduce.TaskTypeMap:
			log.Printf("[%s] Menerima Map Task #%d (File: %s)", workerID, task.TaskID, task.Filename)
			
			// Simulasi proses komputasi berat (Menghitung kata di file)
			time.Sleep(2 * time.Second)
			log.Printf("[%s] Selesai Map Task #%d", workerID, task.TaskID)
			
			// Lapor ke master
			mapreduce.CallReportTask(&mapreduce.TaskResult{
				Type:   mapreduce.TaskTypeMap,
				TaskID: task.TaskID,
			})

		case mapreduce.TaskTypeReduce:
			log.Printf("[%s] Menerima Reduce Task", workerID)
			
			// Simulasi penggabungan hasil Map
			time.Sleep(3 * time.Second)
			log.Printf("[%s] Selesai Reduce Task!", workerID)
			
			mapreduce.CallReportTask(&mapreduce.TaskResult{
				Type:   mapreduce.TaskTypeReduce,
				TaskID: task.TaskID,
			})

		case mapreduce.TaskTypeWait:
			// log.Printf("[%s] Belum ada task, menunggu...", workerID)
			time.Sleep(1 * time.Second)

		case mapreduce.TaskTypeExit:
			log.Printf("[%s] Semua tugas MapReduce selesai. Worker berhenti.", workerID)
			return
		}
	}
}
