package db

import (
	"database/sql"
	"log"
	"os"
	"time"

	_ "github.com/lib/pq"
)

var DB *sql.DB

// Connect membuka koneksi ke PostgreSQL db_rekam_medis dan membuat tabel jika belum ada.
// PENTING: Service B HANYA boleh connect ke db_rekam_medis, tidak ke db_pendaftaran.
func Connect() {
	dsn := os.Getenv("DB_URL")
	if dsn == "" {
		dsn = "postgres://admin:secret123@localhost:5434/db_rekam_medis?sslmode=disable"
	}

	var lastErr error
	connected := false
	for i := 0; i < 10; i++ {
		var openErr error
		DB, openErr = sql.Open("postgres", dsn)
		if openErr != nil {
			lastErr = openErr
		} else if pingErr := DB.Ping(); pingErr != nil {
			lastErr = pingErr
		} else {
			connected = true
			break
		}
		log.Printf("[Service-B][DB] Koneksi gagal (retry ke-%d): %v", i+1, lastErr)
		time.Sleep(3 * time.Second)
	}

	if !connected {
		log.Fatalf("[Service-B][DB] Tidak bisa connect ke database setelah 10 percobaan: %v", lastErr)
	}

	log.Println("[Service-B][DB] Koneksi ke db_rekam_medis berhasil.")
	createTable()
}

func createTable() {
	query := `
	CREATE TABLE IF NOT EXISTS medical_records (
		id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		patient_id   VARCHAR(255) NOT NULL,
		name         VARCHAR(255),
		nik          VARCHAR(16) UNIQUE NOT NULL,
		diagnosis    TEXT DEFAULT 'Draft - Belum ada diagnosis',
		notes        TEXT DEFAULT 'Rekam medis otomatis dibuat saat pendaftaran',
		created_at   TIMESTAMP DEFAULT NOW(),
		updated_at   TIMESTAMP DEFAULT NOW()
	);`

	_, err := DB.Exec(query)
	if err != nil {
		log.Fatalf("[Service-B][DB] Gagal membuat tabel medical_records: %v", err)
	}
	log.Println("[Service-B][DB] Tabel medical_records siap.")
}
