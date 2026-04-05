package grpcserver

import (
	"context"
	"database/sql"
	"log"
	"net"
	"os"

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
