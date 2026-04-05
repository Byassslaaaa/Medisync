package db

import (
	"database/sql"
	"log"
	"os"
	"time"

	_ "github.com/lib/pq"
)

var DB *sql.DB

// Connect membuka koneksi ke PostgreSQL db_pendaftaran dan membuat tabel jika belum ada.
func Connect() {
	dsn := os.Getenv("DB_URL")
	if dsn == "" {
		dsn = "postgres://admin:secret123@localhost:5432/db_pendaftaran?sslmode=disable"
	}

	var lastErr error
	connected := false
	// Retry loop: tunggu hingga postgres siap
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
		log.Printf("[Service-A][DB] Koneksi gagal (retry ke-%d): %v", i+1, lastErr)
		time.Sleep(3 * time.Second)
	}

	if !connected {
		log.Fatalf("[Service-A][DB] Tidak bisa connect ke database setelah 10 percobaan: %v", lastErr)
	}

	log.Println("[Service-A][DB] Koneksi ke db_pendaftaran berhasil.")
	createTable()
}

func createTable() {
	query := `
	CREATE TABLE IF NOT EXISTS patients (
		id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		name          VARCHAR(255) NOT NULL,
		nik           VARCHAR(16)  UNIQUE NOT NULL,
		tanggal_lahir DATE         NOT NULL,
		no_telepon    VARCHAR(20),
		created_at    TIMESTAMP    DEFAULT NOW()
	);`

	_, err := DB.Exec(query)
	if err != nil {
		log.Fatalf("[Service-A][DB] Gagal membuat tabel patients: %v", err)
	}
	log.Println("[Service-A][DB] Tabel patients siap.")
}
