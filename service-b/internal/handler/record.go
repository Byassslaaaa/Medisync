package handler

import (
	"database/sql"
	"net/http"
	"time"

	"hospital/service-b/internal/db"

	"github.com/gin-gonic/gin"
)

type MedicalRecord struct {
	ID        string `json:"id"`
	PatientID string `json:"patient_id"`
	Name      string `json:"name"`
	NIK       string `json:"nik"`
	Diagnosis string `json:"diagnosis"`
	Notes     string `json:"notes"`
	CreatedAt string `json:"created_at"`
	UpdatedAt string `json:"updated_at"`
}

// GetRecordByNIK menangani GET /api/records/:nik
func GetRecordByNIK(c *gin.Context) {
	nik := c.Param("nik")

	var rec MedicalRecord
	var createdAt, updatedAt time.Time

	err := db.DB.QueryRow(`
		SELECT id, patient_id, name, nik, diagnosis, notes, created_at, updated_at
		FROM medical_records
		WHERE nik = $1
	`, nik).Scan(&rec.ID, &rec.PatientID, &rec.Name, &rec.NIK, &rec.Diagnosis, &rec.Notes, &createdAt, &updatedAt)

	if err == sql.ErrNoRows {
		c.JSON(http.StatusNotFound, gin.H{
			"success": false,
			"message": "Rekam medis tidak ditemukan untuk NIK: " + nik,
		})
		return
	}
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"success": false,
			"message": "Gagal mengambil rekam medis.",
		})
		return
	}

	rec.CreatedAt = createdAt.Format(time.RFC3339)
	rec.UpdatedAt = updatedAt.Format(time.RFC3339)

	c.JSON(http.StatusOK, gin.H{"success": true, "data": rec})
}

// GetAllRecords menangani GET /api/records
func GetAllRecords(c *gin.Context) {
	rows, err := db.DB.Query(`
		SELECT id, patient_id, name, nik, diagnosis, notes, created_at, updated_at
		FROM medical_records
		ORDER BY created_at DESC
	`)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"success": false, "message": "Gagal mengambil data."})
		return
	}
	defer rows.Close()

	var records []MedicalRecord
	for rows.Next() {
		var rec MedicalRecord
		var createdAt, updatedAt time.Time
		if err := rows.Scan(&rec.ID, &rec.PatientID, &rec.Name, &rec.NIK, &rec.Diagnosis, &rec.Notes, &createdAt, &updatedAt); err != nil {
			continue
		}
		rec.CreatedAt = createdAt.Format(time.RFC3339)
		rec.UpdatedAt = updatedAt.Format(time.RFC3339)
		records = append(records, rec)
	}

	c.JSON(http.StatusOK, gin.H{"success": true, "data": records})
}
