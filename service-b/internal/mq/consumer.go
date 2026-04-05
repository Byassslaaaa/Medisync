package mq

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"hospital/service-b/internal/db"

	amqp "github.com/rabbitmq/amqp091-go"
)

const (
	exchangeName = "hospital"
	queueName    = "patient.queue"
	routingKey   = "patient.registered"
)

// PatientEvent adalah struktur pesan yang diterima dari RabbitMQ.
// Harus identik dengan PatientEvent di service-a/internal/mq/producer.go.
type PatientEvent struct {
	PatientID    string `json:"patient_id"`
	Name         string `json:"name"`
	NIK          string `json:"nik"`
	TanggalLahir string `json:"tanggal_lahir"`
	NoTelepon    string `json:"no_telepon"`
	Timestamp    string `json:"timestamp"`
}

// Start menginisialisasi consumer dengan reconnect loop otomatis.
// Jika koneksi ke RabbitMQ putus (broker restart), consumer akan
// mencoba reconnect setiap 5 detik tanpa perlu restart service.
// Dipanggil di goroutine terpisah dari main.go.
func Start() {
	url := os.Getenv("RABBITMQ_URL")
	if url == "" {
		url = "amqp://guest:guest@localhost:5672/"
	}

	// Outer loop: reconnect otomatis jika koneksi putus
	for {
		log.Println("[Service-B][MQ] Mencoba koneksi ke RabbitMQ...")
		err := runConsumer(url)
		if err != nil {
			log.Printf("[Service-B][MQ] ✗ Consumer berhenti: %v. Reconnect dalam 5 detik...", err)
			time.Sleep(5 * time.Second)
		}
	}
}

// runConsumer membuka koneksi, mendeklarasikan exchange/queue/binding,
// lalu memproses pesan. Mengembalikan error jika koneksi/channel putus.
func runConsumer(url string) error {
	var conn *amqp.Connection
	var err error

	// Retry loop saat startup awal
	for i := 0; i < 15; i++ {
		conn, err = amqp.Dial(url)
		if err == nil {
			break
		}
		log.Printf("[Service-B][MQ] Gagal connect ke RabbitMQ (retry ke-%d): %v", i+1, err)
		time.Sleep(4 * time.Second)
	}
	if err != nil {
		return err
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		return err
	}
	defer ch.Close()

	// Deklarasi exchange — harus cocok dengan producer (Service A)
	if err = ch.ExchangeDeclare(exchangeName, "direct", true, false, false, false, nil); err != nil {
		return err
	}

	// Deklarasi queue
	q, err := ch.QueueDeclare(queueName, true, false, false, false, nil)
	if err != nil {
		return err
	}

	// Bind queue ke exchange dengan routing key
	if err = ch.QueueBind(q.Name, routingKey, exchangeName, false, nil); err != nil {
		return err
	}

	msgs, err := ch.Consume(q.Name, "", false, false, false, false, nil)
	if err != nil {
		return err
	}

	log.Printf("[Service-B][MQ] Consumer aktif. Mendengarkan queue '%s'...", queueName)

	// Deteksi koneksi putus melalui channel notifikasi
	connClose := conn.NotifyClose(make(chan *amqp.Error, 1))

	for {
		select {
		case msg, ok := <-msgs:
			if !ok {
				// Channel ditutup (RabbitMQ disconnect)
				return fmt.Errorf("msgs channel ditutup")
			}
			processEvent(msg)
		case err := <-connClose:
			if err != nil {
				return fmt.Errorf("koneksi RabbitMQ putus: %v", err)
			}
			return fmt.Errorf("koneksi RabbitMQ ditutup")
		}
	}
}

// processEvent memproses event 'patient.registered' dan membuat draft rekam medis.
func processEvent(msg amqp.Delivery) {
	var event PatientEvent
	if err := json.Unmarshal(msg.Body, &event); err != nil {
		log.Printf("[Service-B][MQ] ✗ Gagal parse pesan: %v", err)
		msg.Nack(false, false) // buang pesan rusak
		return
	}

	log.Printf("[Service-B][MQ] ← Event diterima: patient.registered untuk PatientID=%s, NIK=%s", event.PatientID, event.NIK)

	// Insert draft rekam medis ke db_rekam_medis
	// PENTING: Service B hanya query ke database-nya sendiri
	query := `
		INSERT INTO medical_records (patient_id, name, nik, diagnosis, notes)
		VALUES ($1, $2, $3, $4, $5)
		ON CONFLICT (nik) DO NOTHING
	`
	_, err := db.DB.Exec(query,
		event.PatientID,
		event.Name,
		event.NIK,
		"Draft - Belum ada diagnosis",
		"Rekam medis otomatis dibuat saat pendaftaran pada "+event.Timestamp,
	)

	if err != nil {
		log.Printf("[Service-B][MQ] ✗ Gagal INSERT rekam medis untuk NIK %s: %v", event.NIK, err)
		msg.Nack(false, true) // requeue agar dicoba lagi
		return
	}

	log.Printf("[Service-B][MQ] ✓ Draft rekam medis berhasil dibuat untuk PatientID=%s", event.PatientID)
	msg.Ack(false) // konfirmasi pesan sudah diproses
}
