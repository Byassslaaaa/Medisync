package mq

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

var (
	ch      *amqp.Channel
	mqConn  *amqp.Connection
	mqURL   string
)

const (
	exchangeName = "hospital"
	routingKey   = "patient.registered"
)

// PatientEvent adalah struktur event yang dikirim ke RabbitMQ saat pasien baru didaftarkan.
type PatientEvent struct {
	PatientID     string `json:"patient_id"`
	Name          string `json:"name"`
	NIK           string `json:"nik"`
	TanggalLahir  string `json:"tanggal_lahir"`
	NoTelepon     string `json:"no_telepon"`
	Timestamp     string `json:"timestamp"`
}

// Connect membuka koneksi ke RabbitMQ dan mendeklarasikan exchange.
func Connect() {
	mqURL = os.Getenv("RABBITMQ_URL")
	if mqURL == "" {
		mqURL = "amqp://guest:guest@localhost:5672/"
	}

	var err error

	// Retry loop: RabbitMQ butuh waktu untuk ready saat docker-compose up
	for i := 0; i < 15; i++ {
		mqConn, err = amqp.Dial(mqURL)
		if err == nil {
			break
		}
		log.Printf("[Service-A][MQ] Gagal connect ke RabbitMQ, retry ke-%d...", i+1)
		time.Sleep(4 * time.Second)
	}

	if err != nil {
		log.Fatalf("[Service-A][MQ] Tidak bisa connect ke RabbitMQ: %v", err)
	}

	if err = setupChannel(); err != nil {
		log.Fatalf("[Service-A][MQ] Gagal setup channel: %v", err)
	}

	log.Printf("[Service-A][MQ] Koneksi ke RabbitMQ berhasil. Exchange '%s' siap.", exchangeName)
}

// setupChannel membuat channel baru dan mendeklarasikan exchange.
func setupChannel() error {
	var err error
	ch, err = mqConn.Channel()
	if err != nil {
		return err
	}
	return ch.ExchangeDeclare(
		exchangeName,
		"direct",
		true,  // durable
		false, // auto-deleted
		false, // internal
		false, // no-wait
		nil,
	)
}

// reconnect mencoba membuka ulang koneksi dan channel ke RabbitMQ.
func reconnect() error {
	log.Println("[Service-A][MQ] Reconnecting ke RabbitMQ...")
	var err error
	for i := 0; i < 5; i++ {
		mqConn, err = amqp.Dial(mqURL)
		if err == nil {
			break
		}
		time.Sleep(3 * time.Second)
	}
	if err != nil {
		return err
	}
	return setupChannel()
}

// PublishPatientRegistered mengirimkan event ke RabbitMQ saat pasien baru berhasil didaftarkan.
// Ini adalah komunikasi ASYNCHRONOUS — Service A tidak menunggu Service B memproses event ini.
// Jika channel/koneksi putus, akan mencoba reconnect sekali sebelum return error.
func PublishPatientRegistered(event PatientEvent) error {
	body, err := json.Marshal(event)
	if err != nil {
		return err
	}

	err = publish(body)
	if err != nil {
		// Channel mungkin putus — coba reconnect sekali
		log.Printf("[Service-A][MQ] Channel error, mencoba reconnect: %v", err)
		if reconnErr := reconnect(); reconnErr != nil {
			log.Printf("[Service-A][MQ] ✗ Reconnect gagal: %v", reconnErr)
			return err
		}
		// Coba publish ulang setelah reconnect
		err = publish(body)
	}

	if err != nil {
		log.Printf("[Service-A][MQ] ✗ Gagal publish event: %v", err)
		return err
	}

	log.Printf("[Service-A][MQ] ✓ Event 'patient.registered' berhasil dikirim untuk PatientID: %s", event.PatientID)
	return nil
}

func publish(body []byte) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	return ch.PublishWithContext(ctx,
		exchangeName,
		routingKey,
		false,
		false,
		amqp.Publishing{
			ContentType:  "application/json",
			DeliveryMode: amqp.Persistent,
			Body:         body,
		},
	)
}
