package grpcserver

import (
	"context"
	"database/sql"
	"log"
	"net"
	"os"
	"time"

	"hospital/service-b/internal/db"
	pb "hospital/service-b/internal/proto"

	"google.golang.org/grpc"
)

// MedicalRecordServer adalah implementasi gRPC server untuk Service B.
type MedicalRecordServer struct {
	pb.UnimplementedMedicalRecordServiceServer
}

// CheckPatientRecord dicall oleh Service A via gRPC untuk mengecek apakah
// pasien dengan NIK tertentu sudah memiliki rekam medis di db_rekam_medis.
func (s *MedicalRecordServer) CheckPatientRecord(ctx context.Context, req *pb.PatientRequest) (*pb.RecordResponse, error) {
	log.Printf("[Service-B][gRPC] ← Menerima CheckPatientRecord untuk NIK: %s", req.GetNik())

	var recordID string
	err := db.DB.QueryRow(
		"SELECT id FROM medical_records WHERE nik = $1",
		req.GetNik(),
	).Scan(&recordID)

	if err == sql.ErrNoRows {
		// Tidak ada rekam medis — ini bukan error, pasien baru
		log.Printf("[Service-B][gRPC] → NIK %s: rekam medis belum ada.", req.GetNik())
		return &pb.RecordResponse{
			HasRecord: false,
			RecordId:  "",
			Message:   "Pasien belum memiliki rekam medis.",
		}, nil
	}

	if err != nil {
		log.Printf("[Service-B][gRPC] ✗ Query DB gagal untuk NIK %s: %v", req.GetNik(), err)
		return nil, err
	}

	log.Printf("[Service-B][gRPC] → NIK %s: rekam medis ditemukan (ID: %s).", req.GetNik(), recordID)
	return &pb.RecordResponse{
		HasRecord: true,
		RecordId:  recordID,
		Message:   "Pasien sudah memiliki rekam medis.",
	}, nil
}

// GetAllRecords dicall oleh Service A via gRPC untuk mengambil semua rekam medis.
func (s *MedicalRecordServer) GetAllRecords(ctx context.Context, req *pb.GetRecordsRequest) (*pb.RecordsListResponse, error) {
	log.Println("[Service-B][gRPC] ← Menerima GetAllRecords")

	rows, err := db.DB.QueryContext(ctx, `
		SELECT id, patient_id, COALESCE(name,''), COALESCE(nik,''),
		       diagnosis, COALESCE(notes,''), created_at, updated_at
		FROM medical_records
		ORDER BY created_at DESC
	`)
	if err != nil {
		log.Printf("[Service-B][gRPC] ✗ Query DB gagal: %v", err)
		return nil, err
	}
	defer rows.Close()

	var records []*pb.MedicalRecordItem
	for rows.Next() {
		var item pb.MedicalRecordItem
		var createdAt, updatedAt time.Time
		if err := rows.Scan(&item.Id, &item.PatientId, &item.Name, &item.Nik,
			&item.Diagnosis, &item.Notes, &createdAt, &updatedAt); err != nil {
			continue
		}
		item.CreatedAt = createdAt.Format(time.RFC3339)
		item.UpdatedAt = updatedAt.Format(time.RFC3339)
		records = append(records, &item)
	}

	log.Printf("[Service-B][gRPC] → Mengirim %d rekam medis ke Service A", len(records))
	return &pb.RecordsListResponse{Records: records}, nil
}

// Start menjalankan gRPC server di port yang ditentukan.
// Dipanggil di goroutine terpisah dari main.go agar tidak memblok HTTP server.
func Start() {
	port := os.Getenv("GRPC_PORT")
	if port == "" {
		port = "50052"
	}

	lis, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("[Service-B][gRPC] Gagal listen pada port %s: %v", port, err)
	}

	s := grpc.NewServer()
	pb.RegisterMedicalRecordServiceServer(s, &MedicalRecordServer{})

	log.Printf("[Service-B][gRPC] gRPC server berjalan di port %s", port)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("[Service-B][gRPC] Server error: %v", err)
	}
}
