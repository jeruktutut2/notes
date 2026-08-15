package main

import (
	"log"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
)

func main() {
	appID := os.Getenv("APP_ID")
	if appID == "" {
		appID = "Subscriber-Unknown"
	}

	rabbitURL := os.Getenv("RABBITMQ_URL")
	if rabbitURL == "" {
		rabbitURL = "amqp://guest:guest@localhost:5672/"
	}

	conn, err := amqp.Dial(rabbitURL)
	if err != nil {
		log.Fatalf("[%s] Gagal connect ke RabbitMQ: %v", appID, err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("[%s] Gagal membuka channel: %v", appID, err)
	}
	defer ch.Close()

	// 1. Pastikan Exchange ada
	err = ch.ExchangeDeclare(
		"logs_exchange", // name
		"fanout",        // type
		true,            // durable
		false,           // auto-deleted
		false,           // internal
		false,           // no-wait
		nil,             // arguments
	)
	if err != nil {
		log.Fatalf("[%s] Gagal deklarasi exchange: %v", appID, err)
	}

	// 2. Deklarasi Queue khusus (exclusive) untuk subscriber ini saja
	q, err := ch.QueueDeclare(
		"",    // nama kosong -> RabbitMQ akan buatkan nama random
		false, // durable
		false, // delete when unused
		true,  // exclusive (hanya milik koneksi ini, dihapus jika diskonek)
		false, // no-wait
		nil,   // arguments
	)
	if err != nil {
		log.Fatalf("[%s] Gagal membuat queue: %v", appID, err)
	}

	// 3. Bind (Hubungkan) Queue ini ke Exchange
	err = ch.QueueBind(
		q.Name,          // queue name
		"",              // routing key
		"logs_exchange", // exchange
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("[%s] Gagal bind queue ke exchange: %v", appID, err)
	}

	// 4. Consume pesan
	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	if err != nil {
		log.Fatalf("[%s] Gagal register consumer: %v", appID, err)
	}

	log.Printf("🎧 [%s] Menunggu pesan (Pub/Sub). Tekan CTRL+C untuk exit.", appID)
	
	// channel blocking agar aplikasi tidak berhenti
	var forever chan struct{}
	
	go func() {
		for d := range msgs {
			log.Printf("📥 [%s] Menerima broadcast: %s", appID, d.Body)
		}
	}()

	<-forever
}
