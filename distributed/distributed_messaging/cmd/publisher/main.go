package main

import (
	"context"
	"log"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func main() {
	rabbitURL := os.Getenv("RABBITMQ_URL")
	if rabbitURL == "" {
		rabbitURL = "amqp://guest:guest@localhost:5672/"
	}

	conn, err := amqp.Dial(rabbitURL)
	if err != nil {
		log.Fatalf("Gagal connect ke RabbitMQ: %v", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Gagal membuka channel: %v", err)
	}
	defer ch.Close()

	// Deklarasi Exchange bertipe Fanout (Pub/Sub: kirim ke semua queue yang bind)
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
		log.Fatalf("Gagal deklarasi exchange: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Kirim pesan ke Exchange
	body := "Telah terjadi transaksi penting di sistem: #" + time.Now().Format("15:04:05")
	err = ch.PublishWithContext(ctx,
		"logs_exchange", // exchange
		"",              // routing key (diabaikan jika fanout)
		false,           // mandatory
		false,           // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(body),
		})
	if err != nil {
		log.Fatalf("Gagal mem-publish pesan: %v", err)
	}

	log.Printf("📢 [Publisher] Berhasil mengirim pesan: %s", body)
}
