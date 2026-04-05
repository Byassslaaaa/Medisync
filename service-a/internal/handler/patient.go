package handler

import (
	"log"
	"net/http"
	"time"

	"hospital/service-a/internal/db"
	grpcclient "hospital/service-a/internal/grpc"
	"hospital/service-a/internal/mq"

	"github.com/gin-gonic/gin"
)

// RegisterPatientRequest adalah struktur input dari Frontend
type RegisterPatientRequest struct {
	Name         string `json:"name"          binding:"required"`
	NIK          string `json:"nik"           binding:"required,len=16"`
	TanggalLahir string `json:"tanggal_lahir" binding:"required"` // format: YYYY-MM-DD
	NoTelepon    string `json:"no_telepon"`
}

// PatientResponse adalah struktur response ke Frontend
type PatientResponse struct {
	PatientID    string `json:"patient_id"`
	Name         string `json:"name"`
	NIK          string `json:"nik"`
	TanggalLahir string `json:"tanggal_lahir"`
	NoTelepon    string `json:"no_telepon"`
	RegisteredAt string `json:"registered_at"`
}

// RegisterPatient menangani POST /api/patients
// Alur: validasi → cek gRPC → simpan DB → publish MQ → return response
func RegisterPatient(c *gin.Context) {
	var req RegisterPatientRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"message": "Input tidak valid: " + err.Error(),
		})
		return
	}

	log.Printf("[Service-A][Handler] Permintaan pendaftaran masuk: NIK=%s, Name=%s", req.NIK, req.Name)

	// ─── STEP 1: gRPC ke Service B — cek rekam medis (SYNCHRONOUS) ───
	log.Printf("[Service-A][Handler] → Mengecek rekam medis via gRPC untuk NIK: %s", req.NIK)
	hasRecord, _, err := grpcclient.CheckPatientRecord(req.NIK)
	if err != nil {
		log.Printf("[Service-A][Handler] ✗ gRPC error: %v", err)
		c.JSON(http.StatusServiceUnavailable, gin.H{
			"success": false,
			"message": "Service rekam medis tidak tersedia. Coba lagi.",
		})
		return
	}

	if hasRecord {
		log.Printf("[Service-A][Handler] Pasien dengan NIK %s sudah terdaftar.", req.NIK)
		c.JSON(http.StatusConflict, gin.H{
			"success": false,
			"message": "Pasien dengan NIK ini sudah pernah terdaftar dalam sistem rekam medis.",
		})
		return
	}

	// ─── STEP 2: Simpan ke PostgreSQL db_pendaftaran ───
	var patientID string
	var registeredAt time.Time

	query := `
		INSERT INTO patients (name, nik, tanggal_lahir, no_telepon)
		VALUES ($1, $2, $3, $4)
		RETURNING id, created_at
	`
	err = db.DB.QueryRow(query, req.Name, req.NIK, req.TanggalLahir, req.NoTelepon).
		Scan(&patientID, &registeredAt)

	if err != nil {
		log.Printf("[Service-A][Handler] ✗ Gagal INSERT ke DB: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"message": "Gagal menyimpan data pasien.",
		})
		return
	}

	log.Printf("[Service-A][Handler] ✓ Pasien berhasil disimpan ke DB. PatientID: %s", patientID)

	// ─── STEP 3: Publish event ke RabbitMQ (ASYNCHRONOUS) ───
	// Service A tidak menunggu Service B selesai memproses event ini
	event := mq.PatientEvent{
		PatientID:    patientID,
		Name:         req.Name,
		NIK:          req.NIK,
		TanggalLahir: req.TanggalLahir,
		NoTelepon:    req.NoTelepon,
		Timestamp:    time.Now().Format(time.RFC3339),
	}

	go func() {
		// Publish di goroutine agar tidak memblok response ke client
		if err := mq.PublishPatientRegistered(event); err != nil {
			log.Printf("[Service-A][Handler] ✗ Gagal publish event: %v", err)
		}
	}()

	// ─── STEP 4: Return response ke Frontend ───
	log.Printf("[Service-A][Handler] ✓ Pendaftaran selesai. Returning response ke Frontend.")
	c.JSON(http.StatusCreated, gin.H{
		"success": true,
		"message": "Pasien berhasil didaftarkan.",
		"data": PatientResponse{
			PatientID:    patientID,
			Name:         req.Name,
			NIK:          req.NIK,
			TanggalLahir: req.TanggalLahir,
			NoTelepon:    req.NoTelepon,
			RegisteredAt: registeredAt.Format(time.RFC3339),
		},
	})
}

// GetAllPatients menangani GET /api/patients
func GetAllPatients(c *gin.Context) {
	rows, err := db.DB.Query(`
		SELECT id, name, nik, tanggal_lahir, no_telepon, created_at
		FROM patients
		ORDER BY created_at DESC
	`)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"success": false, "message": "Gagal mengambil data."})
		return
	}
	defer rows.Close()

	var patients []PatientResponse
	for rows.Next() {
		var p PatientResponse
		var createdAt time.Time
		if err := rows.Scan(&p.PatientID, &p.Name, &p.NIK, &p.TanggalLahir, &p.NoTelepon, &createdAt); err != nil {
			continue
		}
		p.RegisteredAt = createdAt.Format(time.RFC3339)
		patients = append(patients, p)
	}

	c.JSON(http.StatusOK, gin.H{"success": true, "data": patients})
}
